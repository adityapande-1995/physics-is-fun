"""
Flask backend for the Radio Sky dashboard.

Endpoints:
  GET /            → serves frontend/index.html
  GET /api/sky     → current sky state (zenith, LST, UTC)
  GET /api/galactic_plane  → alt/az points for b=0 galactic plane
  GET /api/targets → notable radio sources with current alt/az
  GET /api/haslam  → Haslam 408 MHz projected sky image (base64 PNG, 5-min cache)

Run with:
  cd radio_sky
  python backend/server.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from sky import BangaloreSky
from layers.haslam import project_sky
from layers.targets import get_targets_with_altaz
from layers.stars import get_bright_stars, get_constellations, get_moon

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR))
CORS(app)

sky = BangaloreSky()


# ── Frontend ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# ── API ───────────────────────────────────────────────────────────────────────

@app.route("/api/sky")
def api_sky():
    return jsonify(sky.sky_info())


@app.route("/api/galactic_plane")
def api_galactic_plane():
    return jsonify({"points": sky.get_galactic_plane()})


@app.route("/api/targets")
def api_targets():
    return jsonify({"targets": get_targets_with_altaz(sky)})


@app.route("/api/stars")
def api_stars():
    return jsonify({"stars": get_bright_stars(sky)})


@app.route("/api/constellations")
def api_constellations():
    return jsonify({"constellations": get_constellations(sky)})


@app.route("/api/moon")
def api_moon():
    return jsonify(get_moon(sky))


@app.route("/api/haslam")
def api_haslam():
    try:
        img = project_sky(sky)
        if img:
            return jsonify({"status": "ok", "image": img})
        return jsonify({"status": "error", "message": "Projection failed"}), 500
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


if __name__ == "__main__":
    print("Starting Radio Sky backend on http://localhost:5001")
    app.run(debug=False, port=5001, threaded=True)
