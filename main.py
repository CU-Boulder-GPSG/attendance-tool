
import pandas as pd
import os
import glob
from datetime import datetime


def read_csv_wrapper(pathto_role):
    # Import csv in folder
    path = os.getcwd()
    pathto_data = glob.glob(
        os.path.join(
            path,
            'place_attendance_data',
            '*.csv'
        )
    )
    df = pd.read_csv(pathto_data[0], header=1)
    df = df.drop(0, axis=0)

    # Get Affiliation Information
    df_affil = pd.read_csv(pathto_role)
    df = df.merge(
        df_affil,
        left_on='Please select your position:',
        right_on='Affiliation',
        how='left'
    )
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


def main():
    # Local vars
    pathto_role = os.path.join('role_information', 'roles.csv')

    # Import data
    df = read_csv_wrapper(pathto_role)

    # Generate minutes table
    date = '2022-01-26'
    df_minutes = get_minutes_table('2022-01-26', df)
    df_minutes.to_csv(date+'_minutes.csv', index=False)


if __name__ == '__main__':
    main()
