"""
Query MAST for JWST high-contrast imaging data of HR 8799.
"""

from astroquery.mast import Observations


def search_hr8799_jwst():
    print("Searching MAST archive for JWST observations of HR 8799...")
    obs_table = Observations.query_object("HR 8799", radius="0.01 deg")
    
    # Filter for JWST observations
    jwst_obs = obs_table[obs_table['obs_collection'] == 'JWST']
    print(f"Found {len(jwst_obs)} JWST observations for HR 8799.")
    
    if len(jwst_obs) > 0:
        cols = ['obsid', 'proposal_id', 'instrument_name', 'filters', 'obs_title', 't_min', 't_exptime']
        print(jwst_obs[cols])
    return jwst_obs


if __name__ == "__main__":
    search_hr8799_jwst()
