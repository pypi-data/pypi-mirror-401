# aiccel/pandora.py
"""
Pandora - LLM-Powered Data Transformation Engine
=================================================

Pandora uses LLMs to transform pandas DataFrames based on natural language instructions.

Features:
- Natural language to pandas transformations
- Multiple execution backends (local, subprocess, microservice)
- Automatic code repair with retries
- Jailbreak detection for safety
"""

import pandas as pd
import json
import numpy as np
import re
import traceback
from typing import Union, Dict, Any, Optional
from pathlib import Path
from enum import Enum

from .providers import LLMProvider
from .execution import Executor, LocalExecutor, SubprocessExecutor, MicroserviceExecutor
from .logging_config import get_logger
from .exceptions import AICCLException

logger = get_logger("pandora")


# =============================================================================
# ENUMS
# =============================================================================

class ExecutionMode(str, Enum):
    """Execution mode for Pandora code execution."""
    LOCAL = "local"
    SUBPROCESS = "subprocess"
    SERVICE = "service"


# =============================================================================
# EXCEPTIONS
# =============================================================================

class PandoraException(AICCLException):
    """Base exception for Pandora errors."""
    pass


class PandoraLoadError(PandoraException):
    """Error loading data source."""
    pass


class PandoraTransformError(PandoraException):
    """Error during data transformation."""
    pass


class PandoraSecurityError(PandoraException):
    """Security-related error (jailbreak detected)."""
    pass


# =============================================================================
# PANDORA CLASS
# =============================================================================

class Pandora:
    """
    LLM-powered DataFrame transformation engine.
    
    Args:
        llm: LLM provider instance
        max_retries: Maximum retry attempts for code generation (default: 4)
        verbose: Enable verbose logging (default: True)
        safety_enabled: Enable jailbreak detection (default: False)
        execution_mode: Execution mode enum or string (default: LOCAL)
        executor: Custom executor instance (overrides execution_mode)
    
    Usage:
        pandora = Pandora(llm=GeminiProvider())
        result_df = pandora.do(df, "Remove all rows where age < 18")
    """
    
    def __init__(
        self, 
        llm: LLMProvider, 
        max_retries: int = 4, 
        verbose: bool = True, 
        safety_enabled: bool = False,
        execution_mode: Union[ExecutionMode, str] = ExecutionMode.LOCAL,
        executor: Optional[Executor] = None
    ):
        self.llm = llm
        self.max_retries = max_retries
        self.verbose = verbose
        self.safety_enabled = safety_enabled
        
        # Normalize execution_mode to enum
        if isinstance(execution_mode, str):
            try:
                execution_mode = ExecutionMode(execution_mode.lower())
            except ValueError:
                logger.warning(f"Unknown execution mode '{execution_mode}', defaulting to LOCAL")
                execution_mode = ExecutionMode.LOCAL
        
        # Initialize Executor
        if executor:
            self.executor = executor
        else:
            self.executor = self._create_executor(execution_mode)
        
        # Log initialization
        logger.info(f"Pandora initialized: executor={self.executor.__class__.__name__}, safety={safety_enabled}")
        
        if verbose:
            logger.info(f"Using {self.executor.__class__.__name__} for code execution")
            if safety_enabled:
                logger.info("Jailbreak detection ENABLED")
            else:
                logger.debug("Jailbreak detection disabled")
        
        # Lazy load jailbreak checker
        self._check_prompt = None
    
    def _create_executor(self, mode: ExecutionMode) -> Executor:
        """Create executor based on execution mode."""
        if mode == ExecutionMode.LOCAL:
            return LocalExecutor()
        elif mode == ExecutionMode.SUBPROCESS:
            return SubprocessExecutor()
        elif mode == ExecutionMode.SERVICE:
            return MicroserviceExecutor()
        else:
            logger.warning(f"Unknown execution mode {mode}, using LocalExecutor")
            return LocalExecutor()
    
    def _get_jailbreak_checker(self):
        """Lazy load jailbreak checker to avoid import overhead."""
        if self._check_prompt is None:
            from .jailbreak import check_prompt
            self._check_prompt = check_prompt
        return self._check_prompt

    def do(
        self,
        source: Union[str, Path, pd.DataFrame],
        instruction: str,
        safe_mode: bool = False
    ) -> pd.DataFrame:
        """
        Execute natural language instructions on a DataFrame.
        
        Args:
            source: DataFrame, path to CSV/Excel/Parquet/JSON, or string path
            instruction: Natural language instruction for transformation
            safe_mode: If True, return original on failure instead of raising
        
        Returns:
            Transformed DataFrame
        
        Raises:
            PandoraSecurityError: If jailbreak detected
            PandoraLoadError: If source cannot be loaded
            PandoraTransformError: If transformation fails after all retries
        """
        # Security Check
        if self.safety_enabled:
            check_prompt = self._get_jailbreak_checker()
            if not check_prompt(instruction):
                raise PandoraSecurityError(
                    "Instruction blocked by jailbreak detector",
                    context={"instruction": instruction[:100]}
                )

        # Load Data
        try:
            df = source.copy() if isinstance(source, pd.DataFrame) else self._load(source)
        except Exception as e:
            if safe_mode:
                logger.error(f"Load error: {e}")
                return pd.DataFrame()
            raise PandoraLoadError(f"Failed to load data source: {e}", context={"source": str(source)})

        # Keep original for safe mode fallback
        original_df = df.copy() 

        # Generate Rich Context
        profile = self._profile_data(df)
        
        last_error = None
        history = []
        last_code_output = ""
        
        for attempt in range(self.max_retries + 1):
            try:
                # Construct Prompt
                if attempt == 0 or not history:
                    prompt = self._build_initial_prompt(profile, instruction)
                else:
                    prompt = self._build_repair_prompt(
                        instruction, 
                        history[-1], 
                        last_error, 
                        last_code_output
                    )

                # LLM Generation
                logger.debug(f"Attempt {attempt+1}/{self.max_retries+1}")
                if self.verbose:
                    logger.info(f"Pandora thinking (attempt {attempt+1}/{self.max_retries+1})")
                
                raw_response = self.llm.generate(prompt, temperature=0.0, max_tokens=6000)
                code = self._extract_code(raw_response)
                history.append(code)

                # Execute using the configured Executor
                result = self.executor.execute(code, dataframe=df)
                
                # Check result
                if not result.success:
                    raise RuntimeError(result.error)
                
                result_df = result.dataframe
                last_code_output = result.output
                
                if not isinstance(result_df, pd.DataFrame):
                    raise ValueError("Code executed but `df` is no longer a DataFrame")
                
                logger.info("Pandora transformation successful")
                return result_df

            except Exception as e:
                last_code_output = ""
                last_error = f"{type(e).__name__}: {str(e)}"
                
                if not isinstance(e, SyntaxError):
                    tb = traceback.format_exc().split('\n')
                    last_error += "\n" + "\n".join(tb[-4:])
                
                logger.warning(f"Attempt {attempt+1} failed: {last_error}")
                
                # Reset df to original state for next attempt
                df = original_df.copy()
                continue

        # All attempts failed
        msg = f"Pandora failed after {self.max_retries + 1} attempts"
        if safe_mode:
            logger.warning(f"{msg}. Returning original DataFrame.")
            return original_df
        else:
            raise PandoraTransformError(
                msg, 
                context={"last_error": last_error, "attempts": self.max_retries + 1}
            )

    def _profile_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate a concise statistical profile of the DataFrame."""
        profile = {
            "shape": df.shape,
            "columns": {},
        }
        
        for col in df.columns[:20]:  # Limit to first 20 columns
            dtype = str(df[col].dtype)
            col_info = {"dtype": dtype}
            
            try:
                col_info["samples"] = df[col].dropna().sample(min(3, len(df))).tolist()
            except Exception:
                col_info["samples"] = df[col].head(3).tolist()

            if np.issubdtype(df[col].dtype, np.number):
                if not df[col].empty:
                    val_min = float(df[col].min())
                    val_max = float(df[col].max())
                    col_info["min"] = val_min if not np.isnan(val_min) else None
                    col_info["max"] = val_max if not np.isnan(val_max) else None
            elif df[col].dtype == 'object' or df[col].dtype.name == 'category':
                col_info["unique_count"] = int(df[col].nunique())
            
            profile["columns"][col] = col_info
        
        return profile

    def _build_initial_prompt(self, profile: Dict[str, Any], instruction: str) -> str:
        """Build the initial prompt for code generation."""
        row_count = profile.get('shape', ['unknown'])[0]
        return f"""
You are PANDORA, an elite Data Engineer AI.
Your goal: Transform the pandas DataFrame `df` based on the User Instruction.

DATA PROFILE (Rows: {row_count}):
{json.dumps(profile, indent=2, default=str)}

USER INSTRUCTION:
"{instruction}"

LIBRARIES AVAILABLE:
pandas (pd), numpy (np), re, random, string, datetime, math, json.

RULES:
1. The input dataframe is ALREADY loaded in the global variable `df`.
2. You MUST modify `df` in place or assign the result back to `df`.
3. Do NOT use markdown or ```python``` blocks. Just raw code.
4. If masking data, use `random` to ensure uniqueness if required.
5. Ensure `df` remains a pandas DataFrame at the end.
6. **SECURITY:** NO system calls (os, subprocess), NO file access.

DATA MASKING GUIDELINES:
- **PRIORITY:** Follow the user's specific format requests EXACTLY above all else.
- **Defaults (if unspecified):**
  - Names: `Person_{{i}}` (e.g. Person_1, Person_2). **AVOID aliases/initials**.
  - Emails: `user_{{i}}@domain.com`.
  - IDs/SSN: Mask with `***` (e.g. ***-***-1234).
- **Consistency:** If masking PII, map identical values to identical masked values.

REGEX WARNING:
- **DO NOT** use backreferences (like `\\1`) in `re.sub` replacement strings. This causes crashes.
- **MUST USE** a lambda function for dynamic replacement.
- **SIGNATURE:** `re.sub(pattern, replacement, string)`. You MUST provide the 3rd argument (the text).
- Correct: `re.sub(r'\\d+', '***', text_variable)`
- Incorrect: `re.sub(r'\\d+', '***')` -> TypeError: missing string argument.

Start your code now:
"""

    def _build_repair_prompt(
        self, 
        instruction: str, 
        bad_code: str, 
        error: str, 
        output: str
    ) -> str:
        """Build repair prompt for failed code."""
        return f"""
The previous code attempt failed.

USER INSTRUCTION: "{instruction}"

FAILED CODE:
{bad_code}

EXECUTION OUTPUT (STDOUT):
{output}

ERROR MESSAGE:
{error}

TASK:
Fix the code logic.
1. If NameError 'df' not defined: Ensure you aren't deleting it.
2. If IndexError: Check column names in Data Profile.
3. If Regex Error: Switch to simple strings or lambda functions; REMOVE backreferences.
4. Return the FULL, CORRECTED Python script.
"""

    def _extract_code(self, text: str) -> str:
        """Extract code from LLM response, removing markdown blocks."""
        text = text.strip()
        match = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1)
        return text

    def _load(self, path: Union[str, Path]) -> pd.DataFrame:
        """Load DataFrame from file path."""
        p = Path(path)
        
        if not p.exists():
            raise PandoraLoadError(f"File not found: {p}")
        
        loaders = {
            ".csv": pd.read_csv,
            ".xlsx": pd.read_excel,
            ".xls": pd.read_excel,
            ".parquet": pd.read_parquet,
            ".json": pd.read_json,
        }
        
        loader = loaders.get(p.suffix.lower())
        if loader:
            return loader(p)
        
        raise PandoraLoadError(
            f"Unsupported file format: {p.suffix}",
            context={"supported": list(loaders.keys())}
        )