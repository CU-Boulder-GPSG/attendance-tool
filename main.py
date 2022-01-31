
import pandas as pd
import os
from datetime import datetime

pathto_attendance = os.path.join('attendance_data', 'data.csv')
pathto_role = os.path.join('role_information', 'roles.csv')


def read_csv_wrapper(pathto_data, pathto_role):
    # Import
    df = pd.read_csv(pathto_data, header=1)
    df = df.drop(0, axis=0)

    # Get Affiliation Information
    df_affil = pd.read_csv(pathto_role)
    df = df.merge(df_affil, left_on='Please select your position:', right_on='Affiliation', how='left')
    return df


def get_minutes_table(meeting, df):
    # Parse Dates
    df['Start Date'] = df['Start Date'].apply(pd.to_datetime).apply(datetime.date)
    meeting = datetime.strptime(meeting, '%Y-%m-%d').date()

    # Filter Dates
    df = df[df['Start Date'] == meeting]

    # Create Name (Affiliation) Column
    cols = ['Please select yourself', 'Please select yourself.1',
            'Please select yourself.2', 'Please select yourself.3',
            'Please select yourself.4', 'Please select yourself.5',
            'Please enter your full name:', 'Please enter your full name:.1',
            'Name']
    df[cols] = df.fillna('')[cols]
    df['Name'] = df[cols].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
    cols = ['Please select your position:', 'Please Select Your Affiliation', 'Please enter your department and please add the corresponding four letter code\n\n(For example: Environmental Studies, ENVS)']
    df[cols] = df[cols].fillna('')
    df['Affiliation'] = df[cols].apply(lambda row: ''.join(row.values.astype(str)), axis=1)
    df['Name (Affiliation)'] = df['Name'] + ' (' + df['Affiliation'] + ')'

    # Create Minutes Table
    df_table = pd.DataFrame()
    for i in df['Please select your GPSG Position'].unique():
        ser = df[df['Please select your GPSG Position'] == i]['Name (Affiliation)']
        ser = ser.reset_index(drop=True)
        ser.rename(i)
        df_table = pd.concat([df_table, ser], 1, ignore_index=True)
    df_table.columns = df['Please select your GPSG Position'].unique()
    return df_table


if __name__ == '__main__':
    df = read_csv_wrapper(pathto_attendance, pathto_role)
    get_minutes_table('2022-01-26', df).to_csv('Minutes Table From Qualtrics.csv', index=False)
