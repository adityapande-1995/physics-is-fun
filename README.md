# Physics is Fun: Black Hole Visualizations

This project contains two Python simulations that visualize the fascinating physics of black holes.

## Previews

<!-- Add GIFs to the previews/ folder and link them here -->

## Projects

### [Black Hole Simulations](black_hole/)

1.  **Real-time Gravitational Lensing (`black_hole/black_hole_raytracing.py`)**
    *   A GPU-accelerated simulation showing how a black hole bends the light from a background starfield.
    *   Uses `pygame` for the display window and `moderngl` for high-performance calculations on the GPU (via GLSL shaders).
    *   Interactive camera controls allow you to orbit the black hole and zoom in and out.

2.  **Photon Geodesics Side-View (`black_hole/sideview.py`)**
    *   A 2D simulation comparing the paths of photons (light particles) around two types of black holes in a split-screen view.
    *   **Top View:** A static, non-rotating **Schwarzschild** black hole.
    *   **Bottom View:** A rotating **Kerr** black hole, which demonstrates the "frame-dragging" effect on nearby spacetime.
    *   You can interactively change the mass and spin of the black holes to see how it affects the photon paths.

## Getting Started

Follow these instructions to get the simulations running on your local machine.

### 1. Clone the Repository

```bash
git clone git@github.com:adityapande-1995/physics-is-fun.git
cd physics-is-fun
```

### 2. Create and Activate a Virtual Environment

**On macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

Make sure your virtual environment is still activated before running the scripts.

### Gravitational Lensing Demo

This script will automatically download a galaxy background image (`galaxy.jpg`) on its first run.

```bash
python black_hole/black_hole_raytracing.py
```

A `pygame` window will open displaying the black hole against a starfield.

**Controls:**
*   **Move Mouse:** Orbit the camera around the black hole.
*   **Scroll Wheel:** Zoom in and out.

### Photon Path Comparison

```bash
python black_hole/sideview.py
```

A `pygame` window will open with a split-screen view. The top half shows the Schwarzschild black hole, and the bottom shows the Kerr black hole.

**Controls:**
*   **Up/Down Arrows:** Increase/Decrease the mass of the black holes.
*   **Left/Right Arrows:** Increase/Decrease the spin of the Kerr black hole.
*   **'R' Key:** Reset the simulation and clear photon paths.
*   **'H' Key:** Toggle the visibility of the photon sphere radius.
