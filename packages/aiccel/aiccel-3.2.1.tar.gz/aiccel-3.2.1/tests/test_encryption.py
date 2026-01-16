"""
Tests for Encryption module.

Coverage targets:
- Key derivation
- Encryption
- Decryption
- Error handling
"""
import pytest
from unittest.mock import patch


class TestEncryptionConstants:
    """Tests for encryption constants."""
    
    def test_constants_exist(self):
        """Test that constants are defined."""
        from aiccel.encryption import CryptoConstants
        
        assert hasattr(CryptoConstants, 'AES_KEY_SIZE')
        assert hasattr(CryptoConstants, 'GCM_NONCE_SIZE')
        assert hasattr(CryptoConstants, 'PBKDF2_ITERATIONS')
        
        assert CryptoConstants.AES_KEY_SIZE == 32
        assert CryptoConstants.GCM_NONCE_SIZE == 12


class TestSecurityLevel:
    """Tests for security level enum."""
    
    def test_security_levels(self):
        """Test security level values."""
        from aiccel.encryption import SecurityLevel
        
        assert SecurityLevel.MAXIMUM == "maximum"
        assert SecurityLevel.HIGH == "high"
        assert SecurityLevel.STANDARD == "standard"


class TestEncryptedData:
    """Tests for EncryptedData structure."""
    
    def test_encrypted_data_structure(self):
        """Test EncryptedData fields."""
        from aiccel.encryption import EncryptedData
        
        data = EncryptedData(
            version="2.0.0",
            algorithm="AES-256-GCM",
            kdf="PBKDF2-HMAC-SHA256",
            iterations=600000,
            salt=b"testsalt12345678901234567890123",
            nonce=b"testnonce12",
            ciphertext=b"encrypted",
            tag=b"tag1234567890123"
        )
        
        assert data.algorithm == "AES-256-GCM"
        assert data.iterations == 600000
    
    def test_to_json(self):
        """Test JSON serialization."""
        from aiccel.encryption import EncryptedData
        
        data = EncryptedData(
            version="2.0.0",
            algorithm="AES-256-GCM",
            kdf="PBKDF2-HMAC-SHA256",
            iterations=600000,
            salt=b"testsalt12345678901234567890123",
            nonce=b"testnonce12",
            ciphertext=b"encrypted",
            tag=b"tag1234567890123"
        )
        
        json_str = data.to_json()
        
        assert isinstance(json_str, str)
        assert "AES-256-GCM" in json_str


class TestEncryptDecrypt:
    """Tests for encryption and decryption."""
    
    @pytest.mark.skipif(
        not pytest.importorskip("cryptography", reason="cryptography not installed"),
        reason="cryptography not installed"
    )
    def test_encrypt_string(self):
        """Test string encryption."""
        try:
            from aiccel.encryption import encrypt_string, CRYPTO_AVAILABLE
            
            if not CRYPTO_AVAILABLE:
                pytest.skip("cryptography not installed")
            
            plaintext = "Hello, Secret World!"
            password = "test_password_123"
            
            encrypted = encrypt_string(plaintext, password)
            
            assert isinstance(encrypted, str)
            assert encrypted != plaintext
        except ImportError:
            pytest.skip("cryptography not installed")
    
    @pytest.mark.skipif(
        not pytest.importorskip("cryptography", reason="cryptography not installed"),
        reason="cryptography not installed"
    )
    def test_decrypt_string(self):
        """Test string decryption."""
        try:
            from aiccel.encryption import encrypt_string, decrypt_string, CRYPTO_AVAILABLE
            
            if not CRYPTO_AVAILABLE:
                pytest.skip("cryptography not installed")
            
            plaintext = "Hello, Secret World!"
            password = "test_password_123"
            
            encrypted = encrypt_string(plaintext, password)
            decrypted = decrypt_string(encrypted, password)
            
            assert decrypted == plaintext
        except ImportError:
            pytest.skip("cryptography not installed")
    
    @pytest.mark.skipif(
        not pytest.importorskip("cryptography", reason="cryptography not installed"),
        reason="cryptography not installed"
    )
    def test_wrong_password_fails(self):
        """Test that wrong password fails decryption."""
        try:
            from aiccel.encryption import encrypt_string, decrypt_string, DecryptionError, CRYPTO_AVAILABLE
            
            if not CRYPTO_AVAILABLE:
                pytest.skip("cryptography not installed")
            
            plaintext = "Secret data"
            password = "correct_password"
            wrong_password = "wrong_password"
            
            encrypted = encrypt_string(plaintext, password)
            
            with pytest.raises((DecryptionError, Exception)):
                decrypt_string(encrypted, wrong_password)
        except ImportError:
            pytest.skip("cryptography not installed")


class TestSecureVault:
    """Tests for SecureVault class."""
    
    @pytest.mark.skipif(
        not pytest.importorskip("cryptography", reason="cryptography not installed"),
        reason="cryptography not installed"
    )
    def test_vault_creation(self, temp_dir):
        """Test creating a secure vault."""
        try:
            from aiccel.encryption import SecureVault, CRYPTO_AVAILABLE
            
            if not CRYPTO_AVAILABLE:
                pytest.skip("cryptography not installed")
            
            vault_path = temp_dir / "test.vault"
            vault = SecureVault(str(vault_path), "test_password")
            
            assert vault is not None
        except ImportError:
            pytest.skip("cryptography not installed")
    
    @pytest.mark.skipif(
        not pytest.importorskip("cryptography", reason="cryptography not installed"),
        reason="cryptography not installed"
    )
    def test_vault_set_get(self, temp_dir):
        """Test setting and getting vault values."""
        try:
            from aiccel.encryption import SecureVault, CRYPTO_AVAILABLE
            
            if not CRYPTO_AVAILABLE:
                pytest.skip("cryptography not installed")
            
            vault_path = temp_dir / "test.vault"
            vault = SecureVault(str(vault_path), "test_password")
            
            vault.set("api_key", "sk-secret-key-123")
            value = vault.get("api_key")
            
            assert value == "sk-secret-key-123"
        except ImportError:
            pytest.skip("cryptography not installed")
