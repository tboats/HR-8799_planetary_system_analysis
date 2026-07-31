"""
Query MAST for Stage 3 / Reduced high-contrast coronagraphic images of HR 8799.
"""

from astroquery.mast import Observations
import pandas as pd

def search_reduced():
    print("Searching MAST for Stage 3 / Combined JWST imaging for HR 8799...")
    obs = Observations.query_object("HR 8799", radius="0.01 deg")
    jwst_obs = obs[(obs['obs_collection'] == 'JWST') & (obs['dataproduct_type'] == 'image')]
    
    # Filter products for Stage 3 (_i2d.fits or preview)
    products = Observations.get_product_list(jwst_obs)
    i2d_products = Observations.filter_products(
        products,
        productSubGroupDescription=['I2D', 'STAGE3', 'DRZ'],
        extension='fits'
    )
    
    print(f"Found {len(i2d_products)} Stage 3 (I2D) image products.")
    if len(i2d_products) > 0:
        print(i2d_products[['productFilename', 'dataURI', 'size']].head(10))
        # Download top 2 Stage 3 products
        manifest = Observations.download_products(i2d_products[:2], download_dir="/Users/tboats/Documents/Code/physics/astronomy/Projects/hr8799-jwst-orbits/data/reduced")
        print(manifest)

if __name__ == "__main__":
    search_reduced()
