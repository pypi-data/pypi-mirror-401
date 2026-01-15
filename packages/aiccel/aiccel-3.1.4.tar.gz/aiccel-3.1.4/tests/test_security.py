# tests/test_security.py
"""
Security Tests
===============

Tests for encryption and privacy features.
"""

import pytest


class TestPrivacy:
    """Test privacy/PII masking."""
    
    def test_mask_email(self):
        """Mask email addresses."""
        from aiccel import mask_text
        
        text = "Contact me at john@example.com"
        masked = mask_text(text)
        
        assert "john@example.com" not in masked
        assert "[EMAIL_" in masked
    
    def test_mask_phone(self):
        """Mask phone numbers."""
        from aiccel import mask_text
        
        text = "Call me at 555-123-4567"
        masked = mask_text(text)
        
        assert "555-123-4567" not in masked
    
    def test_unmask_text(self):
        """Unmask previously masked text."""
        from aiccel import mask_text, unmask_text
        
        original = "Email: test@example.com"
        masked = mask_text(original)
        unmasked = unmask_text(masked)
        
        assert "test@example.com" in unmasked
    
    def test_entity_masker(self):
        """Test EntityMasker class."""
        from aiccel import EntityMasker
        
        masker = EntityMasker()
        text = "John's SSN is 123-45-6789"
        
        masked, entities = masker.mask(text)
        
        assert "123-45-6789" not in masked
        assert len(entities) > 0
        
        # Unmask
        original = masker.unmask(masked, entities)
        assert "123-45-6789" in original


class TestEncryption:
    """Test encryption features."""
    
    def test_encryption_available(self):
        """Check if encryption is available."""
        from aiccel import ENCRYPTION_AVAILABLE
        # Should be a boolean
        assert isinstance(ENCRYPTION_AVAILABLE, bool)
    
    @pytest.mark.skipif(
        "not __import__('aiccel').ENCRYPTION_AVAILABLE",
        reason="Encryption not available"
    )
    def test_encrypt_decrypt(self):
        """Test basic encryption/decryption."""
        from aiccel.encryption import encrypt, decrypt, generate_key
        
        key = generate_key()
        plaintext = "Secret message"
        
        ciphertext = encrypt(plaintext, key)
        decrypted = decrypt(ciphertext, key)
        
        assert decrypted == plaintext
    
    @pytest.mark.skipif(
        "not __import__('aiccel').ENCRYPTION_AVAILABLE",
        reason="Encryption not available"
    )
    def test_password_hashing(self):
        """Test password hashing."""
        from aiccel.encryption import hash_password, verify_password
        
        password = "my_secure_password"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)


class TestSecureVault:
    """Test secure vault."""
    
    @pytest.mark.skipif(
        "not __import__('aiccel').ENCRYPTION_AVAILABLE",
        reason="Encryption not available"
    )
    def test_vault_store_retrieve(self):
        """Store and retrieve secrets."""
        from aiccel.encryption import SecureVault
        
        vault = SecureVault(master_password="test_master")
        
        vault.set("api_key", "sk-12345")
        retrieved = vault.get("api_key")
        
        assert retrieved == "sk-12345"
    
    @pytest.mark.skipif(
        "not __import__('aiccel').ENCRYPTION_AVAILABLE",
        reason="Encryption not available"
    )
    def test_vault_save_load(self, tmp_path):
        """Save and load vault."""
        from aiccel.encryption import SecureVault
        
        vault_path = str(tmp_path / "test.vault")
        
        vault = SecureVault(master_password="test_master")
        vault.set("secret", "value123")
        vault.save(vault_path)
        
        loaded = SecureVault.load(vault_path, "test_master")
        assert loaded.get("secret") == "value123"
