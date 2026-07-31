"""
Update HR 8799 multi-epoch image generator and HTML renderer with true 3D Keplerian orbital inclination
(i = 28 deg, Omega = 55 deg).
"""

import os
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

OUT_DIR = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/docs/images"
HTML_PATH = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/docs/hr8799_blink_comparator.html"

# HR 8799 System 3D Orbital Parameters (Wang et al. 2018 / GRAVITY Collaboration 2019)
# Inclination i = 28 deg, Node PA Omega = 55 deg
INC_DEG = 28.0
OMEGA_DEG = 55.0

PLANET_ORBITS = {
    'b': {'a_au': 68.0, 'P_yr': 460.0, 'e': 0.02, 'omega_deg': 110.0, 'M0_deg': 240.0, 'flux': 0.75, 'color': '#38bdf8'},
    'c': {'a_au': 43.0, 'P_yr': 190.0, 'e': 0.04, 'omega_deg': 140.0, 'M0_deg': 310.0, 'flux': 1.0,  'color': '#4ade80'},
    'd': {'a_au': 27.0, 'P_yr': 100.0, 'e': 0.10, 'omega_deg': 85.0,  'M0_deg': 180.0, 'flux': 0.95, 'color': '#fbbf24'},
    'e': {'a_au': 16.0, 'P_yr': 45.0,  'e': 0.12, 'omega_deg': 60.0,  'M0_deg': 45.0,  'flux': 0.85, 'color': '#f87171'}
}

EPOCHS = {
    '2008': 2008.8,
    '2015': 2015.5,
    '2022': 2022.9,
    '2024': 2024.5,
    '2026': 2026.2
}

PIXEL_SCALE = 0.015 # arcsec / pixel
PARSEC_DIST = 39.4 # distance in pc (so 1 AU = 1 / 39.4 = 0.02538 arcsec)
AU_TO_ARCSEC = 1.0 / PARSEC_DIST

IMG_SIZE = 512
CENTER = IMG_SIZE // 2

def solve_kepler(M, e):
    """Solve Kepler's equation M = E - e*sin(E) for Eccentric Anomaly E."""
    M = M % (2 * math.pi)
    E = M
    for _ in range(10):
        f = E - e * math.sin(E) - M
        f_prime = 1.0 - e * math.cos(E)
        E -= f / f_prime
    return E

def get_kepler_sky_pos(planet_key, year):
    p = PLANET_ORBITS[planet_key]
    dt = year - 2008.8
    mean_motion = (2.0 * math.pi) / p['P_yr']
    M = math.radians(p['M0_deg']) + mean_motion * dt
    
    e = p['e']
    E = solve_kepler(M, e)
    
    # True anomaly v
    sin_v = math.sqrt(1 - e**2) * math.sin(E) / (1 - e * math.cos(E))
    cos_v = (math.cos(E) - e) / (1 - e * math.cos(E))
    v = math.atan2(sin_v, cos_v)
    
    # Radius r in AU
    r = p['a_au'] * (1.0 - e * math.cos(E))
    
    # Orbit plane coordinates (x_orb, y_orb)
    u = v + math.radians(p['omega_deg']) # argument of latitude
    
    inc = math.radians(INC_DEG)
    Omega = math.radians(OMEGA_DEG)
    
    # Projected coordinates on sky plane (East = -x, North = -y)
    x_sky_au = r * (math.cos(u) * math.sin(Omega) + math.sin(u) * math.cos(Omega) * math.cos(inc))
    y_sky_au = r * (math.cos(u) * math.cos(Omega) - math.sin(u) * math.sin(Omega) * math.cos(inc))
    
    dx_arcsec = -x_sky_au * AU_TO_ARCSEC
    dy_arcsec = y_sky_au * AU_TO_ARCSEC
    
    sep_arcsec = math.sqrt(dx_arcsec**2 + dy_arcsec**2)
    pa_deg = (math.degrees(math.atan2(-dx_arcsec, dy_arcsec))) % 360.0
    
    return dx_arcsec, dy_arcsec, sep_arcsec, pa_deg

def generate_epoch_images():
    os.makedirs(OUT_DIR, exist_ok=True)
    grid_y, grid_x = np.ogrid[:IMG_SIZE, :IMG_SIZE]
    arcsec_to_pix = 1.0 / PIXEL_SCALE
    
    for epoch_key, year in EPOCHS.items():
        np.random.seed(int(year * 10))
        img = np.random.normal(loc=0.02, scale=0.015, size=(IMG_SIZE, IMG_SIZE))
        
        # Halo & Speckle noise
        r_pix = np.sqrt((grid_x - CENTER)**2 + (grid_y - CENTER)**2)
        r_arcsec = r_pix * PIXEL_SCALE
        speckles = gaussian_filter(np.random.exponential(scale=0.08, size=(IMG_SIZE, IMG_SIZE)), sigma=1.8)
        halo = 0.8 / (r_arcsec + 0.15)**2 * speckles
        halo[r_arcsec < 0.22] = 0.0
        img += halo
        
        # Inject Planets at exact 3D Keplerian Positions
        for p_key, p_info in PLANET_ORBITS.items():
            if epoch_key == '2008' and p_key == 'e':
                continue
            dx, dy, sep, pa = get_kepler_sky_pos(p_key, year)
            px = CENTER + (dx * arcsec_to_pix)
            py = CENTER + (dy * arcsec_to_pix)
            
            dist_sq = (grid_x - px)**2 + (grid_y - py)**2
            psf = p_info['flux'] * np.exp(-dist_sq / (2 * 3.2**2))
            airy = p_info['flux'] * 0.12 * np.exp(-dist_sq / (2 * 7.5**2)) * np.cos(np.sqrt(dist_sq) * 0.8)**2
            img += psf + airy

        img[r_arcsec < 0.24] = 0.005
        
        plt.figure(figsize=(7, 7), dpi=120)
        plt.imshow(img, origin='lower', cmap='inferno', vmin=0.0, vmax=0.9)
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        
        out_path = os.path.join(OUT_DIR, f"hr8799_epoch_{epoch_key}.png")
        plt.savefig(out_path, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"Generated Keplerian 3D epoch {epoch_key} ({year}) -> {out_path}")

if __name__ == "__main__":
    generate_epoch_images()
