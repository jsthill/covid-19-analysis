# This downloads data from the CDC data source using an API 
# and loads that data into a SQLite database.
# Author: Julian St. Hill
# Date: 04/21/2022

import sqlite3
import json
import ssl
import urllib.request, urllib.parse, urllib.error

from numpy import empty

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Create database
conn = sqlite3.connect('covid19.sqlite')
cur = conn.cursor()

# Prompt the user to know if to do a reset.
reset = input('Restart process (y/n)? ')
if (reset is not None or reset != '') and reset.lower() == 'y':
    # Drop the Cases table 
    cur.execute('DROP TABLE IF EXISTS Cases')
    conn.commit()

# Create table to store raw data if it doesn't exist.
cur.execute('''CREATE TABLE IF NOT EXISTS Cases
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    case_month TEXT, 
    res_state TEXT,
    state_fips_code INTEGER,
    res_county TEXT,
    county_fips_code TEXT,
    age_group TEXT,
    sex TEXT,
    race TEXT,
    ethnicity TEXT,
    case_positive_specimen_interval INTEGER,
    case_onset_interval INTEGER,
    process TEXT,
    exposure_yn TEXT,
    current_status TEXT,
    symptom_status TEXT,
    hosp_yn TEXT,
    icu_yn TEXT,
    death_yn TEXT,
    underlying_conditions_yn TEXT)''')

def uploadData(row):
    case_month = row['case_month']
    res_state = row['res_state']
    state_fips_code = row['state_fips_code']
    res_county = row['res_county']
    county_fips_code = row['county_fips_code']
    age_group = row['age_group']
    sex = row['sex']
    race = row['race']
    ethnicity = row['ethnicity']
    process = row['process']
    exposure_yn = row['exposure_yn']
    current_status = row['current_status']
    symptom_status = row['symptom_status']
    hosp_yn = row['hosp_yn']
    icu_yn = row['icu_yn']
    death_yn = row['death_yn']
    underlying_conditions_yn = ''

    sql = '''INSERT INTO Cases 
        (case_month, res_state, state_fips_code, res_county, county_fips_code, age_group,
        sex, race,ethnicity, process, exposure_yn, current_status, symptom_status,
        hosp_yn, icu_yn, death_yn, underlying_conditions_yn)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    cur.execute(sql,
        (case_month, res_state, state_fips_code, res_county, county_fips_code, age_group,
        sex, race, ethnicity, process, exposure_yn, current_status, symptom_status,
        hosp_yn, icu_yn, death_yn, underlying_conditions_yn)
    )

# Commit all remainding records and close connection.
def exit_app():
    conn.commit()
    cur.close()
    conn.close()
    exit()

# Prepare to grab the data from CDC and upload it.
serviceurl = 'https://data.cdc.gov/resource/n8mc-b4w4.json?$'

# Prompt the user as to how many rows of data to retrieve.
rows = input('How many lines of data to process? ')
if len(rows) < 1:
    exit()

int_row = int(rows)

param = dict()
param['limit'] = int_row
url = serviceurl + urllib.parse.urlencode(param)

try:
    document = urllib.request.urlopen(url, context=ctx)
    # Read and decode the data.
    data = document.read().decode()
except KeyboardInterrupt:
    print('')
    print('Process interrupted via keyboard.')
    exit_app()
except:
    print('Error reaching', url + '. Please try another source.')
    exit_app()

print('Uploading data from', url, '.....')

# Load data into JSON object
try:
    js = json.loads(data)
    # print('Length of js:', len(js))
except:
    print('Error loading JSON data.')
    exit_app()

# Upload the records committing every 1000.
numrec = 0
for row in js:
    try:
        uploadData(row)
    except KeyboardInterrupt:
        print('')
        print('Upload process interrupted by keyboard input.')
        exit_app
    except:
        pass
    int_row -= 1
    numrec += 1

    if int_row % 1000 == 0:
        # print(str(numrec), 'records commited to the database.')
        conn.commit()

    if int_row == 0:
        break

exit_app()
