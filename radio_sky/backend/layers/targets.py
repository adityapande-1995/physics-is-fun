"""
Curated list of radio sources that are invisible or faint optically from Bangalore
but bright in the radio sky. These are what we want the user to eventually "discover"
by correlating the radio sky with their optical view.
"""
from astropy.coordinates import get_sun

# Flux at 408 MHz in Jy unless noted. Positions in J2000 RA/Dec degrees.
TARGETS = [
    {
        "id": "sgr_a_star",
        "name": "Sagittarius A*",
        "ra": 266.4168,
        "dec": -29.0078,
        "flux_jy": 1000,
        "freq_mhz": 408,
        "type": "Galactic Center / SMBH",
        "color": "#ff4444",
        "why_radio": (
            "The supermassive black hole at the centre of our galaxy — 4 million solar masses "
            "compressed into a region smaller than our solar system. Completely invisible optically: "
            "30 magnitudes of interstellar dust absorb every photon of light. In radio, the surrounding "
            "synchrotron-emitting plasma and the compact source itself shine brightly across all frequencies."
        ),
        "from_bangalore": (
            "From latitude 13°N, Sgr A* transits at 74° altitude — almost directly overhead. "
            "You are looking straight through the dusty heart of the Milky Way. "
            "This is the object that will be completely invisible on any optical night from Bangalore "
            "yet dominates the radio sky overhead."
        ),
    },
    {
        "id": "cas_a",
        "name": "Cassiopeia A",
        "ra": 350.8500,
        "dec": 58.8150,
        "flux_jy": 2720,
        "freq_mhz": 408,
        "type": "Supernova Remnant",
        "color": "#ff8800",
        "why_radio": (
            "The brightest radio source in the sky outside the solar system. The remnant of a stellar "
            "explosion around 1680 AD — no European astronomer recorded the supernova itself, likely "
            "because the progenitor star was shrouded in circumstellar dust. Today the expanding shell "
            "of superheated gas produces intense synchrotron radiation. Its flux is so stable it's "
            "used as a primary calibration source for radio telescopes worldwide."
        ),
        "from_bangalore": (
            "Reaches a maximum altitude of ~44° from Bangalore — not circumpolar, but well visible. "
            "Brightest point source in the radio sky. An exploded star we can't see with our eyes "
            "but would outshine everything in a radio 'photograph'."
        ),
    },
    {
        "id": "cyg_a",
        "name": "Cygnus A",
        "ra": 299.8683,
        "dec": 40.7339,
        "flux_jy": 1590,
        "freq_mhz": 408,
        "type": "Radio Galaxy / AGN",
        "color": "#4488ff",
        "why_radio": (
            "A galaxy 700 million light-years away whose central black hole is launching twin jets of "
            "plasma at near-light-speed. In an optical image it looks like a faint smudge. "
            "In radio, the jets inflate two enormous lobes — each 100,000 light-years across — "
            "that dominate the sky. The radio power output exceeds the entire Milky Way's stellar "
            "luminosity by a factor of 10 million."
        ),
        "from_bangalore": (
            "Max altitude ~63° from Bangalore. The archetypal radio galaxy — the object that in the "
            "1950s convinced astronomers that a whole new class of violent, non-thermal phenomena "
            "existed in the universe, invisible to optical telescopes."
        ),
    },
    {
        "id": "vir_a",
        "name": "Virgo A  (M87)",
        "ra": 187.7059,
        "dec": 12.3911,
        "flux_jy": 861,
        "freq_mhz": 408,
        "type": "Radio Galaxy / Jet Source",
        "color": "#44ffaa",
        "why_radio": (
            "The galaxy whose 6.5-billion-solar-mass black hole was directly imaged by the Event "
            "Horizon Telescope in 2019. A relativistic plasma jet 5,000 light-years long erupts "
            "from the nucleus — detectable in radio across the full extent of the jet, while optically "
            "only the bright core and a faint knot are visible. The radio structure reveals the "
            "mechanics of jet launching that optical images entirely hide."
        ),
        "from_bangalore": (
            "Transits at 77° altitude — nearly overhead from Bangalore. On any given night you are "
            "almost directly below the site of the first black hole photograph, seeing nothing "
            "with the naked eye, while it blazes at radio wavelengths."
        ),
    },
    {
        "id": "cen_a",
        "name": "Centaurus A  (NGC 5128)",
        "ra": 201.3651,
        "dec": -43.0192,
        "flux_jy": 1370,
        "freq_mhz": 408,
        "type": "Radio Galaxy",
        "color": "#ff44aa",
        "why_radio": (
            "The nearest radio galaxy at 13 million light-years. Its radio jets extend 1.4 million "
            "light-years — larger than our entire galaxy — but the central engine is buried inside "
            "a thick dust lane that cuts the optical image in two. The jets are powered by a "
            "55-million-solar-mass black hole that is actively accreting material. "
            "A prime target for understanding how jets form."
        ),
        "from_bangalore": (
            "Reaches 60° altitude from Bangalore — one of the best-placed major radio sources "
            "in the southern sky for Indian latitudes. The closest example of an active galactic "
            "nucleus, and the radio galaxy with the most detailed resolved structure visible."
        ),
    },
    {
        "id": "tau_a",
        "name": "Taurus A  (Crab Nebula)",
        "ra": 83.6221,
        "dec": 22.0145,
        "flux_jy": 1340,
        "freq_mhz": 408,
        "type": "Supernova Remnant / Pulsar",
        "color": "#ffff44",
        "why_radio": (
            "Remnant of SN1054, a supernova recorded by Chinese and Islamic astronomers in July 1054. "
            "At its centre is a pulsar spinning 30 times per second — a neutron star the size of a city "
            "with the mass of the Sun. The pulsar's wind continuously accelerates electrons to "
            "near-light-speed, producing synchrotron radio emission that has barely faded in 970 years. "
            "Used as a standard radio calibration source because its flux is stable and well characterised."
        ),
        "from_bangalore": (
            "Transits at 79° altitude — excellent viewing. While the Crab is visible with a small "
            "telescope, you are seeing scattered nebular light. The radio emission traces the pulsar "
            "wind nebula — an entirely different physical component invisible in amateur optical images."
        ),
    },
    {
        "id": "her_a",
        "name": "Hercules A  (3C 348)",
        "ra": 252.7917,
        "dec": 4.9925,
        "flux_jy": 520,
        "freq_mhz": 408,
        "type": "Radio Galaxy",
        "color": "#aa44ff",
        "why_radio": (
            "A giant elliptical galaxy 2 billion light-years away whose Hubble image shows a "
            "completely unremarkable fuzzy blob. Radio images at 1.4 GHz reveal something spectacular: "
            "two enormous spiral jets, each extending 1.5 million light-years, with ring-like "
            "structures that suggest precessing, pulsed jet activity over millions of years. "
            "One of the most visually striking radio sources in the sky — invisible optically."
        ),
        "from_bangalore": (
            "Transits near zenith (alt ~85°) from Bangalore. Passes almost directly overhead, "
            "completely invisible to the naked eye, with one of the most dramatic radio morphologies "
            "known. A textbook case for why radio astronomy changed our view of the universe."
        ),
    },
    {
        "id": "vela_pulsar",
        "name": "Vela Pulsar",
        "ra": 128.8359,
        "dec": -45.1763,
        "flux_jy": 5.0,
        "freq_mhz": 408,
        "type": "Pulsar / Supernova Remnant",
        "color": "#00ff88",
        "why_radio": (
            "One of the brightest and closest pulsars, just 1000 light-years away, spinning 11 times "
            "per second. The remnant of a supernova 10,000–12,000 years ago. Completely invisible "
            "optically — detectable only as a precise radio clock ticking 11 times per second. "
            "Pulsars are neutron stars: a teaspoon of material weighs one billion tonnes. "
            "Their clockwork radio pulses can be timed to nanosecond precision."
        ),
        "from_bangalore": (
            "Reaches 32° altitude from Bangalore — a southern-sky prize. The Vela supernova "
            "remnant is one of the closest stellar explosions to Earth. No optical counterpart "
            "visible from a light-polluted city, but radio observations clearly reveal the pulsar."
        ),
    },
    {
        "id": "galactic_center_ridge",
        "name": "Galactic Centre Ridge",
        "ra": 266.0,
        "dec": -28.9,
        "flux_jy": 5000,
        "freq_mhz": 408,
        "type": "Diffuse Galactic Emission",
        "color": "#ff6600",
        "why_radio": (
            "The inner few hundred light-years of the Milky Way contain supernova remnants, HII regions, "
            "molecular clouds, magnetar flares, and Sgr A* — all radiating intensely. "
            "This entire region is hidden behind ~30 magnitudes of dust extinction at optical wavelengths. "
            "In the Haslam 408 MHz map it appears as the brightest extended feature in the sky, "
            "a bright ridge tracing the galactic plane that optical observers can never see."
        ),
        "from_bangalore": (
            "Transits near 74° altitude. The optically dark region near Scorpius/Sagittarius — "
            "a coal-black rift in the Milky Way to the naked eye — is actually a wall of dust "
            "hiding one of the most active radio regions of our galaxy directly behind it."
        ),
    },
    {
        "id": "lmc",
        "name": "Large Magellanic Cloud",
        "ra": 80.8938,
        "dec": -69.7561,
        "flux_jy": 1000,
        "freq_mhz": 408,
        "type": "Irregular Dwarf Galaxy",
        "color": "#88ffff",
        "why_radio": (
            "Our nearest galactic neighbour at 160,000 light-years. Contains active star-forming regions "
            "and the site of SN 1987A — the closest supernova in modern times. The radio emission from "
            "SN 1987A has been monitored continuously since 1987 and is still brightening as the "
            "shock wave hits circumstellar material. A living laboratory for supernova physics."
        ),
        "from_bangalore": (
            "From latitude 13°N, the LMC barely grazes the horizon (max ~8°) and only during "
            "southern winter nights. Exceptional southern sky target — mostly inaccessible from India "
            "but worth watching for on clear nights with a clear southern horizon."
        ),
    },
    {
        "id": "sun",
        "name": "Sun  (radio bursts)",
        "ra": None,
        "dec": None,
        "flux_jy": None,
        "freq_mhz": 20,
        "type": "Solar Radio Bursts",
        "color": "#ffff00",
        "why_radio": (
            "The Sun is highly variable in radio. During solar flares, particles accelerated by "
            "magnetic reconnection produce intense bursts at metre wavelengths (10–100 MHz). "
            "A major Type III burst can briefly make the Sun 10,000× brighter than its quiet level. "
            "Radio JOVE volunteer stations stream live solar radio data at ~20 MHz. "
            "This is the most accessible live radio astronomy target — detectable with a simple dipole."
        ),
        "from_bangalore": (
            "The Sun is above the horizon during the day (obviously), and its radio bursts can be "
            "monitored in real time via the Radio JOVE network. Solar cycle 25 is near its peak "
            "in 2025, making this an excellent time to catch flare activity."
        ),
    },
]


def get_targets_with_altaz(sky, time=None):
    t = time or sky.now()

    sun_coord = get_sun(t)
    sun_ra = float(sun_coord.ra.deg)
    sun_dec = float(sun_coord.dec.deg)

    results = []
    for target in TARGETS:
        item = dict(target)
        if target["id"] == "sun":
            ra, dec = sun_ra, sun_dec
            item["ra"] = round(ra, 4)
            item["dec"] = round(dec, 4)
        else:
            ra, dec = target["ra"], target["dec"]

        alt, az = sky.to_altaz(ra, dec, t)
        item["alt"] = round(alt, 2)
        item["az"] = round(az, 2)
        item["visible"] = alt >= 5.0
        results.append(item)

    return results
