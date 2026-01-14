"""
Common validators for NeuralForge applications.

Provides reusable validation patterns for common use cases.
"""

import re


class CommonValidators:
    """
    Reusable validators for common patterns.
    
    Usage with Pydantic:
        from pydantic import BaseModel, validator
        from neuralforge.validators import CommonValidators
        
        class PredictionInput(BaseModel):
            text: str
            model_name: str
            version: str
            
            @validator('text')
            def validate_text(cls, v):
                return CommonValidators.validate_text_length(v, max_len=5000)
            
            @validator('model_name')
            def validate_model_name(cls, v):
                return CommonValidators.validate_model_name(v)
            
            @validator('version')
            def validate_version(cls, v):
                return CommonValidators.validate_version(v)
    """

    @staticmethod
    def validate_text_length(
        v: str,
        min_len: int = 1,
        max_len: int = 10000
    ) -> str:
        """
        Validate text length and strip whitespace.
        
        Args:
            v: Text to validate
            min_len: Minimum length (default: 1)
            max_len: Maximum length (default: 10000)
        
        Returns:
            Stripped and validated text
        
        Raises:
            ValueError: If text is too short or too long
        
        Example:
            >>> CommonValidators.validate_text_length("  hello  ", min_len=1, max_len=100)
            'hello'
        """
        if not isinstance(v, str):
            raise ValueError("Text must be a string")

        v = v.strip()

        if len(v) < min_len:
            raise ValueError(f"Text too short (minimum: {min_len} characters)")

        if len(v) > max_len:
            raise ValueError(f"Text too long (maximum: {max_len} characters)")

        return v

    @staticmethod
    def validate_model_name(v: str) -> str:
        """
        Validate model name format.
        
        Rules:
        - Only lowercase letters, numbers, hyphens, and underscores
        - Must start with a letter
        - Length between 1 and 100 characters
        
        Args:
            v: Model name to validate
        
        Returns:
            Validated model name
        
        Raises:
            ValueError: If model name format is invalid
        
        Example:
            >>> CommonValidators.validate_model_name("sentiment_classifier_v1")
            'sentiment_classifier_v1'
        """
        if not isinstance(v, str):
            raise ValueError("Model name must be a string")

        v = v.strip()

        if not v:
            raise ValueError("Model name cannot be empty")

        if len(v) > 100:
            raise ValueError("Model name too long (maximum: 100 characters)")

        # Must start with letter
        if not v[0].isalpha():
            raise ValueError("Model name must start with a letter")

        # Only lowercase alphanumeric, hyphens, and underscores
        if not re.match(r'^[a-z][a-z0-9_-]*$', v):
            raise ValueError(
                "Model name can only contain lowercase letters, numbers, "
                "hyphens, and underscores"
            )

        return v

    @staticmethod
    def validate_version(v: str) -> str:
        """
        Validate semantic version format.
        
        Format: MAJOR.MINOR.PATCH (e.g., 1.0.0, 2.1.3)
        
        Args:
            v: Version string to validate
        
        Returns:
            Validated version string
        
        Raises:
            ValueError: If version format is invalid
        
        Example:
            >>> CommonValidators.validate_version("1.2.3")
            '1.2.3'
        """
        if not isinstance(v, str):
            raise ValueError("Version must be a string")

        v = v.strip()

        if not re.match(r'^\d+\.\d+\.\d+$', v):
            raise ValueError(
                "Version must be in semantic format (e.g., 1.0.0, 2.1.3)"
            )

        return v

    @staticmethod
    def validate_api_key(v: str) -> str:
        """
        Validate API key format.
        
        Rules:
        - Minimum 16 characters
        - Maximum 128 characters
        - Alphanumeric and special characters allowed
        
        Args:
            v: API key to validate
        
        Returns:
            Validated API key
        
        Raises:
            ValueError: If API key format is invalid
        
        Example:
            >>> CommonValidators.validate_api_key("nf_1234567890abcdef")
            'nf_1234567890abcdef'
        """
        if not isinstance(v, str):
            raise ValueError("API key must be a string")

        v = v.strip()

        if len(v) < 16:
            raise ValueError("API key too short (minimum: 16 characters)")

        if len(v) > 128:
            raise ValueError("API key too long (maximum: 128 characters)")

        return v

    @staticmethod
    def validate_user_id(v: str) -> str:
        """
        Validate user ID format.
        
        Rules:
        - Alphanumeric, hyphens, and underscores only
        - Length between 1 and 50 characters
        
        Args:
            v: User ID to validate
        
        Returns:
            Validated user ID
        
        Raises:
            ValueError: If user ID format is invalid
        
        Example:
            >>> CommonValidators.validate_user_id("user_123")
            'user_123'
        """
        if not isinstance(v, str):
            raise ValueError("User ID must be a string")

        v = v.strip()

        if not v:
            raise ValueError("User ID cannot be empty")

        if len(v) > 50:
            raise ValueError("User ID too long (maximum: 50 characters)")

        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError(
                "User ID can only contain letters, numbers, hyphens, and underscores"
            )

        return v

    @staticmethod
    def validate_email(v: str) -> str:
        """
        Validate email format.
        
        Args:
            v: Email to validate
        
        Returns:
            Validated email (lowercase)
        
        Raises:
            ValueError: If email format is invalid
        
        Example:
            >>> CommonValidators.validate_email("user@example.com")
            'user@example.com'
        """
        if not isinstance(v, str):
            raise ValueError("Email must be a string")

        v = v.strip().lower()

        # Basic email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")

        return v


__all__ = ["CommonValidators"]
