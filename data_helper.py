import pandas as pd
import logging
import pdb

def import_operative_data(file_name):
    df = pd.read_csv(file_name, parse_dates=['createdDate', 'submittedDate', 'sentDate', 'verdictGivenDate', 'canceledDate'], sep = ';')
    df = df.sort_values(['applicationId'])
    return df

def import_usage_data(file_name):
    df = pd.read_csv(file_name, parse_dates=['datetime'], sep = ';')
    df = df[df["municipalityId"].notnull()]
    df["municipalityId"] = df["municipalityId"].astype(int)
    df["userId"] = df["userId"].astype(int)
    df = df.sort_values(['applicationId', 'datetime'])
    return df

def import_municipality_id_data(file_name):
    df = pd.read_csv(file_name, sep = ";")
    df["municipalityId"] = df["municipalityId"].astype(int)
    df["originalMunicipalityId"] = df["originalMunicipalityId"].astype(int)
    df = df.sort_values(['municipalityId'])
    return df

def import_municipality_data(file_name):
    df = pd.read_csv(file_name, sep = ";")
    df["KUNTANRO"] = df["KUNTANRO"].astype(int)
    df = df.sort_values(['KUNTANRO'])
    return df