"""
Core glassmorphism effects for GrandLight components.

This module provides the fundamental blur and transparency effects
that create the signature glassmorphism aesthetic.
"""

from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class GlassEffect:
    """Configuration for glassmorphism visual effects.

    Attributes:
        blur: Blur intensity (0-100), higher values create stronger blur
        opacity: Transparency level (0.0-1.0), lower values are more transparent
        background_color: RGBA color tuple for the glass tint
        border_color: Optional RGBA border color for enhanced depth
        border_width: Border width in pixels
        shadow_blur: Soft shadow blur radius for floating effect
        shadow_offset: Shadow offset as (x, y) tuple

    Example:
        >>> effect = GlassEffect(
        ...     blur=20,
        ...     opacity=0.7,
        ...     background_color=(255, 255, 255, 100)
        ... )
    """

    blur: int = 20
    opacity: float = 0.7
    background_color: Tuple[int, int, int, int] = (255, 255, 255, 100)
    border_color: Optional[Tuple[int, int, int, int]] = None
    border_width: int = 1
    shadow_blur: int = 10
    shadow_offset: Tuple[int, int] = (0, 4)

    def __post_init__(self):
        """Validate effect parameters."""
        if not 0 <= self.blur <= 100:
            raise ValueError("Blur must be between 0 and 100")
        if not 0.0 <= self.opacity <= 1.0:
            raise ValueError("Opacity must be between 0.0 and 1.0")
        if self.border_width < 0:
            raise ValueError("Border width must be non-negative")
        if self.shadow_blur < 0:
            raise ValueError("Shadow blur must be non-negative")


class GlassTheme:
    """Pre-defined glassmorphism themes.

    Provides common color schemes and effect configurations
    for quick application styling.
    """

    @staticmethod
    def light() -> GlassEffect:
        """Light glassmorphism theme with bright tones.

        Returns:
            GlassEffect configured for light backgrounds
        """
        return GlassEffect(
            blur=25,
            opacity=0.75,
            background_color=(255, 255, 255, 120),
            border_color=(255, 255, 255, 180),
            border_width=1,
            shadow_blur=15,
            shadow_offset=(0, 4),
        )

    @staticmethod
    def dark() -> GlassEffect:
        """Dark glassmorphism theme with deep tones.

        Returns:
            GlassEffect configured for dark backgrounds
        """
        return GlassEffect(
            blur=20,
            opacity=0.6,
            background_color=(0, 0, 0, 80),
            border_color=(255, 255, 255, 40),
            border_width=1,
            shadow_blur=20,
            shadow_offset=(0, 6),
        )

    @staticmethod
    def colorful(tint_color: Tuple[int, int, int]) -> GlassEffect:
        """Colorful glassmorphism with custom tint.

        Args:
            tint_color: RGB color tuple for the glass tint

        Returns:
            GlassEffect with the specified color tint

        Example:
            >>> blue_glass = GlassTheme.colorful((100, 150, 255))
        """
        r, g, b = tint_color
        return GlassEffect(
            blur=22,
            opacity=0.65,
            background_color=(r, g, b, 110),
            border_color=(r, g, b, 150),
            border_width=1,
            shadow_blur=12,
            shadow_offset=(0, 5),
        )

    @staticmethod
    def frosted() -> GlassEffect:
        """Heavily frosted glass effect with strong blur.

        Returns:
            GlassEffect with intense blur for frosted appearance
        """
        return GlassEffect(
            blur=40,
            opacity=0.8,
            background_color=(255, 255, 255, 140),
            border_color=(255, 255, 255, 200),
            border_width=2,
            shadow_blur=18,
            shadow_offset=(0, 8),
        )
