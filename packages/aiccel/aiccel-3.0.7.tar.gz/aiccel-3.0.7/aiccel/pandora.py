import pandas as pd
import json
import numpy as np
import re
import ast
import traceback
import io
import contextlib
import random
import string
import datetime
import math
from typing import Union, Dict, Any, List, Optional
from pathlib import Path

from .providers import LLMProvider

class Pandora:
    def __init__(self, llm: LLMProvider, max_retries: int = 4, verbose: bool = True, safety_enabled: bool = False):
        self.llm = llm
        self.max_retries = max_retries
        self.verbose = verbose
        self.safety_enabled = safety_enabled
        
        # Security warning
        if verbose:
            print("WARNING: Pandora uses local code execution. Ensure you trust the input instructions.")
            if safety_enabled:
                print("Safety: Jailbreak detection ENABLED.")
            else:
                print("Safety: Jailbreak detection DISABLED. Enable with safety_enabled=True.")
            
        from .jailbreak import check_prompt
        self._check_prompt = check_prompt

    def do(
        self,
        source: Union[str, Path, pd.DataFrame],
        instruction: str,
        safe_mode: bool = False
    ) -> pd.DataFrame:
        """
        Executes instructions on a DataFrame.
        """
        # 0. Security Check
        if not self._check_prompt(instruction):
            raise ValueError("Security Alert: Instruction blocked by jailbreak detector.")

        # 1. Load Data
        try:
            df = source.copy() if isinstance(source, pd.DataFrame) else self._load(source)
        except Exception as e:
            if safe_mode:
                print(f"Pandora Load Error: {e}")
                return pd.DataFrame()
            raise e

        # We keep the original for safe mode fallback
        original_df = df.copy() 

        # 2. Generate Rich Context
        profile = self._profile_data(df)
        
        last_error = None
        history = []
        last_code_output = ""
        
        # Define SAFE execution scope
        safe_builtins = {
            "abs": abs, "all": all, "any": any, "bool": bool,
            "complex": complex, "dict": dict, "divmod": divmod,
            "enumerate": enumerate, "filter": filter, "float": float,
            "frozenset": frozenset, "hash": hash, "hex": hex,
            "int": int, "isinstance": isinstance, "issubclass": issubclass,
            "iter": iter, "len": len, "list": list, "map": map,
            "max": max, "min": min, "next": next, "oct": oct,
            "ord": ord, "pow": pow, "print": print, "range": range, 
            "repr": repr, "reversed": reversed, "round": round,
            "set": set, "slice": slice, "sorted": sorted,
            "str": str, "sum": sum, "tuple": tuple, "type": type,
            "zip": zip, "None": None, "True": True, "False": False,
            "__import__": __import__ 
        }

        for attempt in range(self.max_retries + 1):
            try:
                # 3. Construct Prompt
                if attempt == 0 or not history:
                    prompt = self._build_initial_prompt(profile, instruction)
                else:
                    prompt = self._build_repair_prompt(
                        instruction, 
                        history[-1], 
                        last_error, 
                        last_code_output
                    )

                # 4. LLM Generation
                if self.verbose:
                    print(f"--- Pandora Thinking (Attempt {attempt+1}/{self.max_retries+1}) ---")
                
                # Using a slightly longer context window
                raw_response = self.llm.generate(prompt, temperature=0.0, max_tokens=6000)
                code = self._extract_code(raw_response)
                history.append(code)

                # 5. Syntax Check
                ast.parse(code) 

                # 6. Prepare Execution Environment
                output_buffer = io.StringIO()
                
                execution_scope = {
                    "df": df,  # Work directly on the DF reference so inplace mods work
                    "pd": pd,
                    "np": np,
                    "re": re,
                    "random": random,
                    "string": string,
                    "datetime": datetime,
                    "math": math,
                    "json": json,
                    "__builtins__": safe_builtins
                }

                # 7. Execute with Output Capture
                with contextlib.redirect_stdout(output_buffer):
                    exec(code, execution_scope)
                
                # 8. Validation
                result_df = execution_scope.get("df")
                
                if not isinstance(result_df, pd.DataFrame):
                    raise ValueError("The code executed but `df` variable was lost or is no longer a DataFrame.")
                
                if self.verbose:
                    print("--- Pandora Success ---")
                
                return result_df

            except Exception as e:
                last_code_output = output_buffer.getvalue() if 'output_buffer' in locals() else ""
                
                last_error = f"{type(e).__name__}: {str(e)}"
                if not isinstance(e, SyntaxError):
                    tb = traceback.format_exc().split('\n')
                    last_error += "\n" + "\n".join(tb[-4:])
                
                if self.verbose:
                    print(f"Pandora Error (Attempt {attempt+1}): {last_error}")
                
                # If we failed, reset the DF to original state for the next attempt so we don't work on broken state
                df = original_df.copy()
                
                continue

        # Failure Handling
        msg = f"Pandora failed to transform data after {self.max_retries} attempts."
        if safe_mode:
            print(f"WARNING: {msg} Returning original DataFrame.")
            return original_df
        else:
            raise RuntimeError(f"{msg}\nLast Error: {last_error}")

    def _profile_data(self, df: pd.DataFrame) -> Dict:
        """Generates a concise statistical profile."""
        profile = {
            "shape": df.shape,
            "columns": {},
        }
        
        for col in df.columns[:20]: 
            dtype = str(df[col].dtype)
            col_info = {"dtype": dtype}
            try:
                col_info["samples"] = df[col].dropna().sample(min(3, len(df))).tolist()
            except:
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

    def _build_initial_prompt(self, profile: Dict, instruction: str) -> str:
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
- Correct: `re.sub(r'\d+', '***', text_variable)`
- Incorrect: `re.sub(r'\d+', '***')` -> TypeError: missing string argument.

Start your code now:
"""

    def _build_repair_prompt(self, instruction, bad_code, error, output) -> str:
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
        text = text.strip()
        match = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1)
        return text

    def _load(self, path):
        p = Path(path)
        if p.suffix == ".csv": return pd.read_csv(p)
        if p.suffix in [".xlsx", ".xls"]: return pd.read_excel(p)
        if p.suffix == ".parquet": return pd.read_parquet(p)
        if p.suffix == ".json": return pd.read_json(p)
        raise ValueError(f"Unsupported file format: {p}")