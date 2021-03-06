import sys, math, pdb
from datetime import timedelta
import pandas as pd
import numpy as np
import logging

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

SESSION_THRESHOLD_IN_MINUTES = 15

def summarize_applications(odf, udf, municipality_summary):
    """ Create a summary of the applications as a table. Presumes app_events are in datetime order
          * Count number of comments for different roles
    """

    summary = None

    udf = udf.sort_values(['applicationId', 'datetime'])

    print("Analyzing {} usage events  ({} unique actions)".format(len(udf), len(udf["action"].unique())))

    application_ids = udf['applicationId'].unique()

    n = 0
    total_count = len(application_ids)

    for application_id in application_ids:
        app = odf[odf['applicationId'] == application_id]

        if app.empty:
            print("Skipping application with no operative data: " + application_id)
            continue

        app_info = parse_application_summary(application_id, app.iloc[0].to_dict(), udf[udf['applicationId'] == application_id], municipality_summary)

        if summary is None:
            summary = pd.DataFrame(app_info, index = [0])
        else:
            summary.loc[len(summary)] = app_info

        n = n + 1
        if n % 1000 == 0 or n == total_count:
            print("Processing.. {}%".format( int( float(n) / total_count * 100)))


    summary = pd.merge(odf, summary, on = 'applicationId')

    return summary

def parse_application_summary(application_id, app, ae, municipality_summary):
    result = {  "applicationId": application_id, 
                "nEvents": len(ae),
                "nUsers": ae.userId.nunique(),
                "nUpdateDocs": len(ae[ae['action'] == 'update-doc']),
                "nApplicationComments": len(ae[(ae['action'] == 'add-comment') & (ae['target'] == 'application')]),
                "nApplicationCommentsApplicant": len(ae[(ae['role'] == 'applicant') & (ae['action'] == 'add-comment') & (ae['target'] == 'application')]),
                "nApplicationCommentsAuthority": len(ae[(ae['role'] == 'authority') & (ae['action'] == 'add-comment') & (ae['target'] == 'application')]),
                "nUploadAttachments" : len(ae[ae['action'] == 'upload-attachment']),
                "nInvites" : len(ae[ae['action'] == 'invite-with-role']),
                "createdMonth": app['createdDate'].month,
                "createdWeekDay": app['createdDate'].dayofweek,
                "createdHour": app['createdDate'].hour,
                "sessionLength": count_session_length(ae, SESSION_THRESHOLD_IN_MINUTES),
                "sessionLengthApplicant": count_session_length_by_role(ae, 'applicant', SESSION_THRESHOLD_IN_MINUTES),
                "sessionLengthAuthority": count_session_length_by_role(ae, 'authority', SESSION_THRESHOLD_IN_MINUTES),
                "leadTime": count_days(app, 'createdDate', 'verdictGivenDate'),
                "municipality" : municipality_summary[municipality_summary['municipalityId'] == app['municipalityId']]['municipalityName']
            }
    return result

def count_session_length(events, threshold_in_minutes):
    delta = timedelta(minutes = threshold_in_minutes)

    timestamps = events['datetime']

    if(len(timestamps) == 0):
        return 0

    prev = timestamps.iloc[0]
    i = 1
    totalSession = 0
    while i < len(timestamps):
        diff = timestamps.iloc[i] - prev
        prev = timestamps.iloc[i]
        if(diff < delta):
            totalSession = totalSession + diff.total_seconds()

        i = i + 1
        
    return round(totalSession / 60, 0)

def count_session_length_by_role(events, role, threshold_in_minutes):
    return count_session_length(events[events['role'] == role], threshold_in_minutes)

def count_days(app, from_date_name, till_date_name):
    delta = app[till_date_name] - app[from_date_name]

    if pd.isnull(delta):
        return None
    else:
        return int(delta.days + 1)


def applications_by_month_by_action(application_summary, operation):
    odf_operation = application_summary[application_summary['operationId'] == operation]
    nApplicationsMonth = range(12)
    for i in range(12):
        nApplicationsMonth[i] = len(odf_operation[odf_operation['createdMonth'] == (i + 1)])
    
    plt.bar([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], nApplicationsMonth, width=1.0, color="blue")
    
def applications_by_month(application_summary):
    nApplicationsMonth = range(12)
    for i in range(12):
        nApplicationsMonth[i] = len(application_summary[application_summary['createdMonth'] == (i + 1)])
    
    plt.bar([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], nApplicationsMonth, width=1.0, color="blue")
    
def applications_by_weekday(application_summary):
    ind = np.arange(7) + 0.2
    nApplicationsWeekday = range(0, 7)
    for i in range(0, 7):
        nApplicationsWeekday[i] = len(application_summary[application_summary['createdWeekDay'] == i])
    
    plt.bar(ind, nApplicationsWeekday, width=1.0, color="blue")
    plt.xticks(ind + 0.8/2., ('Ma', 'Ti', 'Ke', 'To', 'Pe', 'La','Su'))
    
def applications_by_weekday_by_operation(application_summary, operation):
    odf_operation = application_summary[application_summary['operationId'] == operation]
    ind = np.arange(7) + 0.2
    nApplicationsWeekday = range(0, 7)
    for i in range(0, 7):
        nApplicationsWeekday[i] = len(odf_operation[odf_operation['createdWeekDay'] == i])
    
    plt.bar(ind, nApplicationsWeekday, width=1.0, color="blue")
    plt.xticks(ind + 0.8/2., ('Ma', 'Ti', 'Ke', 'To', 'Pe', 'La','Su'))
    
def applications_by_hour(application_summary):
    nApplicationsHour = range(24)
    for i in range(24):
        nApplicationsHour[i] = len(application_summary[application_summary['createdHour'] == i])
    
    plt.bar(range(24), nApplicationsHour, width=1.0, color="blue")
    
def applications_by_hour_by_operation(application_summary, operation):
    odf_operation = application_summary[application_summary['operationId'] == operation]
    nApplicationsHour = range(24)
    for i in range(24):
        nApplicationsHour[i] = len(odf_operation[odf_operation['createdHour'] == i])
    
    plt.bar(range(24), nApplicationsHour, width=1.0, color="blue")

