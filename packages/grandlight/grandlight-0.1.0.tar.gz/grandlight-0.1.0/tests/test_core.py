"""
Unit tests for GrandLight core module.
"""

import pytest
from grandlight.core import (
    Component,
    Container,
    Position,
    Size,
    Rect,
    Event,
    EventType,
)


class TestPosition:
    """Test cases for Position dataclass."""

    def test_initialization(self):
        """Test Position initialization."""
        pos = Position(100, 200)
        assert pos.x == 100
        assert pos.y == 200

    def test_default_values(self):
        """Test Position default values."""
        pos = Position()
        assert pos.x == 0
        assert pos.y == 0

    def test_unpacking(self):
        """Test Position unpacking."""
        pos = Position(50, 75)
        x, y = pos
        assert x == 50
        assert y == 75


class TestSize:
    """Test cases for Size dataclass."""

    def test_initialization(self):
        """Test Size initialization."""
        size = Size(800, 600)
        assert size.width == 800
        assert size.height == 600

    def test_default_values(self):
        """Test Size default values."""
        size = Size()
        assert size.width == 100
        assert size.height == 100

    def test_unpacking(self):
        """Test Size unpacking."""
        size = Size(1920, 1080)
        w, h = size
        assert w == 1920
        assert h == 1080


class TestRect:
    """Test cases for Rect dataclass."""

    def test_initialization(self):
        """Test Rect initialization."""
        rect = Rect(10, 20, 100, 50)
        assert rect.x == 10
        assert rect.y == 20
        assert rect.width == 100
        assert rect.height == 50

    def test_position_property(self):
        """Test position property."""
        rect = Rect(15, 25, 100, 100)
        pos = rect.position
        assert pos.x == 15
        assert pos.y == 25

    def test_size_property(self):
        """Test size property."""
        rect = Rect(0, 0, 200, 150)
        size = rect.size
        assert size.width == 200
        assert size.height == 150

    def test_right_property(self):
        """Test right edge calculation."""
        rect = Rect(10, 10, 100, 100)
        assert rect.right == 110

    def test_bottom_property(self):
        """Test bottom edge calculation."""
        rect = Rect(10, 10, 100, 100)
        assert rect.bottom == 110

    def test_center_property(self):
        """Test center point calculation."""
        rect = Rect(0, 0, 100, 100)
        center = rect.center
        assert center.x == 50
        assert center.y == 50

    def test_contains_point_inside(self):
        """Test contains method with point inside."""
        rect = Rect(10, 10, 100, 100)
        assert rect.contains(50, 50) is True
        assert rect.contains(10, 10) is True
        assert rect.contains(110, 110) is True

    def test_contains_point_outside(self):
        """Test contains method with point outside."""
        rect = Rect(10, 10, 100, 100)
        assert rect.contains(5, 50) is False
        assert rect.contains(115, 50) is False
        assert rect.contains(50, 5) is False
        assert rect.contains(50, 115) is False

    def test_intersects_overlapping(self):
        """Test intersects with overlapping rectangles."""
        rect1 = Rect(10, 10, 100, 100)
        rect2 = Rect(50, 50, 100, 100)
        assert rect1.intersects(rect2) is True
        assert rect2.intersects(rect1) is True

    def test_intersects_non_overlapping(self):
        """Test intersects with non-overlapping rectangles."""
        rect1 = Rect(10, 10, 50, 50)
        rect2 = Rect(100, 100, 50, 50)
        assert rect1.intersects(rect2) is False
        assert rect2.intersects(rect1) is False


class TestEvent:
    """Test cases for Event dataclass."""

    def test_initialization(self):
        """Test Event initialization."""
        event = Event(EventType.CLICK, x=100, y=200, data="test")
        assert event.event_type == EventType.CLICK
        assert event.x == 100
        assert event.y == 200
        assert event.data == "test"

    def test_default_values(self):
        """Test Event default values."""
        event = Event(EventType.HOVER)
        assert event.x == 0
        assert event.y == 0
        assert event.key is None
        assert event.data is None


class MockComponent(Component):
    """Mock component for testing."""

    def render(self, surface):
        """Mock render method."""
        pass


class TestComponent:
    """Test cases for Component base class."""

    def test_initialization(self):
        """Test Component initialization."""
        comp = MockComponent()
        assert comp.visible is True
        assert comp.enabled is True
        assert comp.parent is None

    def test_custom_position_size(self):
        """Test Component with custom position and size."""
        pos = Position(50, 75)
        size = Size(200, 150)
        comp = MockComponent(position=pos, size=size)
        assert comp.position == pos
        assert comp.size == size

    def test_bounds_property(self):
        """Test bounds property."""
        comp = MockComponent(position=Position(10, 20), size=Size(100, 50))
        bounds = comp.bounds
        assert bounds.x == 10
        assert bounds.y == 20
        assert bounds.width == 100
        assert bounds.height == 50

    def test_absolute_position_no_parent(self):
        """Test absolute position without parent."""
        comp = MockComponent(position=Position(50, 75))
        abs_pos = comp.absolute_position
        assert abs_pos.x == 50
        assert abs_pos.y == 75

    def test_event_handler_registration(self):
        """Test event handler registration."""
        comp = MockComponent()
        called = []

        def handler(event):
            called.append(event)

        comp.on(EventType.CLICK, handler)
        event = Event(EventType.CLICK, x=10, y=20)
        comp.emit(event)

        assert len(called) == 1
        assert called[0] == event

    def test_multiple_event_handlers(self):
        """Test multiple handlers for same event type."""
        comp = MockComponent()
        calls = []

        def handler1(event):
            calls.append("handler1")

        def handler2(event):
            calls.append("handler2")

        comp.on(EventType.CLICK, handler1)
        comp.on(EventType.CLICK, handler2)
        comp.emit(Event(EventType.CLICK))

        assert calls == ["handler1", "handler2"]

    def test_disabled_component_no_events(self):
        """Test that disabled components don't handle events."""
        comp = MockComponent(enabled=False)
        called = []

        def handler(event):
            called.append(event)

        comp.on(EventType.CLICK, handler)
        result = comp.handle_event(Event(EventType.CLICK, x=50, y=50))

        assert result is False
        assert len(called) == 0


class TestContainer:
    """Test cases for Container class."""

    def test_add_child(self):
        """Test adding child components."""
        container = Container()
        child = MockComponent()
        container.add(child)

        assert len(container.children) == 1
        assert container.children[0] == child
        assert child.parent == container

    def test_add_child_with_parent_raises_error(self):
        """Test that adding component with existing parent raises error."""
        container1 = Container()
        container2 = Container()
        child = MockComponent()

        container1.add(child)

        with pytest.raises(ValueError, match="already has a parent"):
            container2.add(child)

    def test_remove_child(self):
        """Test removing child components."""
        container = Container()
        child = MockComponent()
        container.add(child)
        container.remove(child)

        assert len(container.children) == 0
        assert child.parent is None

    def test_clear_children(self):
        """Test clearing all children."""
        container = Container()
        child1 = MockComponent()
        child2 = MockComponent()
        container.add(child1)
        container.add(child2)
        container.clear()

        assert len(container.children) == 0
        assert child1.parent is None
        assert child2.parent is None

    def test_event_propagation_to_children(self):
        """Test that events propagate to children."""
        container = Container(size=Size(200, 200))
        child = MockComponent(position=Position(50, 50), size=Size(100, 100))
        container.add(child)

        called = []

        def handler(event):
            called.append(event)

        child.on(EventType.CLICK, handler)

        # Event within child bounds
        event = Event(EventType.CLICK, x=75, y=75)
        container.handle_event(event)

        assert len(called) == 1
