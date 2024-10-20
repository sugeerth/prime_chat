# Import necessary modules again due to execution context reset
import pandas as pd
import numpy as np
import datetime
import time
import streamlit as st
import altair as alt

class CGM:

    def __init__(self, start_time, num_points, duration_in_minutes):
        self.start_time = pd.Timestamp.now()
        self.num_points = num_points
        self.time_intervals = [start_time + pd.Timedelta(minutes=duration_in_minutes*i) for i in range(self.num_points)]
        # self.glucose_levels = np.random.normal(loc=100, scale=10, size=self.num_points)

        # hypoglycemic
        self.glucose_levels = np.random.normal(loc=80, scale=30, size=self.num_points)


        # Create initial dataframe
        self.cg_data = pd.DataFrame({
            'Time': self.time_intervals,
            'Glucose Level (mg/dL)': self.glucose_levels.round(1)
        })
    

    # Function to append new data
    def add_new_data(self, cg_data, new_time, new_glucose_level):
        new_data = pd.DataFrame({
            'Time': [new_time],
            'Glucose Level (mg/dL)': [new_glucose_level]
        })
        return pd.concat([cg_data, new_data], ignore_index=True)

    def initiate_cgm_chart(cg_data) -> alt.Chart:
            # Create initial chart
        glucose_chart = alt.Chart(cg_data).mark_line(point=True).encode(
            x='Time:T',
            y='Glucose Level (mg/dL):Q',
            tooltip=['Time:T', 'Glucose Level (mg/dL):Q']
        ).properties(
            title='Continuous Glucose Monitoring (Dynamic Update)',
            width=600,
            height=300
        )
        return glucose_chart
