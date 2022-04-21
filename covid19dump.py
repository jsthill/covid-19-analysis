# This script creates a json data file to be used as input for visualization.
# Author: Julian St. Hill
# Date: 04/21/2022

import sqlite3

# Create connections
conn = sqlite3.connect('covid19.sqlite')
cur = conn.cursor()

def writeData(cur):
    cols = len(cur.description)
    for row in cur:
        # print(row)
        if cols == 2:
            fhandle.write(",\n['" + row[1] + "'," + str(row[0]) + "]")
        elif cols == 3:
            fhandle.write(",\n['" + row[1] + "'," + "'" + row[2] + "'," + str(row[0]) + "]")
    fhandle.write("\n];\n")   

# Open file for writing.
fhandle = open('covid19_data.js','w')
fhandle.write("bystate = [['State', 'Cases']")
# Get cases by state.
cur.execute('SELECT count(res_state) Count, res_state From Cases GROUP By res_state')
writeData(cur)

# Cases by month
cur.execute('SELECT count(case_month) Count, case_month From Cases GROUP By case_month')
fhandle.write("bymonth = [['Month', 'Cases']")
writeData(cur)

# Cases by month and by state
cur.execute('SELECT count(case_month) Count, case_month, res_state From Cases GROUP By case_month, res_state ORDER By count(case_month) DESC LIMIT 25')
fhandle.write("bymonthstate = [['Month','State','Cases']")
writeData(cur)

# Cases by age group
cur.execute('SELECT count(age_group) as Count, age_group FROM Cases GROUP By age_group')
fhandle.write("byagegroup = [['Age Group', 'Cases']")
writeData(cur)

# Cases by age group
cur.execute("SELECT count(death_yn) as Count, age_group FROM Cases WHERE death_yn = 'Yes' GROUP By age_group")
fhandle.write("byagegroupdeaths = [['Age Group', 'Deaths']")
writeData(cur)

fhandle.close()

cur.close()
conn.close()