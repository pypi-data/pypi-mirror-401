"""
Tests for Privacy module (EntityMasker).

Coverage targets:
- Entity masking
- Entity unmasking
- Different entity types
- Async operations
"""
import pytest
from unittest.mock import MagicMock, patch


class TestEntityMaskerInitialization:
    """Tests for EntityMasker initialization."""
    
    def test_basic_initialization(self):
        """Test basic EntityMasker creation."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        
        assert masker._gliner_model is None
        assert masker._model_loaded is False


class TestEmailMasking:
    """Tests for email masking."""
    
    def test_mask_email(self):
        """Test masking email addresses."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        text = "Contact me at john.doe@example.com for more info."
        
        masked, mapping = masker.mask_sensitive_entities(text, remove_email=True)
        
        assert "john.doe@example.com" not in masked
        assert len(mapping) > 0
    
    def test_mask_multiple_emails(self):
        """Test masking multiple emails."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        text = "Email alice@test.com or bob@test.org"
        
        masked, mapping = masker.mask_sensitive_entities(text, remove_email=True)
        
        assert "alice@test.com" not in masked
        assert "bob@test.org" not in masked


class TestPhoneMasking:
    """Tests for phone number masking."""
    
    def test_mask_us_phone(self):
        """Test masking US phone numbers."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        text = "Call me at 555-123-4567"
        
        masked, mapping = masker.mask_sensitive_entities(text, remove_phone=True)
        
        assert "555-123-4567" not in masked
    
    def test_mask_phone_with_parentheses(self):
        """Test masking phone with parentheses format."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        text = "Phone: (555) 123-4567"
        
        masked, mapping = masker.mask_sensitive_entities(text, remove_phone=True)
        
        assert "(555) 123-4567" not in masked


class TestUnmasking:
    """Tests for entity unmasking."""
    
    def test_unmask_entities(self):
        """Test unmasking masked entities."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        original = "Contact john@example.com"
        
        masked, mapping = masker.mask_sensitive_entities(original, remove_email=True)
        unmasked = masker.unmask_entities(masked, mapping)
        
        assert unmasked == original
    
    def test_unmask_multiple_entities(self):
        """Test unmasking multiple entities."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        original = "Email: a@test.com, Phone: 555-1234"
        
        masked, mapping = masker.mask_sensitive_entities(
            original, 
            remove_email=True, 
            remove_phone=True
        )
        unmasked = masker.unmask_entities(masked, mapping)
        
        assert "a@test.com" in unmasked
        assert "555-1234" in unmasked


class TestConvenienceFunctions:
    """Tests for convenience functions."""
    
    def test_mask_text_function(self):
        """Test mask_text convenience function."""
        from aiccel.privacy import mask_text
        
        text = "Email: user@domain.com"
        masked, mapping = mask_text(text, remove_email=True)
        
        assert "user@domain.com" not in masked
    
    def test_unmask_text_function(self):
        """Test unmask_text convenience function."""
        from aiccel.privacy import mask_text, unmask_text
        
        original = "Contact test@example.org"
        masked, mapping = mask_text(original, remove_email=True)
        unmasked = unmask_text(masked, mapping)
        
        assert unmasked == original


class TestProcessTextSafely:
    """Tests for safe text processing."""
    
    def test_process_text_safely(self):
        """Test process_text_safely workflow."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        
        def mock_processor(text):
            return f"Processed: {text}"
        
        result = masker.process_text_safely(
            "Email: user@test.com",
            mock_processor,
            remove_email=True
        )
        
        # Result should have original email restored
        assert "user@test.com" in result["unmasked_response"]


class TestNoMaskingWhenDisabled:
    """Tests for when masking is disabled."""
    
    def test_no_email_mask_when_disabled(self):
        """Test email not masked when remove_email=False."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        text = "Email: user@example.com"
        
        masked, mapping = masker.mask_sensitive_entities(text, remove_email=False)
        
        assert "user@example.com" in masked
    
    def test_no_mask_when_all_disabled(self):
        """Test no masking when all options are False."""
        from aiccel.privacy import EntityMasker
        
        masker = EntityMasker()
        text = "Email: user@example.com, Phone: 555-1234"
        
        masked, mapping = masker.mask_sensitive_entities(
            text, 
            remove_email=False, 
            remove_phone=False
        )
        
        assert masked == text
        assert len(mapping) == 0
