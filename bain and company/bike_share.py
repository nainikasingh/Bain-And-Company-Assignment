#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
from datetime import datetime
from time import strptime
import numpy as np
import pandas as pd
from datacheck import question
from visualization import usage_stats, usage_plot
from IPython.display import display

file_in  = 'trip_data.csv'
file_out = 'new_trip_data.csv'

#with open(file_out, 'w') as f_out, open(file_in, 'r') as f_in:
#    in_reader = csv.reader(f_in)
#    out_writer = csv.writer(f_out)
#
#    while True:
#        datarow = next(in_reader)
#        if datarow[2][:9] == '10/1/2013':
#            break
#        out_writer.writerow(datarow)
#        
        
        
sample_data = pd.read_csv('new_trip_data.csv')

display(sample_data.head())

    

station_info = pd.read_csv('station_data.csv')
display(station_info.head())

def create_station_mapping(station_data):
    """
    Create a mapping from station IDs to cities, returning the
    result as a dictionary.
    """
    station_map = {}
    for data_file in station_data:
        with open(data_file, 'r') as f_in:
            
            weather_reader = csv.DictReader(f_in)

            for row in weather_reader:
                station_map[row['Id']] = row['City']
    return station_map


def summarise_data(trip_in, station_data, trip_out):
   
    station_map = create_station_mapping(station_data)
    
    with open(trip_out, 'w') as f_out:
        out_colnames = ['Duration', 'start_date', 'start_year',
                        'start_month', 'start_hour', 'weekday',
                        'start_city', 'end_city', 'subscription_type']        
        trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
        trip_writer.writeheader()
        
        for data_file in trip_in:
            with open(data_file, 'r') as f_in:
                trip_reader = csv.DictReader(f_in)

                for row in trip_reader:
                    new_point = {}
                    
                    new_point['Duration'] = float(row['Duration'])
                    
                    trip_date = datetime.strptime(row['Start Date'], '%d/%m/%Y %H:%M')
                    new_point['start_date']  = trip_date.strftime('%Y-%m-%d')
                    new_point['start_year']  = trip_date.strftime('%Y')
                    new_point['start_month'] = trip_date.strftime('%m')
                    new_point['start_hour']  = trip_date.strftime('%H')
                    new_point['weekday']     = trip_date.strftime('%d')
                    
                    new_point['start_city'] = station_map[row['Start Station']]
                    new_point['end_city'] = station_map[row['End Station']]
                    if 'Subscription Type' in row:
                        new_point['subscription_type'] = row['Subscription Type']
                    else:
                        new_point['subscription_type'] = row['Subscriber Type']

                    trip_writer.writerow(new_point)

    
    
station_data = ['station_data.csv']
trip_in = ['trip_data.csv']
trip_out = 'trip_summary.csv'
summarise_data(trip_in, station_data, trip_out)

sample_data = pd.read_csv(trip_out)
display(sample_data.head())

question(sample_data)

    

trip_data = pd.read_csv('trip_summary.csv')

usage_stats(trip_data)


usage_plot(trip_data, 'subscription_type')

usage_plot(trip_data, 'Duration')

usage_plot(trip_data, 'Duration', ['Duration < 360'])


usage_plot(trip_data, 'Duration', ['Duration < 360'], boundary = 0, bin_width = 5)


station_data = ['station_data.csv']
trip_in = ['trip_data.csv']
trip_out = 'data_y1_y2_summary.csv'

summarise_data(trip_in, station_data, trip_out)


trip_data = pd.read_csv('data_y1_y2_summary.csv')
display(trip_data.head())
#
#usage_stats(trip_data)
#usage_plot(trip_data)











