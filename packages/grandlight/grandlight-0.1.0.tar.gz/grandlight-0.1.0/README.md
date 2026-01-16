# GrandLight ✨

> A modern Python GUI library featuring glassmorphism design aesthetics

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

**GrandLight** is a revolutionary GUI library that brings the elegant glassmorphism design trend to Python applications. With its frosted glass effects, transparency layers, and modern aesthetics, GrandLight enables developers to create stunning user interfaces that feel premium and contemporary.

## ✨ Features

- **🎨 Glassmorphism Design**: Built-in components with frosted glass aesthetics
- **🌈 Transparency Effects**: Beautiful blur and transparency layers
- **🎭 Modern UI Components**: Buttons, panels, windows, and more with glassmorphic styling
- **🚀 Easy to Use**: Simple, intuitive API for rapid development
- **🎯 Customizable**: Full control over colors, blur intensity, and transparency
- **⚡ Performance Optimized**: Efficient rendering for smooth animations
- **🔧 Extensible**: Build your own custom glassmorphic components

## 🚀 Quick Start

### Installation

```bash
pip install grandlight
```

### Basic Usage

```python
from grandlight import Window, GlassPanel, GlassButton

# Create a glassmorphic window
window = Window(title="My Glassmorphic App", size=(800, 600))

# Add a glass panel
panel = GlassPanel(
    blur=20,
    opacity=0.7,
    background_color=(255, 255, 255, 100)
)
window.add(panel)

# Add a glass button
button = GlassButton(
    text="Click Me",
    blur=15,
    opacity=0.8
)
panel.add(button)

# Run the application
window.run()
```

## 📚 Core Concepts

### Glassmorphism Properties

GrandLight components support the following glassmorphism properties:

- **`blur`**: Intensity of the backdrop blur effect (0-100)
- **`opacity`**: Transparency level (0.0-1.0)
- **`background_color`**: RGBA color tuple for the glass effect
- **`border_color`**: Optional border color for enhanced depth
- **`shadow`**: Soft shadow for floating effect

### Component Hierarchy

```
Window
  ├── GlassPanel
  │     ├── GlassButton
  │     ├── GlassLabel
  │     └── GlassInput
  ├── GlassNavBar
  └── GlassDialog
```

## 🎨 Styling Tips

For the best glassmorphism effects:

1. **Use subtle backgrounds**: Light gradients or blurred images work best
2. **Layer transparencies**: Stack multiple glass panels for depth
3. **Consistent blur values**: Keep blur intensity similar across components
4. **Soft colors**: Pastel or muted tones enhance the glass aesthetic
5. **Minimal borders**: Thin, light borders complement the frosted look

## 📖 Documentation

For comprehensive documentation, visit our [GitHub repository](https://github.com/rheehose/grandlight).

## 🛠️ Requirements

- Python 3.8 or higher
- Pillow (PIL) for image processing
- NumPy for efficient array operations

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Rheehose (Rhee Creative)**  
Copyright © 2008-2026

## 🌟 Acknowledgments

Special thanks to the design community for inspiring the glassmorphism trend and making GUI development more beautiful.

## 📮 Contact

- GitHub: [@rheehose](https://github.com/rheehose)
- Issues: [Report a bug](https://github.com/rheehose/grandlight/issues)

---

**Made with ❤️ by Rhee Creative**
