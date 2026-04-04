"""
Bright naked-eye stars as orientation anchors.
These give the user real optical landmarks to cross-reference against the radio map.
Visible magnitude limit set to ~2.0 — stars bright enough to see even from
light-polluted Bangalore skies.
"""

# (name, ra_deg, dec_deg, magnitude, constellation note)
BRIGHT_STARS = [
    ("Sirius",      101.2875, -16.7161, -1.46, "α CMa — brightest star in the sky"),
    ("Canopus",      95.9879, -52.6957, -0.74, "α Car — dominant in the south"),
    ("Arcturus",    213.9153,  19.1822, -0.05, "α Boo — orange giant, high in spring"),
    ("Vega",        279.2347,  38.7837,  0.03, "α Lyr — overhead in summer"),
    ("Capella",      79.1723,  45.9980,  0.08, "α Aur — winter hexagon"),
    ("Rigel",        78.6345,  -8.2016,  0.13, "β Ori — blue supergiant in Orion"),
    ("Procyon",     114.8255,   5.2250,  0.34, "α CMi — winter triangle"),
    ("Betelgeuse",   88.7929,   7.4071,  0.58, "α Ori — red supergiant, Orion's shoulder"),
    ("Achernar",     24.4288, -57.2367,  0.46, "α Eri — far south, barely visible"),
    ("Hadar",       210.9559, -60.3730,  0.61, "β Cen — southern pointer star"),
    ("Altair",      297.6958,   8.8683,  0.76, "α Aql — summer triangle"),
    ("Aldebaran",    68.9802,  16.5093,  0.87, "α Tau — red eye of the Bull"),
    ("Antares",     247.3519, -26.4320,  1.06, "α Sco — red rival of Mars, near galactic centre"),
    ("Spica",       201.2983,  -11.1613, 0.98, "α Vir — blue-white, spring sky"),
    ("Pollux",      116.3289,  28.0262,  1.16, "β Gem — brightest twin"),
    ("Fomalhaut",   344.4127, -29.6223,  1.16, "α PsA — lonely autumn star in the south"),
    ("Deneb",       310.3580,  45.2803,  1.25, "α Cyg — summer triangle, supergiant"),
    ("Mimosa",      191.9303, -59.6888,  1.25, "β Cru — Southern Cross"),
    ("Regulus",     152.0930,  11.9672,  1.36, "α Leo — heart of the Lion"),
    ("Adhara",      104.6564, -28.9722,  1.50, "ε CMa — below Sirius"),
    ("Castor",      113.6495,  31.8883,  1.58, "α Gem — double star"),
    ("Shaula",      263.4022, -37.1038,  1.62, "λ Sco — tail of Scorpius, near galactic plane"),
    ("Bellatrix",    81.2828,   6.3497,  1.64, "γ Ori — Orion's shoulder"),
    ("Elnath",       81.5728,  28.6074,  1.68, "β Tau — tip of the Bull's horn"),
    ("Miaplacidus", 138.3000, -69.7172,  1.68, "β Car — south circumpolar"),
    ("Alnilam",      84.0534,  -1.2019,  1.70, "ε Ori — middle star of Orion's Belt"),
    ("Alnitak",      85.1897,  -1.9426,  1.77, "ζ Ori — eastern star of Orion's Belt"),
    ("Mintaka",      83.0016,  -0.2991,  2.23, "δ Ori — western star of Orion's Belt"),
]


# ── Constellation stick figures ───────────────────────────────────────────────
# Each entry: (name, [ (ra1,dec1, ra2,dec2), ... ])  — line segments in J2000

CONSTELLATIONS = {
    "Orion": [
        # Belt: Mintaka – Alnilam – Alnitak
        (83.0016, -0.2991,  84.0534, -1.2019),
        (84.0534, -1.2019,  85.1897, -1.9426),
        # Shoulders: Betelgeuse – Bellatrix
        (88.7929,  7.4071,  81.2828,  6.3497),
        # Betelgeuse down to belt
        (88.7929,  7.4071,  85.1897, -1.9426),
        # Bellatrix down to belt
        (81.2828,  6.3497,  83.0016, -0.2991),
        # Feet: Rigel and Saiph
        (78.6345, -8.2016,  83.0016, -0.2991),
        (86.9391, -9.6697,  85.1897, -1.9426),
    ],
    "Ursa Major": [
        # Big Dipper bowl
        (165.9320, 61.7511, 178.4577, 53.6948),
        (178.4577, 53.6948, 183.8565, 57.0325),
        (183.8565, 57.0325, 193.5073, 55.9598),
        (193.5073, 55.9598, 165.9320, 61.7511),
        # Handle
        (193.5073, 55.9598, 200.9814, 54.9254),
        (200.9814, 54.9254, 206.8854, 49.3133),
        (206.8854, 49.3133, 210.9563, 47.1568),
    ],
    "Scorpius": [
        # Head: Graffias – Dschubba – Acrab
        (241.3593, -19.8054, 240.0833, -22.6217),
        (240.0833, -22.6217, 244.9350, -15.7250),
        # Body down to Antares
        (240.0833, -22.6217, 247.3519, -26.4320),
        # Antares to tail
        (247.3519, -26.4320, 252.9675, -34.2928),
        (252.9675, -34.2928, 253.0839, -37.1038),
        (253.0839, -37.1038, 263.4022, -37.1038),
        # Stinger
        (263.4022, -37.1038, 264.3297, -43.0),
    ],
    "Crux": [
        # Southern Cross — vertical
        (183.7863, -57.1130, 187.7912, -63.0990),
        # horizontal
        (186.6497, -59.5410, 191.9303, -59.6888),
    ],
    "Cassiopeia": [
        # W shape
        (6.8238,  56.5373,  14.1771,  60.7167),
        (14.1771,  60.7167,  28.5988,  63.6700),
        (28.5988,  63.6700,  9.2429,  59.1498),
        (9.2429,  59.1498,  21.4538,  68.8842),
    ],
    "Gemini": [
        # Castor and Pollux heads
        (113.6495, 31.8883, 116.3289, 28.0262),
        # Bodies down
        (113.6495, 31.8883, 100.9831, 25.1312),
        (116.3289, 28.0262, 106.0270, 20.5705),
        # Feet
        (100.9831, 25.1312,  99.4280, 16.5458),
        (106.0270, 20.5705,  101.3223, 12.8958),
    ],
    "Leo": [
        # Sickle (head)
        (152.0930, 11.9672, 154.9930, 19.8421),
        (154.9930, 19.8421, 148.1909, 26.0071),
        (148.1909, 26.0071, 146.4627, 23.7742),
        (146.4627, 23.7742, 152.0930, 11.9672),
        # Body to tail (Denebola)
        (152.0930, 11.9672, 168.5274, 15.4297),
        (168.5274, 15.4297, 177.2649, 14.5720),
    ],
    "Centaurus": [
        # Alpha and Beta Cen (pointer stars to Southern Cross)
        (219.9021, -60.8340, 210.9559, -60.3730),
        (210.9559, -60.3730, 201.3651, -43.0192),
    ],
    "Canis Major": [
        # Sirius at top, body
        (101.2875, -16.7161, 104.6564, -28.9722),  # Sirius to Adhara
        (101.2875, -16.7161,  98.6578, -23.8333),  # Sirius to Wezen
        (104.6564, -28.9722,  98.6578, -23.8333),
    ],
}


def get_constellations(sky):
    """
    Return constellation stick-figure segments, each projected to alt/az.
    Only segments where BOTH endpoints are above the horizon are included.
    """
    result = []
    for name, segments in CONSTELLATIONS.items():
        lines = []
        for ra1, dec1, ra2, dec2 in segments:
            alt1, az1 = sky.to_altaz(ra1, dec1)
            alt2, az2 = sky.to_altaz(ra2, dec2)
            if alt1 >= 3.0 and alt2 >= 3.0:
                lines.append({
                    "alt1": round(alt1, 2), "az1": round(az1, 2),
                    "alt2": round(alt2, 2), "az2": round(az2, 2),
                })
        if lines:
            result.append({"name": name, "lines": lines})
    return result


def get_moon(sky):
    """Return Moon position, phase, and illumination."""
    from astropy.coordinates import get_body
    from astropy.time import Time

    t = sky.now()
    moon = get_body("moon", t, sky.location)
    alt, az = sky.to_altaz(float(moon.ra.deg), float(moon.dec.deg), t)

    # Phase angle approximation via elongation from Sun
    from astropy.coordinates import get_sun
    sun = get_sun(t)
    elongation = float(moon.separation(sun).deg)
    illumination = round((1 - abs(elongation - 180) / 180) * 100)
    # Simple phase name
    if illumination > 95:
        phase = "Full Moon"
    elif illumination > 60:
        phase = "Gibbous"
    elif illumination > 35:
        phase = "Quarter"
    elif illumination > 5:
        phase = "Crescent"
    else:
        phase = "New Moon"

    return {
        "ra": round(float(moon.ra.deg), 4),
        "dec": round(float(moon.dec.deg), 4),
        "alt": round(alt, 2),
        "az": round(az, 2),
        "visible": alt >= 3.0,
        "illumination": illumination,
        "phase": phase,
        "elongation": round(elongation, 1),
    }


def get_bright_stars(sky, min_alt=5.0):
    results = []
    for name, ra, dec, mag, note in BRIGHT_STARS:
        alt, az = sky.to_altaz(ra, dec)
        if alt >= min_alt:
            results.append({
                "name": name,
                "ra": ra,
                "dec": dec,
                "mag": mag,
                "note": note,
                "alt": round(alt, 2),
                "az": round(az, 2),
                "visible": True,
            })
    return results
