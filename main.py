import io
import os
import openpyxl
import requests
import pandas as pd
import shutil


def create_necessary_folders():
    required_folders = ['weather_data', 'excel_files']
    for folder in required_folders:
        # clean data from weather_data folder
        try:
            if os.path.isfile(folder) or os.path.islink(folder):
                os.unlink(folder)
            elif os.path.isdir(folder):
                shutil.rmtree(folder)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (folder, e))

        path = os.path.join(folder)
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok=True)
                print(f"Directories '{path}' created successfully")
            except OSError:
                print(f"Directories '{path}' can not be created")


def retrieve_data(file_name, location_name):
    df = pd.read_csv(file_name, header=2)
    df_filtered = df[df['Name'] == location_name]
    return df_filtered.reset_index(drop=True)


def request_weather_data(station_id, station_name, year=2000, past_three_years=False):

    if past_three_years:
        for select_year in range(year-2, year+1):
            url = f"https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={station_id}&Year={select_year}&Month=12&Day=14&timeframe=2&submit=Download+Data"
            r = requests.get(url).content
            df = pd.read_csv(io.StringIO(r.decode('utf-8')))
            df.to_csv(f"./weather_data/{station_name}_{select_year}_weather_data.csv")

    else:
        url = f"https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={station_id}&Year={year}&Month=12&Day=14&timeframe=2&submit=Download+Data"
        r = requests.get(url).content
        df = pd.read_csv(io.StringIO(r.decode('utf-8')))
        df.to_csv(f"./weather_data/{station_name}_{year}_weather_data.csv")


def solve_exercises(file_path, location_name, exercise_number):
    # go through each csv file in given file path
    for file in os.listdir(file_path):
        if file.endswith(".csv"):
            with open(os.path.join(file_path, file), 'r'):
                # read file
                csv_file = pd.read_csv(f"{file_path}/{file}", sep=',')
                # clean up rows that doesn't have any temperature value
                csv_file = csv_file[csv_file['Max Temp (°C)'].notnull()].reset_index(drop=True)
                year = csv_file['Year'][0]
                csv_file['Climate ID'] = csv_file['Climate ID'].apply(str)
                df_station_inv['Climate ID'] = df_station_inv['Climate ID'].apply(str)
                if exercise_number == 1:
                    merged_results = pd.merge(df_station_inv, csv_file, how='right', on='Climate ID')
                    if os.path.isfile(f"./excel_files/{location_name}_output.xlsx"):
                        book = openpyxl.load_workbook(f'./excel_files/{location_name}_output.xlsx')
                        writer = pd.ExcelWriter(f'./excel_files/{location_name}_output.xlsx', engine='openpyxl')
                        writer.book = book
                        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
                        merged_results.to_excel(
                            writer,
                            sheet_name=f"{year}",
                            index=False,
                            header=True
                        )
                        writer.save()

                    else:
                        merged_results.to_excel(f"./excel_files/{location_name}_output.xlsx", sheet_name=f"{year}")
                else: # when exercise number = 2
                    print(f"Max temp for given year is: {csv_file['Max Temp (°C)'].max()}")
                    print(f"Min temp for given year is: {csv_file['Min Temp (°C)'].min()}")
                    print(f"Average temp per month per year is:\n")
                    print(f"{csv_file[['Month', 'Mean Temp (°C)']].groupby('Month').mean()}")
                    print(f"Average Temperature overall for year is: {csv_file['Mean Temp (°C)'].mean()}")


if __name__ == '__main__':

    # read data from station_inventory_file for TORONTO
    df_station_inv = retrieve_data(file_name="station_inventory_en.csv",
                                   location_name="TORONTO CITY")
    # pull out station_id to be used later.
    station_id = df_station_inv['Station ID'][0]
    station_name = df_station_inv['Name'][0]

    # create the necessary folders
    create_necessary_folders()

    # ask for year
    year = int(input("Please enter a year you'd like the data for:\n"))

    # ask for exercise number
    exercise_number = int(input("Please enter the exercise number you'd like to do.\n"
                                "Exercise 1 will give you past 3 years data.\n"
                                "Exercise 2 will give you only the data for given year.\n"))

    past_three_years = False
    if exercise_number == 1:
        past_three_years = True

    # download data for stationID and year
    request_weather_data(station_id=station_id, station_name=station_name, year=year,
                         past_three_years = past_three_years)

    # assign file_path as the folder for weather_data
    file_path = "./weather_data"

    solve_exercises(file_path=file_path, location_name=station_name, exercise_number=exercise_number)


