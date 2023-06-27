import glob 
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime
import psycopg2

tmpfile    = "dealership_temp.tmp"       # store all extracted data
logfile    = "dealership_logfile.txt"       # all event logs will be stored
targetfile = "transformed_data.csv"   # transformed data is stored 

def extract_from_csv(file_to_process): 
    dataframe = pd.read_csv(file_to_process) 
    return dataframe

def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process,lines=True)
    return dataframe 

def extract_from_xml(file_to_process): #uses the ET.parse() function from the ElementTree library to parse the XML file and create an XML tree object.
    rows = []
    tree = ET.parse(file_to_process)
    root = tree.getroot() # root of the XML tree is obtained using the tree.getroot() method.
    for person in root: #iterate over each person element in the XML file.
        car_model = person.find("car_model").text
        year_of_manufacture = int(person.find("year_of_manufacture").text)
        price = float(person.find("price").text)
        fuel = person.find("fuel").text
        row = {"car_model": car_model, "year_of_manufacture": year_of_manufacture, "price": price, "fuel": fuel}
        rows.append(row)
    dataframe = pd.DataFrame(rows)
    return dataframe

def extract():
    # creating an empty dataframe, this dataframe will store all the extracted values.
    extracted_data = pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])
    # For csv files, iterates through all csv files
    for csvfile in glob.glob("extract/*.csv"):
        extracted_data = pd.concat([extracted_data, extract_from_csv(csvfile)], ignore_index=True)
    # For json files
    for jsonfile in glob.glob("extract/*.json"):
        extracted_data = pd.concat([extracted_data, extract_from_json(jsonfile)], ignore_index=True)
    # For xml files
    for xmlfile in glob.glob("extract/*.xml"):
        extracted_data = pd.concat([extracted_data, extract_from_xml(xmlfile)], ignore_index=True)
    return extracted_data

def transform(data):
       data['price'] = round(data.price, 2)
       return data

def load(targetfile,data_to_load):
    data_to_load.to_csv(targetfile) 

def log(message):
    timestamp_format = '%H:%M:%S-%h-%d-%Y'
    #Hour-Minute-Second-MonthName-Day-Year
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("dealership_logfile.txt","a") as f: f.write(timestamp + ',' + message + 'n')

def rename_column(filename, new_column_name):
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(filename)

    # Update the first column name
    df.rename(columns={df.columns[0]: new_column_name}, inplace=True)

    # Save the DataFrame back to a CSV file
    df.to_csv(filename, index=False)

def load_to_postgres(targetfile):
    conn = psycopg2.connect(database="etl",
                        user='postgres', password='postgres',
                        host='127.0.0.1', port='5432')

    cursor = conn.cursor()
    # Create the table
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS car_price (
            sr_no VARCHAR(5),
            car_model VARCHAR(200),
            year_of_manufacture VARCHAR(200),
            price VARCHAR(50),
            fuel VARCHAR(50)
            
        )
    '''
    cursor.execute(create_table_query)

    # Load data from CSV
    with open(targetfile, 'r') as file:
        cursor.copy_from(file, 'car_price', sep=',', columns=('sr_no','car_model', 'year_of_manufacture', 'price', 'fuel'))

    # Fetch and print the data
    select_query = "SELECT * FROM car_price"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.commit()
    conn.close()


log("ETL Job Started")

# extract 
log("Extract phase Started")
extracted_data = extract() 
log("Extract phase Ended")

# transform 
log("Transform phase Started")
transformed_data = transform(extracted_data)
log("Transform phase Ended")

# load 
log("Load phase Started")
load(targetfile,transformed_data)
new_column_name = "sr_no"
rename_column(targetfile, new_column_name)
load_to_postgres(targetfile)
log("Load phase Ended")

log("ETL Job Ended")