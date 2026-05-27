import requests
import pandas as pd
from sqlalchemy import create_engine
import logging
logging.basicConfig(level=logging.INFO, filename="Logs",format='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H - %M - %S')

#=======================================
#Extract Processs...
#=======================================
def extract():

    try:                                            #Error might occured in this block

        url = "https://fakestoreapi.com/products"      #Api URL 

        response = requests.get(url)            #Using request to get the data

        data = response.json()                  #Converting the data into json data file format

        df = pd.DataFrame(data)                 #Converting that data into dataframe using pandas  

        Customers = pd.read_csv("D:\\xamp\\htdocs\\Data Enginner_Projects\\Orders_Project_Using_CSV And API\Customers.csv")         #Put the csv file path in the bracket

        return Customers,df

    except FileNotFoundError as e:                    #The error information is displayed by this block

        logging.error(f"File Could not found {e}")
        return None, None

    finally:                              #This block will run every time pipeline execute

        logging.info("Extract process is completed successfully")


#=========================================    
#Transformation Process.....
#=========================================

def transform(Customers,df):              

    try:

        Customers["City"] = Customers["City"].fillna("Unknown")            #Handle null value using fillna function 

        Customers["City"] = Customers["City"].str.lower()           #formated the string by using lower function

        Customers["Age"] = Customers["Age"].fillna(Customers["Age"].mean())    #Handle null values of using the fillna function

        Customers["Membership"] = Customers["Membership"].fillna("Bronze")        #Handle null values by using the fillna function

        Customers["Age_Category"] = Customers["Age"].apply(lambda x: "Teenager" if x < 18 else "Adult" if x < 60 else "Senior_Citizen")    #Did feature engineering 

        df["title"] = df["title"].fillna("Unknown")       #Handle null  values using the fillna function

        df = df.drop(["description","image","rating"], axis = 1)      #Drop the columns which we not required

        df = df[df["category"].isin(["men's clothing","women's clothing"])]     #Filter the required data 

        return Customers,df


    except KeyError as e:

        logging.error(f"The Column colud not be found {e}")          #Error handaling 
        return Customers,df

    finally:

        logging.info("Transform process is completed") 

#==================================
# Load Process......
#==================================

def load(Customers,df):

    try:

        conn = create_engine(
            "mysql+pymysql://root:root@localhost:3306/practice"      #Path of database to store the data
            )

        Customers.to_sql("customers_data",conn,        #Store Customers transform values in Database name as customers_data
                         if_exists = "replace",
                         index = False)
        
        df.to_sql("products_data",conn,          #Store products transform values in Database name as products_data
                  if_exists = "replace",
                  index = False)
        
        logging.info("Data is loaded Successfully")      #Conformation of data Successfully loaded

    except Exception as e:

        logging.error(f"Error during load {e}")         #Error handaling


    finally:

        logging.info("Load Process is Completed")        #Load process completed


#================================
# Main pipeline
#================================

Customers,df = extract()         #Extract the data 

if Customers is not None and df is not None:     #Check if there are any None Values

    Customers,df = transform(Customers,df)       #Transform process execute here
    load(Customers,df)               #Load process is executed here

else:

    logging.error("None Values are present in Data")

logging.info("Pipeline is Successfully Executed")     #pipeline process runs successfully conformation








    






