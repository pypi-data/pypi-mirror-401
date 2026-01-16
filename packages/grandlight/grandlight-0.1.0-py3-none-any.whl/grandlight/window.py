"""
Window management for GrandLight applications.

This module provides the main Window class that serves as the root
container for all UI components.
"""

from typing import Optional, Tuple, List
from .core import Container, Position, Size


class Window(Container):
    """Main application window with glassmorphic support.

    The Window is the root container for all UI components in a GrandLight
    application. It manages the rendering loop, event dispatching, and
    provides a beautiful glassmorphic canvas for UI elements.

    Example:
        >>> window = Window(
        ...     title="My App",
        ...     size=Size(800, 600),
        ...     background_gradient=["#667eea", "#764ba2"]
        ... )
        >>> window.add(my_panel)
        >>> window.run()
    """

    def __init__(
        self,
        title: str = "GrandLight Application",
        size: Optional[Size] = None,
        position: Optional[Position] = None,
        background_color: Optional[Tuple[int, int, int]] = None,
        background_gradient: Optional[List[str]] = None,
        background_image: Optional[str] = None,
        resizable: bool = True,
        fullscreen: bool = False,
        vsync: bool = True,
        fps: int = 60,
    ):
        """Initialize the window.

        Args:
            title: Window title
            size: Window size (default: 800x600)
            position: Window position (default: centered)
            background_color: Solid background color RGB
            background_gradient: List of color stops for gradient background
            background_image: Path to background image
            resizable: Whether window can be resized
            fullscreen: Start in fullscreen mode
            vsync: Enable vertical sync
            fps: Target frames per second
        """
        if size is None:
            size = Size(800, 600)

        super().__init__(position or Position(0, 0), size, True, True)

        self.title = title
        self.background_color = background_color or (240, 240, 245)
        self.background_gradient = background_gradient
        self.background_image = background_image
        self.resizable = resizable
        self.fullscreen = fullscreen
        self.vsync = vsync
        self.fps = fps

        # Window state
        self._running = False
        self._frame_count = 0
        self._delta_time = 0.0

    def run(self) -> None:
        """Start the main event loop.

        This method enters the main loop, handling events, updating
        components, and rendering frames until the window is closed.

        Example:
            >>> window = Window(title="My App")
            >>> window.add(my_ui)
            >>> window.run()  # Blocks until window is closed
        """
        self._running = True
        self._setup()

        import time

        last_time = time.time()

        while self._running:
            # Calculate delta time
            current_time = time.time()
            self._delta_time = current_time - last_time
            last_time = current_time

            # Handle events
            self._process_events()

            # Update components
            self.update(self._delta_time)

            # Render frame
            self._render_frame()

            self._frame_count += 1

            # Frame rate limiting
            if self.fps > 0:
                time.sleep(max(0, (1.0 / self.fps) - self._delta_time))

        self._cleanup()

    def close(self) -> None:
        """Close the window and exit the main loop."""
        self._running = False

    def _setup(self) -> None:
        """Initialize the rendering backend.

        This is called once before the main loop starts.
        In a full implementation, this would initialize OpenGL/Cairo/etc.
        """
        print(f"╔{'═' * 60}╗")
        print(f"║ {self.title:^58} ║")
        print(f"╠{'═' * 60}╣")
        print("║ GrandLight v0.1.0 - Glassmorphism GUI Library            ║")
        w_str = f"Window: {self.size.width}x{self.size.height} @ {self.fps} FPS"
        print(f"║ {w_str}{' ' * (58 - len(w_str))}║")
        print(f"╚{'═' * 60}╝")
        print("\nPress Ctrl+C to exit...\n")

    def _cleanup(self) -> None:
        """Clean up resources before closing.

        This is called once after the main loop exits.
        """
        print("\nWindow closed.")

    def _process_events(self) -> None:
        """Process input events.

        In a full implementation, this would poll keyboard, mouse,
        and window events from the OS/windowing system.
        """
        # Placeholder for event processing
        # Real implementation would use pygame/glfw/qt for events
        pass

    def _render_frame(self) -> None:
        """Render a single frame.

        This method renders the background and all child components.
        """
        # In a real implementation:
        # 1. Clear the framebuffer
        # 2. Render background (solid/gradient/image)
        # 3. Render all components with glass effects
        # 4. Swap buffers

        # Placeholder rendering
        self.render(None)

    def render(self, surface: any = None) -> None:
        """Render the window and all components.

        Args:
            surface: Rendering surface (implementation-specific)
        """
        # Render background
        self._render_background()

        # Render all child components
        super().render(surface)

    def _render_background(self) -> None:
        """Render the window background.

        Supports solid colors, gradients, and images.
        """
        # Placeholder for background rendering
        if self.background_gradient:
            # Would render gradient
            pass
        elif self.background_image:
            # Would load and render image
            pass
        else:
            # Would fill with solid color
            pass

    def set_background_gradient(self, colors: List[str]) -> None:
        """Set a gradient background.

        Args:
            colors: List of hex color strings

        Example:
            >>> window.set_background_gradient(["#667eea", "#764ba2"])
        """
        self.background_gradient = colors

    def set_background_image(self, image_path: str, blur: int = 0) -> None:
        """Set an image background.

        Args:
            image_path: Path to background image
            blur: Optional blur amount (great for glassmorphism!)

        Example:
            >>> window.set_background_image("bg.jpg", blur=10)
        """
        self.background_image = image_path

    def center_component(self, component) -> None:
        """Center a component in the window.

        Args:
            component: Component to center

        Example:
            >>> panel = GlassPanel(size=Size(400, 300))
            >>> window.add(panel)
            >>> window.center_component(panel)
        """
        component.position = Position(
            (self.size.width - component.size.width) // 2,
            (self.size.height - component.size.height) // 2,
        )

    @property
    def delta_time(self) -> float:
        """Get the time elapsed since last frame in seconds."""
        return self._delta_time

    @property
    def frame_count(self) -> int:
        """Get the total number of frames rendered."""
        return self._frame_count

    @property
    def current_fps(self) -> float:
        """Get the current FPS based on delta time."""
        return 1.0 / self._delta_time if self._delta_time > 0 else 0
