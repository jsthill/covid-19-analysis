# covid-19-analysis
This project is done using Python. It analyses data from CDC on COVID-19 cases.

<!-- How it works -->
Data is retrieved from the CDC using their provided API. The Python file grabdata.py 
calls the API "https://data.cdc.gov/resource/n8mc-b4w4.json?$" to get the data and loads 
it into a local database (SQLite). 

Prior to calling the API the program first asks the user if to reset. If the user types
anything except "Y" or "y" the program will ignore the input and continue processing. 
However if the user types "y" the program will drop the Cases table if it exists.

The Cases table is created if it was dropped or if the program is being run for the first time. Next the user is prompted to enter the number of records to retrieve from the CDC data source. Please note the more records requested the more time it will take to download. The sample data provided only contains 700,000 records. This is a very small subset of the 65M plus records available for download.

After loading the data into the database the next step is to create a data file with data models for each visualization. This is done by running the Python program covid19dump.py which creates the JSON file covid19_data.js.

Finally to view the data open index.html in the browser.

To view the sample data follow these steps.

1. Download the covid19_data.js and index.html files to a folder on your computer.
2. Open the index.html file in your browser. Please note both files must be located in the same folder.

To run the full process follow these steps. The assumption is made that you have Python3 installed on your computer.

1. Download grabdata.py, covid19dump.py and index.html to a folder on your computer.
2. Run grabdata.py and follow the prompts.
3. Run covid19dump.py
4. Open index.html

Please note if you don't want to run step 2 above to download data from the CDC source you can download the database covid19.sqlite.zip and uncompress it.
