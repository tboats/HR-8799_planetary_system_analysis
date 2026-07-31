"""
Fetch real MAST Preview images (JPG/PNG) for JWST NIRCam HR 8799 observations.
"""

import os
import requests
from astroquery.mast import Observations
import pandas as pd

DATA_DIR = "/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/data/previews"

def fetch_mast_previews():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Querying MAST preview products for HR 8799 JWST imaging...")
    
    obs = Observations.query_object("HR 8799", radius="0.01 deg")
    jwst_obs = obs[(obs['obs_collection'] == 'JWST') & (obs['dataproduct_type'] == 'image')]
    
    # Get products
    products = Observations.get_product_list(jwst_obs)
    
    # Filter for preview images (JPG / PNG)
    previews = Observations.filter_products(
        products,
        productSubGroupDescription=['PREVIEW', 'PNG', 'JPG', 'IMAGE'],
        extension=['jpg', 'png', 'fits']
    )
    
    print(f"Found {len(previews)} preview/image products.")
    print(previews[['productFilename', 'dataURI', 'productSubGroupDescription', 'size']].head(20))

    # Download top previews
    manifest = Observations.download_products(previews[:10], download_dir=DATA_DIR)
    print("Download manifest:")
    print(manifest)

if __name__ == "__main__":
    fetch_mast_previews()
