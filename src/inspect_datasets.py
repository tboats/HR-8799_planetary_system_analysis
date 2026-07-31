"""
Detailed inspection of JWST observations for HR 8799.
"""

from astroquery.mast import Observations
import pandas as pd


def inspect_jwst_hr8799():
    print("Querying MAST JWST data products for HR 8799...")
    obs_table = Observations.query_object("HR 8799", radius="0.01 deg")
    jwst_obs = obs_table[obs_table['obs_collection'] == 'JWST']
    
    df = jwst_obs.to_pandas()
    
    # Clean and group by program / instrument
    summary = df.groupby(['proposal_id', 'instrument_name', 'filters', 'obs_title']).size().reset_index(name='count')
    print("\n=== JWST HR 8799 Programs Summary ===")
    print(summary.to_string(index=False))

    return df, summary


if __name__ == "__main__":
    inspect_jwst_hr8799()
