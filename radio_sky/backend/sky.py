"""
Sky position engine for Bangalore, India.
Answers: what is overhead right now, where is the galactic plane, etc.
"""
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
import astropy.units as u
import numpy as np

# Bangalore: IISc campus area, elevation ~920m
BANGALORE = EarthLocation(lat=12.9716 * u.deg, lon=77.5946 * u.deg, height=920 * u.m)


class BangaloreSky:
    def __init__(self):
        self.location = BANGALORE

    def now(self):
        return Time.now()

    def altaz_frame(self, time=None):
        if time is None:
            time = self.now()
        return AltAz(obstime=time, location=self.location)

    def to_altaz(self, ra_deg, dec_deg, time=None):
        coord = SkyCoord(ra=ra_deg * u.deg, dec=dec_deg * u.deg, frame="icrs")
        altaz = coord.transform_to(self.altaz_frame(time))
        return float(altaz.alt.deg), float(altaz.az.deg)

    def get_zenith(self, time=None):
        """RA/Dec of the point directly overhead."""
        if time is None:
            time = self.now()
        lst = time.sidereal_time("apparent", longitude=self.location.lon)
        return float(lst.deg), float(self.location.lat.deg)

    def get_galactic_plane(self, time=None, n=720):
        """
        Returns a list of {l, alt, az} for points along b=0 galactic plane.
        Client uses this to draw the galactic plane arc on the sky map.
        """
        if time is None:
            time = self.now()
        frame = self.altaz_frame(time)
        lons = np.linspace(0, 360, n, endpoint=False)
        gal = SkyCoord(l=lons * u.deg, b=0 * u.deg, frame="galactic")
        altaz = gal.transform_to(frame)
        return [
            {"l": round(float(l), 1), "alt": round(float(a), 2), "az": round(float(z), 2)}
            for l, a, z in zip(lons, altaz.alt.deg, altaz.az.deg)
        ]

    def sky_info(self):
        t = self.now()
        zenith_ra, zenith_dec = self.get_zenith(t)
        lst = t.sidereal_time("apparent", longitude=self.location.lon)
        return {
            "utc": t.isot,
            "lst_hours": round(float(lst.hour), 4),
            "zenith_ra": round(zenith_ra, 4),
            "zenith_dec": round(zenith_dec, 4),
            "location": {
                "name": "Bangalore",
                "lat": float(BANGALORE.lat.deg),
                "lon": float(BANGALORE.lon.deg),
            },
        }
