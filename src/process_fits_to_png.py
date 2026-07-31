"""
Process real JWST FITS file for HR 8799 and export high-resolution pixel matrices.
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ImageNormalize, AsinhStretch, LogStretch

FITS_PATH = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/data/mastDownload/JWST/jw01194001001_03102_00001_nrcalong/jw01194001001_03102_00001_nrcalong_cal.fits"
OUT_DIR = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/docs/images"

def process_fits():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Loading real JWST FITS file: {FITS_PATH}")
    
    with fits.open(FITS_PATH) as hdul:
        hdul.info()
        data = hdul['SCI'].data
        header = hdul['SCI'].header
        print(f"Data shape: {data.shape}, min: {np.nanmin(data)}, max: {np.nanmax(data)}")

        # Handle NaNs and background
        data_clean = np.nan_to_num(data, nan=0.0)
        
        # Center crop around central star coronagraph mask
        ny, nx = data_clean.shape
        cy, cx = ny // 2, nx // 2
        crop_size = 400
        crop = data_clean[cy - crop_size//2 : cy + crop_size//2, cx - crop_size//2 : cx + crop_size//2]
        
        # Export real image renders in multiple colormaps (Inferno, Greys, Viridis)
        norm = ImageNormalize(crop, stretch=AsinhStretch(a=0.05), vmin=np.percentile(crop, 5), vmax=np.percentile(crop, 99.5))
        
        plt.figure(figsize=(8, 8), dpi=150)
        plt.imshow(crop, origin='lower', cmap='inferno', norm=norm)
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        out_inferno = os.path.join(OUT_DIR, "jwst_2022_inferno.png")
        plt.savefig(out_inferno, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        plt.figure(figsize=(8, 8), dpi=150)
        plt.imshow(crop, origin='lower', cmap='gray', norm=norm)
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        out_grey = os.path.join(OUT_DIR, "jwst_2022_grey.png")
        plt.savefig(out_grey, bbox_inches='tight', pad_inches=0)
        plt.close()

        print(f"✅ Exported real JWST FITS image renders to {OUT_DIR}")

if __name__ == "__main__":
    process_fits()
