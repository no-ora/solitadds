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

import applications

def draw_plots_for_month(output_images_folder, application_summary, filename):
# Create folder for images
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)
    
    # Barchart for applications by month
    fig = plt.figure(1)
    plt.title("Kaikki")
    plt.xlabel("Kuukausi")
    plt.ylabel("Hakemusten maara")
    applications.applications_by_month(application_summary)
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(output_images_folder + "/" + filename + ".png", dpi=80)
    plt.close()
    
    operationIds = application_summary['operationId'].unique()
    for operationId in operationIds:
        if isinstance(operationId, basestring):
            fig = plt.figure(1)
            plt.title(operationId)
            plt.xlabel("Kuukausi")
            plt.ylabel("Hakemusten maara")
            applications.applications_by_month_by_action(application_summary, operationId)
            canvas = FigureCanvasAgg(fig)
            canvas.print_figure(output_images_folder + '/' + operationId + "_" + filename + ".png", dpi=80)
            plt.close()

def draw_plots_for_weekday(output_images_folder, application_summary, filename):
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)
    
    # Barchart for applications by weekday
    fig = plt.figure(2)
    plt.title("Kaikki")
    plt.xlabel("Viikonpaiva")
    plt.ylabel("Hakemusten maara")
    applications.applications_by_weekday(application_summary)
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(output_images_folder + "/" + filename + ".png", dpi=80)
    plt.close()
    
    operationIds = application_summary['operationId'].unique()
    for operationId in operationIds:
        if isinstance(operationId, basestring):
            fig = plt.figure(1)
            plt.title(operationId)
            plt.xlabel("Viikonpaiva")
            plt.ylabel("Hakemusten maara")
            applications.applications_by_weekday_by_operation(application_summary, operationId)
            canvas = FigureCanvasAgg(fig)
            canvas.print_figure(output_images_folder + '/' + operationId + "_" + filename + ".png", dpi=80)
            plt.close()
    
def draw_plots_for_hour(output_images_folder, application_summary, filename):
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)
    
    # Barchart for applications by hour
    fig = plt.figure(3)
    plt.title("Kaikki")
    plt.xlabel("Tunti")
    plt.ylabel("Hakemusten maara")
    applications.applications_by_hour(application_summary)
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(output_images_folder + "/" + filename + ".png", dpi=80)
    plt.close()
    
    operationIds = application_summary['operationId'].unique()
    for operationId in operationIds:
        if isinstance(operationId, basestring):
            fig = plt.figure(1)
            plt.title(operationId)
            plt.xlabel("Tunti")
            plt.ylabel("Hakemusten maara")
            applications.applications_by_hour_by_operation(application_summary, operationId)
            canvas = FigureCanvasAgg(fig)
            canvas.print_figure(output_images_folder + '/' + operationId + "_" + filename + ".png", dpi=80)
            plt.close()
    
       
    
    