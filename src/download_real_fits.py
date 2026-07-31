"""
Query, download, and extract actual FITS imaging data for HR 8799 from MAST.
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from astroquery.mast import Observations
from astropy.io import fits
from astropy.visualization import astropy_mpl_style, ImageNormalize, LogStretch, AsinhStretch

DATA_DIR = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/data"

def download_and_process_fits():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Querying MAST for JWST & HST HR 8799 imaging data products...")
    
    # Query imaging products for HR 8799
    obs = Observations.query_object("HR 8799", radius="0.01 deg")
    jwst_obs = obs[(obs['obs_collection'] == 'JWST') & (obs['dataproduct_type'] == 'image')]
    
    print(f"Found {len(jwst_obs)} JWST image observations.")
    
    # Filter for NIRCam coronagraphy observations
    nircam_coron = jwst_obs[jwst_obs['instrument_name'] == 'NIRCAM/CORON']
    print(f"Found {len(nircam_coron)} NIRCam coronagraphy observations.")
    
    # Select top datasets from 2022 and 2024
    if len(nircam_coron) > 0:
        # Get product list for first two distinct observations
        products = Observations.get_product_list(nircam_coron[:3])
        # Filter for calibrated science image products (_cal.fits or _i2d.fits)
        cal_products = Observations.filter_products(
            products, 
            productSubGroupDescription=['I2D', 'CAL'], 
            extension='fits'
        )
        print(f"Filtered {len(cal_products)} calibrated FITS products.")
        
        if len(cal_products) > 0:
            print("Downloading FITS products (top 2)...")
            manifest = Observations.download_products(cal_products[:2], download_dir=DATA_DIR)
            print("Download manifest:", manifest)
            return manifest

    return None

if __name__ == "__main__":
    download_and_process_fits()
