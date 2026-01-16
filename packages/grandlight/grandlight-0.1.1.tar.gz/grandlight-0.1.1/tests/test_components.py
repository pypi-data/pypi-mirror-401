"""
Unit tests for GrandLight components module.
"""

import pytest
from grandlight.core import Position, Size, EventType, Event
from grandlight.components import GlassPanel, GlassButton, GlassLabel, GlassInput
from grandlight.effects import GlassTheme


class TestGlassPanel:
    """Test cases for GlassPanel component."""

    def test_initialization_default(self):
        """Test GlassPanel with default parameters."""
        panel = GlassPanel()
        assert panel.visible is True
        assert panel.enabled is True
        assert panel.padding == 10
        assert panel.effect is not None

    def test_initialization_custom(self):
        """Test GlassPanel with custom parameters."""
        effect = GlassTheme.dark()
        panel = GlassPanel(
            position=Position(100, 200), size=Size(400, 300), effect=effect, padding=20
        )
        assert panel.position.x == 100
        assert panel.position.y == 200
        assert panel.size.width == 400
        assert panel.size.height == 300
        assert panel.effect == effect
        assert panel.padding == 20

    def test_add_children(self):
        """Test adding children to panel."""
        panel = GlassPanel()
        button = GlassButton("Test")
        panel.add(button)

        assert len(panel.children) == 1
        assert button.parent == panel


class TestGlassButton:
    """Test cases for GlassButton component."""

    def test_initialization_default(self):
        """Test GlassButton with default parameters."""
        button = GlassButton("Click Me")
        assert button.text == "Click Me"
        assert button.visible is True
        assert button.enabled is True
        assert button.font_size == 14
        assert button._hover is False
        assert button._pressed is False

    def test_initialization_custom(self):
        """Test GlassButton with custom parameters."""
        effect = GlassTheme.colorful((100, 150, 255))
        button = GlassButton(
            text="Custom",
            position=Position(50, 50),
            size=Size(150, 50),
            effect=effect,
            font_size=16,
        )
        assert button.text == "Custom"
        assert button.size.width == 150
        assert button.size.height == 50
        assert button.effect == effect
        assert button.font_size == 16

    def test_auto_sizing(self):
        """Test button auto-sizing based on text."""
        button = GlassButton("Short")
        assert button.size.width >= 100  # Minimum width
        assert button.size.height == 40

        long_button = GlassButton("This is a much longer button text")
        assert long_button.size.width > button.size.width

    def test_click_handler(self):
        """Test click event handler."""
        clicks = []

        def on_click(event):
            clicks.append(event)

        button = GlassButton("Test", on_click=on_click)
        button.emit(Event(EventType.CLICK, x=50, y=20))

        assert len(clicks) == 1

    def test_hover_state(self):
        """Test hover state changes."""
        button = GlassButton("Test")
        assert button._hover is False

        # Simulate hover
        button.emit(Event(EventType.HOVER, x=50, y=20))
        assert button._hover is True

        # Simulate hover end
        button.emit(Event(EventType.HOVER_END, x=50, y=20))
        assert button._hover is False

    def test_current_effect_normal(self):
        """Test current effect in normal state."""
        effect = GlassTheme.light()
        button = GlassButton("Test", effect=effect)
        assert button.current_effect == effect

    def test_current_effect_hover(self):
        """Test current effect in hover state."""
        effect = GlassTheme.light()
        hover_effect = GlassTheme.frosted()
        button = GlassButton("Test", effect=effect, hover_effect=hover_effect)

        button._hover = True
        assert button.current_effect == hover_effect


class TestGlassLabel:
    """Test cases for GlassLabel component."""

    def test_initialization_default(self):
        """Test GlassLabel with default parameters."""
        label = GlassLabel("Hello World")
        assert label.text == "Hello World"
        assert label.font_size == 14
        assert label.font_weight == "normal"
        assert label.text_align == "left"
        assert label.background is True

    def test_initialization_custom(self):
        """Test GlassLabel with custom parameters."""
        label = GlassLabel(
            text="Title",
            font_size=24,
            font_weight="bold",
            text_align="center",
            background=False,
        )
        assert label.text == "Title"
        assert label.font_size == 24
        assert label.font_weight == "bold"
        assert label.text_align == "center"
        assert label.background is False

    def test_auto_sizing(self):
        """Test label auto-sizing based on text."""
        short_label = GlassLabel("Hi")
        long_label = GlassLabel("This is a much longer label text")

        assert long_label.size.width > short_label.size.width

    def test_font_size_affects_height(self):
        """Test that font size affects label height."""
        small_label = GlassLabel("Test", font_size=12)
        large_label = GlassLabel("Test", font_size=24)

        assert large_label.size.height > small_label.size.height


class TestGlassInput:
    """Test cases for GlassInput component."""

    def test_initialization_default(self):
        """Test GlassInput with default parameters."""
        input_field = GlassInput()
        assert input_field.value == ""
        assert input_field.placeholder == ""
        assert input_field._focused is False
        assert input_field._cursor_position == 0

    def test_initialization_with_value(self):
        """Test GlassInput with initial value."""
        input_field = GlassInput(value="Initial text", placeholder="Enter text...")
        assert input_field.value == "Initial text"
        assert input_field.placeholder == "Enter text..."
        assert input_field._cursor_position == len("Initial text")

    def test_focus_state(self):
        """Test focus state changes."""
        input_field = GlassInput()
        assert input_field._focused is False

        # Simulate focus
        input_field.emit(Event(EventType.FOCUS))
        assert input_field._focused is True

        # Simulate blur
        input_field.emit(Event(EventType.BLUR))
        assert input_field._focused is False

    def test_current_effect_normal(self):
        """Test current effect in normal state."""
        effect = GlassTheme.light()
        input_field = GlassInput(effect=effect)
        assert input_field.current_effect == effect

    def test_current_effect_focused(self):
        """Test current effect in focused state."""
        effect = GlassTheme.light()
        focus_effect = GlassTheme.frosted()
        input_field = GlassInput(effect=effect, focus_effect=focus_effect)

        input_field._focused = True
        assert input_field.current_effect == focus_effect

    def test_on_change_handler(self):
        """Test on_change event handler."""
        changes = []

        def on_change(event):
            changes.append(event)

        input_field = GlassInput(on_change=on_change)
        input_field.emit(Event(EventType.KEY_PRESS, key="a"))

        assert len(changes) == 1

    def test_custom_size(self):
        """Test custom size initialization."""
        input_field = GlassInput(size=Size(300, 50))
        assert input_field.size.width == 300
        assert input_field.size.height == 50
