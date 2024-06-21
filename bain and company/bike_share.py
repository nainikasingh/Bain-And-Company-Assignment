#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from datetime import datetime
from datacheck import question
from visualization import usage_stats, usage_plot
from IPython.display import display

# Filenames
file_in = 'trip_data.csv'
file_out = 'new_trip_data.csv'
station_file = 'station_data.csv'
trip_out1 = 'trip_summary.csv'
trip_out2 = 'data_y1_y2_summary.csv'

# Load sample data
sample_data = pd.read_csv(file_out)
display(sample_data.head())

# Load station data
station_info = pd.read_csv(station_file)
display(station_info.head())

def create_station_mapping(station_data_file):
    """
    Create a mapping from station IDs to cities, returning the
    result as a dictionary.
    """
    station_df = pd.read_csv(station_data_file)
    return station_df.set_index('Id')['City'].to_dict()

def summarise_data(trip_file, station_data_file, trip_out):
    # Create station mapping
    station_map = create_station_mapping(station_data_file)
    
    # Read trip data
    trip_df = pd.read_csv(trip_file)
    
    # Process date fields and map station IDs to cities
    trip_df['start_date'] = pd.to_datetime(trip_df['Start Date'], format='%d/%m/%Y %H:%M')
    trip_df['start_year'] = trip_df['start_date'].dt.year
    trip_df['start_month'] = trip_df['start_date'].dt.month
    trip_df['start_hour'] = trip_df['start_date'].dt.hour
    trip_df['weekday'] = trip_df['start_date'].dt.weekday
    trip_df['start_city'] = trip_df['Start Station'].map(station_map)
    trip_df['end_city'] = trip_df['End Station'].map(station_map)
    
    # Select and rename columns
    trip_df = trip_df.rename(columns={'Duration': 'duration', 'Subscription Type': 'subscription_type', 'Subscriber Type': 'subscription_type'})
    trip_df = trip_df[['duration', 'start_date', 'start_year', 'start_month', 'start_hour', 'weekday', 'start_city', 'end_city', 'subscription_type']]
    
    # Save to new CSV
    trip_df.to_csv(trip_out, index=False)

# Summarize data
summarise_data(file_in, station_file, trip_out1)

# Load and display summarized data
sample_data = pd.read_csv(trip_out1)
display(sample_data.head())

question(sample_data)

# Generate usage stats and plots
trip_data = pd.read_csv(trip_out1)
usage_stats(trip_data)
usage_plot(trip_data, 'subscription_type')
usage_plot(trip_data, 'duration')
usage_plot(trip_data, 'duration', ['duration < 360'])
usage_plot(trip_data, 'duration', ['duration < 360'], boundary=0, bin_width=5)

# Summarize additional data
summarise_data(file_in, station_file, trip_out2)

# Load and display additional summarized data
trip_data = pd.read_csv(trip_out2)
display(trip_data.head())
