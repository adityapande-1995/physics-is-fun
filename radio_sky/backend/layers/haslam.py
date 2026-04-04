"""
Haslam 408 MHz all-sky map layer.

Downloads the Remazeilles et al. 2014 reprocessed Haslam map from NASA LAMBDA
(~3 MB FITS file), then projects the currently-visible sky onto an azimuthal
equidistant canvas centred on Bangalore's zenith.

Projection convention (matches sky.js exactly):
  - Centre of image = zenith
  - North = up, East = left  (standard sky orientation looking up)
  - r = r_max * (90 - alt) / 90  →  horizon at edge, zenith at centre
  - az = arctan2(-dx, dy)         →  North=0°, East=90°, South=180°, West=270°

The projected image is cached for CACHE_SECONDS so the slow coordinate
transform only runs once every 5 minutes.
"""
import io
import base64
import time as time_module
from pathlib import Path
from threading import Lock

import numpy as np
import requests

DATA_DIR = Path(__file__).parent.parent.parent / "data"
CACHE_PATH = DATA_DIR / "haslam408.fits"

HASLAM_URL = (
    "https://lambda.gsfc.nasa.gov/data/foregrounds/haslam_2014/"
    "haslam408_dsds_Remazeilles2014.fits"
)

_haslam_map = None
_load_lock = Lock()

_cache = {"image": None, "ts": 0.0}
CACHE_SECONDS = 300  # 5-minute cache


def _load_map():
    global _haslam_map
    if _haslam_map is not None:
        return _haslam_map
    with _load_lock:
        if _haslam_map is not None:
            return _haslam_map

        import healpy as hp

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not CACHE_PATH.exists():
            print(f"[haslam] Downloading 408 MHz map (~3 MB) → {CACHE_PATH}")
            r = requests.get(HASLAM_URL, stream=True, timeout=120)
            r.raise_for_status()
            with open(CACHE_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=65536):
                    f.write(chunk)
            print("[haslam] Download complete.")

        _haslam_map = hp.read_map(str(CACHE_PATH), verbose=False)
        print(f"[haslam] Loaded map, NSIDE={hp.get_nside(_haslam_map)}")
        return _haslam_map


def project_sky(sky, size=600):
    """
    Project the Haslam map onto an azimuthal equidistant canvas.
    Returns a base64-encoded RGBA PNG string, or None on failure.
    Result is cached for CACHE_SECONDS.
    """
    now = time_module.time()
    if _cache["image"] is not None and (now - _cache["ts"]) < CACHE_SECONDS:
        return _cache["image"]

    try:
        import healpy as hp
        from astropy.coordinates import SkyCoord
        import astropy.units as u
        from PIL import Image
        import matplotlib.cm as cm
    except ImportError as e:
        print(f"[haslam] Missing dependency: {e}")
        return None

    haslam = _load_map()
    nside = hp.get_nside(haslam)

    t = sky.now()
    frame = sky.altaz_frame(t)

    cx = cy = size // 2
    r_max = size // 2 - 30  # matches JS canvas r_max

    # Build pixel grid: (IY, IX) → (row, col)
    cols = np.arange(size)
    rows = np.arange(size)
    IY, IX = np.meshgrid(rows, cols, indexing="ij")

    # Normalised offsets: +dx = right (west), +dy = up (north)
    dx = (IX - cx) / r_max
    dy = (cy - IY) / r_max
    r = np.sqrt(dx**2 + dy**2)

    mask = r <= 1.0  # pixels inside the horizon circle

    alt_deg = 90.0 * (1.0 - r[mask])
    # North=0°, East=90° (east is LEFT in sky view → -dx direction)
    az_deg = (np.degrees(np.arctan2(-dx[mask], dy[mask])) + 360.0) % 360.0

    print(f"[haslam] Transforming {mask.sum()} sky pixels (this takes a few seconds)…")
    coords = SkyCoord(alt=alt_deg * u.deg, az=az_deg * u.deg, frame=frame)
    # Haslam FITS is stored in GALACTIC coordinates — must convert before lookup
    galactic = coords.icrs.galactic
    theta = np.radians(90.0 - galactic.b.deg)   # galactic colatitude
    phi   = np.radians(galactic.l.deg) % (2 * np.pi)
    pix_idx = hp.ang2pix(nside, theta, phi)

    output = np.full((size, size), np.nan)
    output[mask] = haslam[pix_idx]

    valid = output[~np.isnan(output)]
    vmin = max(np.percentile(valid, 2), 1.0)
    vmax = np.percentile(valid, 99.5)

    log_out = np.log10(np.clip(output, vmin, vmax))
    normed = (log_out - np.log10(vmin)) / (np.log10(vmax) - np.log10(vmin))
    normed = np.nan_to_num(np.clip(normed, 0.0, 1.0))

    colored = cm.inferno(normed)  # (H, W, 4) float32
    rgba = (colored * 255).astype(np.uint8)
    rgba[..., 3] = np.where(mask, 200, 0).astype(np.uint8)  # transparent outside

    img = Image.fromarray(rgba, "RGBA")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode()

    _cache["image"] = encoded
    _cache["ts"] = now
    print("[haslam] Projection complete, cached.")
    return encoded
