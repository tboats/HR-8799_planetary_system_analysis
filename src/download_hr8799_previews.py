"""
Fetch MAST preview images / products for HR 8799 JWST epochs.
"""

from astroquery.mast import Observations
import pandas as pd


def fetch_previews():
    print("Querying MAST products for HR 8799 JWST imaging...")
    obs = Observations.query_object("HR 8799", radius="0.01 deg")
    jwst_obs = obs[(obs['obs_collection'] == 'JWST') & (obs['dataproduct_type'] == 'image')]
    
    print(f"Found {len(jwst_obs)} JWST image observations.")
    
    # Get products for top imaging observations from different MJDs
    df = jwst_obs.to_pandas()
    df = df.sort_values(by='t_min')
    
    # Group by year/epoch
    print(df[['obsid', 'proposal_id', 'instrument_name', 'filters', 't_min']].head(15))

    return df


if __name__ == "__main__":
    fetch_previews()
