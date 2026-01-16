"""
GrandLight - A Modern Glassmorphism GUI Library

GrandLight brings elegant glassmorphism design to Python applications,
featuring frosted glass effects, transparency layers, and modern UI components.

Copyright (c) 2008-2026 Rheehose (Rhee Creative)
Licensed under the MIT License
"""

__version__ = "0.1.0"
__author__ = "Rheehose (Rhee Creative)"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2008-2026 Rheehose (Rhee Creative)"

# Core imports
from .core import Component, Container, Position, Size, Rect, Event, EventType
from .effects import GlassEffect, GlassTheme
from .window import Window
from .components import GlassPanel, GlassButton, GlassLabel, GlassInput

__all__ = [
    # Metadata
    "__version__",
    "__author__",
    "__license__",
    "__copyright__",
    # Core classes
    "Component",
    "Container",
    "Position",
    "Size",
    "Rect",
    "Event",
    "EventType",
    # Effects
    "GlassEffect",
    "GlassTheme",
    # Main window
    "Window",
    # Components
    "GlassPanel",
    "GlassButton",
    "GlassLabel",
    "GlassInput",
]
