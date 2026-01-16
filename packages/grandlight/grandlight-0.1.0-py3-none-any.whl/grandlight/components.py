"""
Glassmorphic UI components for GrandLight.

This module contains the actual UI components with glassmorphism styling,
including panels, buttons, labels, and input fields.
"""

from typing import Optional, Tuple, Callable, Any
from .core import Component, Container, Position, Size, Event, EventType
from .effects import GlassEffect, GlassTheme


class GlassPanel(Container):
    """A glassmorphic panel container.

    GlassPanel is a container with glassmorphism styling that can hold
    other components. It features blur effects, transparency, and optional
    borders for a modern, floating appearance.

    Example:
        >>> panel = GlassPanel(
        ...     size=Size(400, 300),
        ...     effect=GlassTheme.light()
        ... )
        >>> panel.add(GlassButton(text="Click me"))
    """

    def __init__(
        self,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        effect: Optional[GlassEffect] = None,
        padding: int = 10,
        visible: bool = True,
        enabled: bool = True,
    ):
        """Initialize the glass panel.

        Args:
            position: Panel position
            size: Panel size
            effect: Glass effect configuration (default: light theme)
            padding: Inner padding in pixels
            visible: Whether the panel is visible
            enabled: Whether the panel is enabled
        """
        super().__init__(position, size, visible, enabled)
        self.effect = effect or GlassTheme.light()
        self.padding = padding
        self._hover = False

    def render(self, surface: Any) -> None:
        """Render the glass panel with blur and transparency effects.

        Args:
            surface: Surface to render to
        """
        if not self.visible:
            return

        # In a real implementation, this would:
        # 1. Apply backdrop blur filter
        # 2. Fill with semi-transparent background
        # 3. Draw border if specified
        # 4. Apply shadow effect
        # 5. Render children

        abs_pos = self.absolute_position

        # Placeholder rendering logic
        # This would use PIL/Cairo/OpenGL in actual implementation
        _render_data = {
            "type": "glass_panel",
            "x": abs_pos.x,
            "y": abs_pos.y,
            "width": self.size.width,
            "height": self.size.height,
            "blur": self.effect.blur,
            "opacity": self.effect.opacity,
            "background": self.effect.background_color,
            "border": self.effect.border_color,
            "border_width": self.effect.border_width,
            "shadow_blur": self.effect.shadow_blur,
            "shadow_offset": self.effect.shadow_offset,
        }

        # Render children
        super().render(surface)


class GlassButton(Component):
    """A glassmorphic button component.

    Interactive button with glass styling, hover effects, and click handling.

    Example:
        >>> def on_click(event):
        ...     print("Button clicked!")
        >>> button = GlassButton(
        ...     text="Click Me",
        ...     effect=GlassTheme.colorful((100, 150, 255))
        ... )
        >>> button.on(EventType.CLICK, on_click)
    """

    def __init__(
        self,
        text: str,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        effect: Optional[GlassEffect] = None,
        hover_effect: Optional[GlassEffect] = None,
        font_size: int = 14,
        font_family: str = "Inter",
        text_color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        on_click: Optional[Callable[[Event], Any]] = None,
        visible: bool = True,
        enabled: bool = True,
    ):
        """Initialize the glass button.

        Args:
            text: Button text
            position: Button position
            size: Button size (auto-sized if None)
            effect: Glass effect for normal state
            hover_effect: Glass effect for hover state
            font_size: Font size in pixels
            font_family: Font family name
            text_color: RGBA text color
            on_click: Click event handler
            visible: Whether button is visible
            enabled: Whether button is enabled
        """
        # Auto-size based on text if size not provided
        if size is None:
            # Rough estimation: 10px per character + padding
            width = max(100, len(text) * 10 + 40)
            height = 40
            size = Size(width, height)

        super().__init__(position, size, visible, enabled)
        self.text = text
        self.effect = effect or GlassTheme.light()
        self.hover_effect = hover_effect or GlassTheme.frosted()
        self.font_size = font_size
        self.font_family = font_family
        self.text_color = text_color
        self._hover = False
        self._pressed = False

        if on_click:
            self.on(EventType.CLICK, on_click)

        # Register internal event handlers
        self.on(EventType.HOVER, self._on_hover)
        self.on(EventType.HOVER_END, self._on_hover_end)

    def _on_hover(self, event: Event) -> None:
        """Internal hover handler."""
        self._hover = True

    def _on_hover_end(self, event: Event) -> None:
        """Internal hover end handler."""
        self._hover = False

    @property
    def current_effect(self) -> GlassEffect:
        """Get the current effect based on button state."""
        return self.hover_effect if self._hover else self.effect

    def render(self, surface: Any) -> None:
        """Render the glass button.

        Args:
            surface: Surface to render to
        """
        if not self.visible:
            return

        abs_pos = self.absolute_position
        effect = self.current_effect

        # Placeholder rendering data
        _render_data = {
            "type": "glass_button",
            "x": abs_pos.x,
            "y": abs_pos.y,
            "width": self.size.width,
            "height": self.size.height,
            "text": self.text,
            "blur": effect.blur,
            "opacity": effect.opacity,
            "background": effect.background_color,
            "border": effect.border_color,
            "border_width": effect.border_width,
            "font_size": self.font_size,
            "font_family": self.font_family,
            "text_color": self.text_color,
            "hover": self._hover,
            "pressed": self._pressed,
        }


class GlassLabel(Component):
    """A glassmorphic text label.

    Non-interactive text display with optional glass background.

    Example:
        >>> label = GlassLabel(
        ...     text="Welcome to GrandLight",
        ...     font_size=24,
        ...     font_weight="bold"
        ... )
    """

    def __init__(
        self,
        text: str,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        effect: Optional[GlassEffect] = None,
        font_size: int = 14,
        font_family: str = "Inter",
        font_weight: str = "normal",
        text_color: Tuple[int, int, int, int] = (50, 50, 50, 255),
        text_align: str = "left",
        background: bool = True,
        visible: bool = True,
    ):
        """Initialize the glass label.

        Args:
            text: Label text
            position: Label position
            size: Label size (auto-sized if None)
            effect: Glass effect (only used if background=True)
            font_size: Font size in pixels
            font_family: Font family name
            font_weight: Font weight (normal, bold, etc.)
            text_color: RGBA text color
            text_align: Text alignment (left, center, right)
            background: Whether to show glass background
            visible: Whether label is visible
        """
        if size is None:
            # Auto-size based on text
            width = max(100, len(text) * 8 + 20)
            height = font_size + 20
            size = Size(width, height)

        super().__init__(position, size, visible, True)
        self.text = text
        self.effect = effect or GlassTheme.light()
        self.font_size = font_size
        self.font_family = font_family
        self.font_weight = font_weight
        self.text_color = text_color
        self.text_align = text_align
        self.background = background

    def render(self, surface: Any) -> None:
        """Render the glass label.

        Args:
            surface: Surface to render to
        """
        if not self.visible:
            return

        abs_pos = self.absolute_position

        _render_data = {
            "type": "glass_label",
            "x": abs_pos.x,
            "y": abs_pos.y,
            "width": self.size.width,
            "height": self.size.height,
            "text": self.text,
            "font_size": self.font_size,
            "font_family": self.font_family,
            "font_weight": self.font_weight,
            "text_color": self.text_color,
            "text_align": self.text_align,
            "background": self.background,
        }

        if self.background:
            _render_data.update(
                {
                    "blur": self.effect.blur,
                    "opacity": self.effect.opacity,
                    "background_color": self.effect.background_color,
                }
            )


class GlassInput(Component):
    """A glassmorphic text input field.

    Interactive text input with glass styling and keyboard handling.

    Example:
        >>> def on_submit(event):
        ...     print(f"Submitted: {event.data}")
        >>> input_field = GlassInput(
        ...     placeholder="Enter text...",
        ...     on_submit=on_submit
        ... )
    """

    def __init__(
        self,
        placeholder: str = "",
        value: str = "",
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        effect: Optional[GlassEffect] = None,
        focus_effect: Optional[GlassEffect] = None,
        font_size: int = 14,
        font_family: str = "Inter",
        text_color: Tuple[int, int, int, int] = (50, 50, 50, 255),
        placeholder_color: Tuple[int, int, int, int] = (150, 150, 150, 200),
        on_change: Optional[Callable[[Event], Any]] = None,
        on_submit: Optional[Callable[[Event], Any]] = None,
        visible: bool = True,
        enabled: bool = True,
    ):
        """Initialize the glass input field.

        Args:
            placeholder: Placeholder text
            value: Initial value
            position: Input position
            size: Input size
            effect: Glass effect for normal state
            focus_effect: Glass effect for focused state
            font_size: Font size
            font_family: Font family
            text_color: Text color
            placeholder_color: Placeholder text color
            on_change: Change event handler
            on_submit: Submit event handler (Enter key)
            visible: Whether input is visible
            enabled: Whether input is enabled
        """
        if size is None:
            size = Size(200, 40)

        super().__init__(position, size, visible, enabled)
        self.placeholder = placeholder
        self.value = value
        self.effect = effect or GlassTheme.light()
        self.focus_effect = focus_effect or GlassTheme.frosted()
        self.font_size = font_size
        self.font_family = font_family
        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self._focused = False
        self._cursor_position = len(value)

        if on_change:
            self.on(EventType.KEY_PRESS, on_change)
        if on_submit:
            self._submit_handler = on_submit

        self.on(EventType.FOCUS, self._on_focus)
        self.on(EventType.BLUR, self._on_blur)

    def _on_focus(self, event: Event) -> None:
        """Internal focus handler."""
        self._focused = True

    def _on_blur(self, event: Event) -> None:
        """Internal blur handler."""
        self._focused = False

    @property
    def current_effect(self) -> GlassEffect:
        """Get current effect based on focus state."""
        return self.focus_effect if self._focused else self.effect

    def render(self, surface: Any) -> None:
        """Render the glass input field.

        Args:
            surface: Surface to render to
        """
        if not self.visible:
            return

        abs_pos = self.absolute_position
        effect = self.current_effect
        display_text = self.value if self.value else self.placeholder
        display_color = self.text_color if self.value else self.placeholder_color

        _render_data = {
            "type": "glass_input",
            "x": abs_pos.x,
            "y": abs_pos.y,
            "width": self.size.width,
            "height": self.size.height,
            "text": display_text,
            "blur": effect.blur,
            "opacity": effect.opacity,
            "background": effect.background_color,
            "border": effect.border_color,
            "border_width": effect.border_width,
            "font_size": self.font_size,
            "font_family": self.font_family,
            "text_color": display_color,
            "focused": self._focused,
            "cursor_position": self._cursor_position,
        }
