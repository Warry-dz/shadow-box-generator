# Shadow Box Generator
# Inverse Ray-Tracing Shadow Box Generator

A custom Python-based computational geometry engine designed to calculate and generate precise hole patterns on the four interior walls of a 3D box. When a single point light source is placed inside, the light passing through these holes projects a target 2D image onto a surrounding external surface.

This project is built from scratch with absolute mathematical precision—avoiding heavy external CAD modeling frameworks for the core physics simulation.

---

## 🚀 Project Features

* **Manual Inverse Ray Tracing Engine:** Calculates exact 3D parametric line intersections ($P = L + t \cdot D$) to map target image pixels back to box wall coordinates.
* **Modular Architecture:** Clean separation of concerns between physical configuration, image preprocessing, and physics calculations.
* **Adaptive Brush Sizing:** Implements dynamic neighborhood hole-punching to eliminate aliasing and prevent gaps/white lines caused by ray divergence as distance increases.
* **OpenCV Image Integration:** Automatically processes input images into high-contrast binary masks.

---

## 📁 Project Structure

```text
sh_lamp/
│
├── inputs/
│   └── im1.png              # Target 2D image to project
├── outputs/
│   └── 2d_masks/            # Generated PNG masks for the 4 box walls
├── src/
│   ├── config.py            # Physical box dimensions, resolution, and light position
│   ├── image_processor.py   # Loads images and generates binary masks
│   └── ray_tracer.py        # Core ray-tracing engine and wall mapping logic
│
├── main.py                  # Main orchestration script
└── README.md                # Project documentation


📐 How It Works (The Physics & Math)
Image Masking: The engine loads a target image and converts it into a binary black-and-white matrix, where black pixels represent the light-emitting points of your design.

Back-Propagation (Inverse Rays): For every target pixel, the algorithm casts an inverse ray from the target wall, through the box interior, straight back to the internal light source position.

Wall Intersection: Using analytical geometry, it tests which of the four side walls (top, bottom, left, right) the ray intersects first by solving parametric line equations.

Adaptive Matrix Mapping: The 3D hit point is mapped into 2D row/column matrix indices for that specific wall. An adaptive dynamic brush size ensures solid, gap-free hole patterns even where rays diverge near the base.