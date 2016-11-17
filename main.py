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
    parser.add_argument('-ou', '--output-file-users', help='Output CSV file for users', required=False, default = os.getcwd() + "/summary-users.csv")
    parser.add_argument('-outputimages', '--output-images-folder', help='Output folder for plotimages', required=False, default = os.getcwd() + "/plots")
    args = vars(parser.parse_args())
    return args

        
if __name__ == "__main__":
    pd.set_option('display.width', 240)
    args = parse_args()
    input_file_operative = args['input_file_operative']
    input_file_usage = args['input_file_usage']
    output_file_applications = args['output_file_applications']
    output_file_users = args['output_file_users']
    output_images_folder = args['output_images_folder']

    analysis_start_time = datetime.datetime.now()

    odf = data_helper.import_operative_data(input_file_operative)
    udf = data_helper.import_usage_data(input_file_usage)
    

    print("Total number of apps: {}".format(len(odf)))
    print("Total number of events: {} with time range from {} to {} ".format(len(udf), udf['datetime'].min(), udf['datetime'].max()))

    application_summary =  analyze.summarize_applications(odf, udf)
    application_summary.to_csv(output_file_applications, sep=';', encoding='utf-8')
    
    user_summary = analyze.summarize_users(odf, udf)
    user_summary.to_csv(output_file_users, sep=';', encoding='utf-8')
    
    print("Analysis took {} seconds".format(datetime.datetime.now() - analysis_start_time))
    
    # Create folder for images
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)
    
    # Barchart for applications by month
    fig = plt.figure(1)
    plt.title("Kaikki")
    plt.xlabel("Kuukausi")
    plt.ylabel("Hakemusten maara")
    analyze.applications_by_month(application_summary)
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(output_images_folder + "/kaikki_kuukausittain.png", dpi=80)
    plt.close()
    
    fig = plt.figure(1)
    plt.title("Kaikki")
    plt.xlabel("Viikonpaiva")
    plt.ylabel("Hakemusten maara")
    analyze.applications_by_weekday(application_summary)
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(output_images_folder + "/kaikki_viikonpaiva.png", dpi=80)
    plt.close()
    
    
    operationIds = odf['operationId'].unique()
    counter = 2
    for operationId in operationIds:
        if isinstance(operationId, basestring):
            fig = plt.figure(counter)
            counter = counter + 1
            plt.title(operationId)
            plt.xlabel("Kuukausi")
            plt.ylabel("Hakemusten maara")
            analyze.applications_by_month_by_action(application_summary, operationId)
            canvas = FigureCanvasAgg(fig)
            canvas.print_figure(output_images_folder + '/' + operationId + "_kuukausittain.png", dpi=80)
            plt.close()
            