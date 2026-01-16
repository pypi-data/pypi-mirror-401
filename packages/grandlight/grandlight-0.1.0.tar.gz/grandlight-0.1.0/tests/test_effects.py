"""
Unit tests for GrandLight effects module.
"""

import pytest
from grandlight.effects import GlassEffect, GlassTheme


class TestGlassEffect:
    """Test cases for GlassEffect dataclass."""
    
    def test_default_initialization(self):
        """Test GlassEffect with default parameters."""
        effect = GlassEffect()
        assert effect.blur == 20
        assert effect.opacity == 0.7
        assert effect.background_color == (255, 255, 255, 100)
        assert effect.border_color is None
        assert effect.border_width == 1
        assert effect.shadow_blur == 10
        assert effect.shadow_offset == (0, 4)
    
    def test_custom_initialization(self):
        """Test GlassEffect with custom parameters."""
        effect = GlassEffect(
            blur=30,
            opacity=0.5,
            background_color=(100, 150, 200, 120),
            border_color=(255, 255, 255, 180),
            border_width=2
        )
        assert effect.blur == 30
        assert effect.opacity == 0.5
        assert effect.background_color == (100, 150, 200, 120)
        assert effect.border_color == (255, 255, 255, 180)
        assert effect.border_width == 2
    
    def test_invalid_blur(self):
        """Test that invalid blur values raise ValueError."""
        with pytest.raises(ValueError, match="Blur must be between 0 and 100"):
            GlassEffect(blur=101)
        
        with pytest.raises(ValueError, match="Blur must be between 0 and 100"):
            GlassEffect(blur=-1)
    
    def test_invalid_opacity(self):
        """Test that invalid opacity values raise ValueError."""
        with pytest.raises(ValueError, match="Opacity must be between 0.0 and 1.0"):
            GlassEffect(opacity=1.5)
        
        with pytest.raises(ValueError, match="Opacity must be between 0.0 and 1.0"):
            GlassEffect(opacity=-0.1)
    
    def test_invalid_border_width(self):
        """Test that negative border width raises ValueError."""
        with pytest.raises(ValueError, match="Border width must be non-negative"):
            GlassEffect(border_width=-1)
    
    def test_invalid_shadow_blur(self):
        """Test that negative shadow blur raises ValueError."""
        with pytest.raises(ValueError, match="Shadow blur must be non-negative"):
            GlassEffect(shadow_blur=-5)


class TestGlassTheme:
    """Test cases for GlassTheme presets."""
    
    def test_light_theme(self):
        """Test light theme configuration."""
        theme = GlassTheme.light()
        assert isinstance(theme, GlassEffect)
        assert theme.blur == 25
        assert theme.opacity == 0.75
        assert theme.background_color == (255, 255, 255, 120)
    
    def test_dark_theme(self):
        """Test dark theme configuration."""
        theme = GlassTheme.dark()
        assert isinstance(theme, GlassEffect)
        assert theme.blur == 20
        assert theme.opacity == 0.6
        assert theme.background_color == (0, 0, 0, 80)
    
    def test_colorful_theme(self):
        """Test colorful theme with custom tint."""
        tint = (100, 150, 255)
        theme = GlassTheme.colorful(tint)
        assert isinstance(theme, GlassEffect)
        assert theme.background_color == (100, 150, 255, 110)
        assert theme.border_color == (100, 150, 255, 150)
    
    def test_frosted_theme(self):
        """Test frosted theme with heavy blur."""
        theme = GlassTheme.frosted()
        assert isinstance(theme, GlassEffect)
        assert theme.blur == 40
        assert theme.opacity == 0.8
        assert theme.border_width == 2
