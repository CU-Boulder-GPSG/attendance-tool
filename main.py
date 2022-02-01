
import pandas as pd
import argparse
import os
import glob
from datetime import datetime


def input_parse():
    """Parse command line inputs
    Returns
    -------
    argparse_inputs: argparse.ArgumentParser
        Parse command line arguments
    """
    # Create argument parser
    argparse_inputs = argparse.ArgumentParser()

    # Command line arguments
    argparse_inputs.add_argument(
        '--date',
        type=str,
        action='store',
        help="Date of meeting in format 'YYYY-MM-DD'",
        required=True
    )

    # Parse arguments
    argparse_inputs = argparse_inputs.parse_args()

    return argparse_inputs


def read_csv_wrapper(pathto_role):
    """
    Wrapper function to read csv files

    Parameters
    ----------
    pathto_role : str
        Path to role data

    Returns
    -------
    df : DataFrame
        Pandas DataFrame of attendance data for all dates
    """
    # Import csv in folder
    path = os.getcwd()
    pathto_data = glob.glob(
        os.path.join(
            path,
            'attendance_data',
            '*.csv'
        )
    )
    try:
        df = pd.read_csv(pathto_data[0], header=1)
    except IndexError:
        raise TypeError(
            'No csv files supplied in `attendance_data` folder'
        )
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
    """
    Generate minutes table

    Parameters
    ----------
    meeting : str
        Date of meeting in format 'YYYY-MM-DD'
    df : DataFrame
        DataFrame from read_csv_wrapper function

    Returns
    -------
    df_table : DataFrame
        Minutes table
    """
    # Parse dates
    df['Start Date'] = df['Start Date'].apply(
        pd.to_datetime
    ).apply(datetime.date)
    meeting = datetime.strptime(meeting, '%Y-%m-%d').date()

    # Filter dates
    df = df[df['Start Date'] == meeting]

    # Combine senator, exec, and officer information
    df = df.fillna('')
    cols = [
        'Please select yourself',
        'Please select yourself.1',
        'Please select yourself.2',
        'Please select yourself.3',
        'Please select yourself.4',
        'Please select yourself.5',
        'Please select yourself.6',
        'Please enter your full name:',
        'Please enter your full name:.1',
        'Name'
    ]
    df['Name'] = df[cols].apply(
        lambda row: ''.join(row.values.astype(str)),
        axis=1
    )

    # Combine representative information
    cols = [
        'Please select your position:',
        'Please Select Your Affiliation',
        'Please enter your department and please add the corresponding four '
        'letter code\n\n(For example: Environmental Studies, ENVS)'
    ]
    df['Affiliation'] = df[cols].apply(
        lambda row: ''.join(row.values.astype(str)),
        axis=1
    )

    # Combine senator and respresentative information
    df['Name (Affiliation)'] = df['Name'] + ' (' + df['Affiliation'] + ')'

    # Create minutes table
    df_table = pd.DataFrame()
    position = 'Please select your GPSG Position'
    for i in df[position].unique():
        ser = df[df[position] == i]['Name (Affiliation)']
        ser = ser.reset_index(drop=True)
        ser.rename(i)
        df_table = pd.concat(objs=[df_table, ser], axis=1, ignore_index=True)
    df_table.columns = df[position].unique()

    return df_table


def main():
    # Local vars
    pathto_role = os.path.join('role_information', 'roles.csv')

    # Parse arguments
    clargs = input_parse()

    # Import data
    df = read_csv_wrapper(pathto_role)

    # Generate minutes table
    date = clargs.date
    df_minutes = get_minutes_table(date, df)
    df_minutes.to_csv(date+'_minutes.csv', index=False)


if __name__ == '__main__':
    main()
