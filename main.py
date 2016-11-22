#!/usr/bin/python

import sys, re, pdb, os
import logging
import argparse

import numpy as np
import pandas as pd

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import datetime

import utils, data_helper

import analyze


def parse_args():
    """
    Parse command line args.
    
    Example
    -------
    python main.py --input-file-operative ../data/small/some-applications-operative-pub-20161031.csv --input-file-usage ../data/small/some-lupapiste-usage-pub-20161031.csv --output-file-applications ../target/application-summary.csv --output-file-users ../target/user-summary.csv
    """
    parser = argparse.ArgumentParser(description='SOLITADDS analysis')
    parser.add_argument('-io', '--input-file-operative', help='Input CSV file for operative data', required = False, default = os.getcwd() + "/test-data/some-applications-operative-pub-20161031.csv")
    parser.add_argument('-iu', '--input-file-usage', help='Input CSV file for usage data', required = False, default = os.getcwd() + "/test-data/some-lupapiste-usage-pub-20161031.csv")
    parser.add_argument('-oa', '--output-file-applications', help='Output CSV file for applications', required = False, default = os.getcwd() + "/summary-applications.csv")
    parser.add_argument('-imi', '--input-file-municipality-id', help='Input CSV file for municipality id data', required = False, default = os.getcwd() + "/test-data/lupapiste-usage-municipality-ids-20161031.csv")
    parser.add_argument('-im', '--input-file-municipality-data', help='Input CSV file for municipality data', required = False, default = os.getcwd() + "/test-data/kuntanumerot.csv")
    parser.add_argument('-ou', '--output-file-users', help='Output CSV file for users', required=False, default = os.getcwd() + "/summary-users.csv")
    parser.add_argument('-outputimages', '--output-images-folder', help='Output folder for plotimages', required=False, default = os.getcwd() + "/plots")
    args = vars(parser.parse_args())
    return args

        
if __name__ == "__main__":
    pd.set_option('display.width', 240)
    args = parse_args()
    input_file_operative = args['input_file_operative']
    input_file_usage = args['input_file_usage']
    input_file_municipality_id = args['input_file_municipality_id']
    input_file_municipality_data = args['input_file_municipality_data']
    output_file_applications = args['output_file_applications']
    output_file_users = args['output_file_users']
    output_images_folder = args['output_images_folder']

    analysis_start_time = datetime.datetime.now()

    odf = data_helper.import_operative_data(input_file_operative)
    udf = data_helper.import_usage_data(input_file_usage)
    municipalityId = data_helper.import_municipality_id_data(input_file_municipality_id)
    municipalityData = data_helper.import_municipality_data(input_file_municipality_data)

    print("Total number of apps: {}".format(len(odf)))
    print("Total number of events: {} with time range from {} to {} ".format(len(udf), udf['datetime'].min(), udf['datetime'].max()))

    municipality_summary = analyze.combine_municipalities_data(municipalityId, municipalityData)

    application_summary =  analyze.summarize_applications(odf, udf, municipality_summary)
    application_summary.to_csv(output_file_applications, sep=';', encoding='utf-8')
    
    user_summary = analyze.summarize_users(odf, udf)
    user_summary.to_csv(output_file_users, sep=';', encoding='utf-8')
    
    
    print("Analysis took {} seconds".format(datetime.datetime.now() - analysis_start_time))
    
    # Plots for all applications
    analyze.draw_plots_for_month(output_images_folder, application_summary, "kuukausi_kaikki")
    analyze.draw_plots_for_weekday(output_images_folder, application_summary, "viikonpaiva_kaikki")
    analyze.draw_plots_for_hour(output_images_folder, application_summary, "tunti_kaikki")
    
    # Plots for one time builders
    #one_time_builder_data = application_summary[application_summary['applicationId'].isin(analyze.get_one_time_builder_application_ids(user_summary))]
    #analyze.draw_plots_for_month(output_images_folder, one_time_builder_data, "kuukausi_kertarakentaja")
    #analyze.draw_plots_for_weekday(output_images_folder, one_time_builder_data, "viikonpaiva_kertarakentaja")
    #analyze.draw_plots_for_hour(output_images_folder, one_time_builder_data, "tunti_kertarakentaja")
    