"""
Core base classes for GrandLight components.

This module provides the foundation for all glassmorphic UI components,
including base classes, event handling, and rendering interfaces.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Callable, Any
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """Types of UI events that components can handle."""

    CLICK = "click"
    HOVER = "hover"
    HOVER_END = "hover_end"
    FOCUS = "focus"
    BLUR = "blur"
    KEY_PRESS = "key_press"
    RESIZE = "resize"
    DRAG = "drag"
    DROP = "drop"


@dataclass
class Event:
    """Represents a UI event.

    Attributes:
        event_type: Type of the event
        x: X coordinate of the event (if applicable)
        y: Y coordinate of the event (if applicable)
        key: Key code for keyboard events
        data: Additional event data
    """

    event_type: EventType
    x: int = 0
    y: int = 0
    key: Optional[str] = None
    data: Any = None


@dataclass
class Position:
    """2D position with x and y coordinates."""

    x: int = 0
    y: int = 0

    def __iter__(self):
        """Allow unpacking: x, y = position."""
        return iter((self.x, self.y))


@dataclass
class Size:
    """2D size with width and height."""

    width: int = 100
    height: int = 100

    def __iter__(self):
        """Allow unpacking: w, h = size."""
        return iter((self.width, self.height))


@dataclass
class Rect:
    """Rectangle defined by position and size.

    Attributes:
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Rectangle width
        height: Rectangle height
    """

    x: int = 0
    y: int = 0
    width: int = 100
    height: int = 100

    @property
    def position(self) -> Position:
        """Get the position of the rectangle."""
        return Position(self.x, self.y)

    @property
    def size(self) -> Size:
        """Get the size of the rectangle."""
        return Size(self.width, self.height)

    @property
    def right(self) -> int:
        """Get the right edge x coordinate."""
        return self.x + self.width

    @property
    def bottom(self) -> int:
        """Get the bottom edge y coordinate."""
        return self.y + self.height

    @property
    def center(self) -> Position:
        """Get the center point of the rectangle."""
        return Position(self.x + self.width // 2, self.y + self.height // 2)

    def contains(self, x: int, y: int) -> bool:
        """Check if a point is inside the rectangle.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if point is inside the rectangle
        """
        return self.x <= x <= self.right and self.y <= y <= self.bottom

    def intersects(self, other: "Rect") -> bool:
        """Check if this rectangle intersects with another.

        Args:
            other: Another rectangle

        Returns:
            True if rectangles intersect
        """
        return not (
            self.right < other.x
            or self.x > other.right
            or self.bottom < other.y
            or self.y > other.bottom
        )


class Component(ABC):
    """Abstract base class for all GrandLight UI components.

    All interactive and visual elements inherit from this class,
    which provides common functionality for rendering, event handling,
    and layout management.
    """

    def __init__(
        self,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        visible: bool = True,
        enabled: bool = True,
    ):
        """Initialize the component.

        Args:
            position: Component position (default: 0, 0)
            size: Component size (default: 100x100)
            visible: Whether the component is visible
            enabled: Whether the component is enabled for interaction
        """
        self.position = position or Position(0, 0)
        self.size = size or Size(100, 100)
        self.visible = visible
        self.enabled = enabled
        self.parent: Optional["Container"] = None
        self._event_handlers: dict[EventType, List[Callable]] = {}

    @property
    def bounds(self) -> Rect:
        """Get the bounding rectangle of this component."""
        return Rect(self.position.x, self.position.y, self.size.width, self.size.height)

    @property
    def absolute_position(self) -> Position:
        """Get the absolute position in window coordinates.

        Returns:
            Absolute position considering parent hierarchy
        """
        if self.parent is None:
            return self.position

        parent_pos = self.parent.absolute_position
        return Position(parent_pos.x + self.position.x, parent_pos.y + self.position.y)

    def on(self, event_type: EventType, handler: Callable[[Event], Any]) -> None:
        """Register an event handler.

        Args:
            event_type: Type of event to handle
            handler: Callback function to handle the event

        Example:
            >>> def on_click(event):
            ...     print(f"Clicked at {event.x}, {event.y}")
            >>> button.on(EventType.CLICK, on_click)
        """
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)

    def emit(self, event: Event) -> bool:
        """Emit an event to registered handlers.

        Args:
            event: Event to emit

        Returns:
            True if event was handled, False otherwise
        """
        if event.event_type not in self._event_handlers:
            return False

        for handler in self._event_handlers[event.event_type]:
            handler(event)

        return True

    def handle_event(self, event: Event) -> bool:
        """Handle an event for this component.

        Args:
            event: Event to handle

        Returns:
            True if event was handled, False to propagate
        """
        if not self.enabled or not self.visible:
            return False

        # Check if event is within bounds
        abs_pos = self.absolute_position
        local_x = event.x - abs_pos.x
        local_y = event.y - abs_pos.y

        if not (0 <= local_x < self.size.width and 0 <= local_y < self.size.height):
            return False

        return self.emit(event)

    @abstractmethod
    def render(self, surface: Any) -> None:
        """Render the component to a surface.

        Args:
            surface: Surface to render to (implementation-specific)
        """
        pass

    def update(self, delta_time: float) -> None:
        """Update component state.

        Args:
            delta_time: Time elapsed since last update in seconds
        """
        pass


class Container(Component):
    """Base class for components that can contain other components.

    Containers manage child components, handle their layout,
    and propagate events to children.
    """

    def __init__(
        self,
        position: Optional[Position] = None,
        size: Optional[Size] = None,
        visible: bool = True,
        enabled: bool = True,
    ):
        """Initialize the container.

        Args:
            position: Container position
            size: Container size
            visible: Whether the container is visible
            enabled: Whether the container is enabled
        """
        super().__init__(position, size, visible, enabled)
        self.children: List[Component] = []

    def add(self, component: Component, **layout_params) -> None:
        """Add a child component to this container.

        Args:
            component: Component to add
            **layout_params: Additional layout parameters (implementation-specific)
        """
        if component.parent is not None:
            raise ValueError("Component already has a parent")

        component.parent = self
        self.children.append(component)

    def remove(self, component: Component) -> None:
        """Remove a child component from this container.

        Args:
            component: Component to remove
        """
        if component in self.children:
            component.parent = None
            self.children.remove(component)

    def clear(self) -> None:
        """Remove all child components."""
        for child in self.children[:]:
            self.remove(child)

    def handle_event(self, event: Event) -> bool:
        """Handle events, propagating to children.

        Args:
            event: Event to handle

        Returns:
            True if event was handled
        """
        if not self.enabled or not self.visible:
            return False

        # Try children first (reverse order for proper z-order)
        for child in reversed(self.children):
            if child.handle_event(event):
                return True

        # Then try self
        return super().handle_event(event)

    def render(self, surface: Any) -> None:
        """Render container and all children.

        Args:
            surface: Surface to render to
        """
        if not self.visible:
            return

        # Render children
        for child in self.children:
            child.render(surface)

    def update(self, delta_time: float) -> None:
        """Update container and all children.

        Args:
            delta_time: Time elapsed since last update
        """
        super().update(delta_time)

        for child in self.children:
            child.update(delta_time)
