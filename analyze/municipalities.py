import sys, math, pdb
from datetime import timedelta
import pandas as pd
import logging
import numpy as np

def combine_municipalities_data(municipality_id_df, municipality_data):
    municipality_ids = municipality_id_df['municipalityId'].unique()
    summary = None
    
    for municipality_id in municipality_ids:
        
        name = municipality_data[municipality_data['KUNTANRO'].isin(municipality_id_df[municipality_id_df['municipalityId'] == municipality_id]['originalMunicipalityId'])]['KUNTANIMIFI']
        m_name = None
        if len(name) > 0:
            m_name = name.item()
        municipality = {    
                "municipalityId": municipality_id, 
                "municipalityName": m_name
            }

        if summary is None:
            summary = pd.DataFrame(municipality, index = [0])
        else:
            summary.loc[len(summary)] = municipality
            
        summary['municipalityId'] = summary['municipalityId'].astype(int)
    
    return summary