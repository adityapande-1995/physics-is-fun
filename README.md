# Physics is Fun: Black Hole Visualizations

This project contains two Python simulations that visualize the fascinating physics of black holes.

## Features

1.  **Real-time Gravitational Lensing (`black_hole_raytracing.py`)**
    *   A GPU-accelerated simulation showing how a black hole bends the light from a background starfield.
    *   Uses `pygame` for the display window and `moderngl` for high-performance calculations on the GPU (via GLSL shaders).
    *   Interactive camera controls allow you to orbit the black hole and zoom in and out.

2.  **Photon Geodesics Side-View (`sideview.py`)**
    *   A 2D simulation comparing the paths of photons (light particles) around two types of black holes in a split-screen view.
    *   **Top View:** A static, non-rotating **Schwarzschild** black hole.
    *   **Bottom View:** A rotating **Kerr** black hole, which demonstrates the "frame-dragging" effect on nearby spacetime.
    *   You can interactively change the mass and spin of the black holes to see how it affects the photon paths.

## Getting Started

Follow these instructions to get the simulations running on your local machine.

### 1. Clone the Repository

First, clone this repository to your computer:

```bash
git clone <URL_OF_THIS_REPOSITORY>
cd physics-is-fun
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to keep project dependencies isolated.

**On macOS / Linux:**

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

**On Windows:**

```bash
# Create the virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate
```

### 3. Install Dependencies

With your virtual environment activated, install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

Make sure your virtual environment is still activated before running the scripts.

### Gravitational Lensing Demo

This script will automatically download a galaxy background image (`galaxy.jpg`) on its first run.

```bash
python black_hole_raytracing.py
```

A `pygame` window will open displaying the black hole against a starfield.

**Controls:**
*   **Move Mouse:** Orbit the camera around the black hole.
*   **Scroll Wheel:** Zoom in and out.

### Photon Path Comparison

```bash
python sideview.py
```

A `pygame` window will open with a split-screen view. The top half shows the Schwarzschild black hole, and the bottom shows the Kerr black hole.

**Controls:**
*   **Up/Down Arrows:** Increase/Decrease the mass of the black holes.
*   **Left/Right Arrows:** Increase/Decrease the spin of the Kerr black hole.
*   **'R' Key:** Reset the simulation and clear photon paths.
*   **'H' Key:** Toggle the visibility of the photon sphere radius.

```