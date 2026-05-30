#========================
#Requirements 
#========================

import pandas as pd        #Pandas Library
import numpy as np         #Numpy Library
import requests            #Requests for featching the API
import logging             #Logging for tracking the execution
logging.basicConfig(level=logging.INFO,filename="Logs",format= '%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m -%d   %H-%M-%S')     #Format of the logging 
import os                  #Os for avoiding hardcoding
from sqlalchemy import create_engine      #Create_engine from sqlalchemy for loading data in SQL Database
from dotenv import load_dotenv       #Imported load_dotenv for avoiding hardcoding links and paths
load_dotenv()

#==============================
#Extract Proceess
#==============================


def extract():                         #Function Block for Extract Process

    try:
        logging.info("Extract Process is Executed......")        #This block will conform the start of extract process

        City_Demo = pd.read_csv("City_Demographics.csv")            #Read CSV File 

        City_Infra = pd.read_json("City_infrastructure.json")      #Read JSON File

        cities = City_Demo["City"].tolist()       #Select the Required Weather info of perticular cities
 
        weather_list = []              #Empty Weather_list for putting the wheather details of each cities

        API_KEY =os.getenv("API_KEY")       #Putting the API_KEY for accessing the weather api account

        for city in cities:          #USing For loop for extracting each city information 

            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"          #URL of the weather api

            response = requests.get(url)           #getting the response from the url

            if response.status_code == 200:         #Checking if the URL is fetch properly

                Data = response.json()           #Converting into Json format once api is extracted

                weather_list.append({                #Appending the information of each selected city into empty weather_list
                   "City":city,                                #City Name
                   "Temperature":Data["main"]["temp"],         #City Temperature
                   "Humidity": Data["main"]["humidity"],          #Humidity of the City
                   "Condition": Data["weather"][0]["description"]       #Condition of the overall weather in that city
               })
        
            else:

              logging.error(f"API Failed for {city}:{response.status_code}")         #Error block that shows API has failed to load

        Weather_df = pd.DataFrame(weather_list)         #Converting the Json file into pandas dataframe format to fearther proccessing

        return City_Demo,City_Infra,Weather_df       #Returning the overall result

    except FileNotFoundError as e:                 #If file not found or if file is missing this error will display the error message
 
        logging.error(f"The Required File is Missing {e}")
        return None,None,None

    finally:

        logging.info("Extract process execution is completed")        #This Block will conform the end of the extract method

#============================
# Transformation process
#============================

def transformation(City_Demo,City_Infra,Weather_df):

    try:

        logging.info("Transformation process is executed....")

# City_Demographics.CSV File Transformation

        City_Demo["Population"] = City_Demo["Population"].fillna(City_Demo["Population"].mean())               #--------|
                                                                                                               #        |----> Handaling Null values by using the there average values for avoiding wrong data analysis 
        City_Demo["Literacy_Rate"] = City_Demo["Literacy_Rate"].fillna(City_Demo["Literacy_Rate"].mean())      #--------|

        City_Demo["GDP"] = City_Demo["GDP"].fillna(0)             # Giving 0 to Null values to avoid skewing averages

        City_Demo["City"] = City_Demo["City"].str.strip().str.title()        # Standardize the city names by removing the extra spaces and converting to title case

        City_Demo["Pop_Density"] = (City_Demo["Population"]* 1000000 / City_Demo["Area"]).round(2)          # Calculate population density (people per km2) to compare city crowding

        City_Demo["City_Tier"] = City_Demo["Population"].apply(lambda x: "Tier 1" if x >= 10 else "Tier 2" if x >= 5 else "Tier 3")      # Categorizing the City in tiers 1 , 2, 3 depending on its population size

        City_Demo["Literacy_Label"] = City_Demo["Literacy_Rate"].apply(lambda x: "Highly Educated" if x >= 88 else "Educated" if x >= 50 else "Developing")     # Classify cities by literacy rate into "Highly educated","Educated" and "Developing"

        City_Demo["GDP_Category"] = City_Demo["GDP"].apply(lambda x: "High GDP" if x >= 200 else "Medium GDP" if x >= 50 else "Low GDP")         # Categorizing the GDP in (High GDP, Medium GDP and Low GDP) as per billions/millions. 

# City_infrastructure.json File Transformation

        City_Infra["City"] = City_Infra["City"].str.strip().str.title()       # Normalize city names in infrastructure data to ensure consistency for marging

        City_Infra["smart_city_score"] = City_Infra["smart_city_score"].fillna(0)         # Filling the missing values in smart_city_score by 0 to avoid error in scoring
                                                                                          
        City_Infra["ev_charging_stations"] = City_Infra["ev_charging_stations"].fillna(0)      # Filling the missing values in ev_charging_stations by 0 to avoid error in scoring

        City_Infra["Smart_City_Label"] =  np.where(City_Infra["smart_city_score"] >= 85, "Excellent",np.where(City_Infra["smart_city_score"] >= 75, "Good",np.where(City_Infra["smart_city_score"] >= 65,"Average", "Developing")))       # Categorizing the Cities infrastructure by (Excellent,Good,Average and Developing) for clear understanding of cities 

        City_Infra["Infra_Score"] = (City_Infra["metro_lines"]*10 + City_Infra["airports"]*5 + City_Infra["railway_stations"]*2 + City_Infra["ev_charging_stations"]*0.1).round(2)          # Giving scores on the basis of city infrasturcture on the basis of facility provided within each cities

        City_Infra["EV_Readiness"] = np.where(City_Infra["ev_charging_stations"] >= 300,"High",np.where(City_Infra["ev_charging_stations"] >= 150,"Medium","Low"))         # By using numpy where function  we are categorizing the cities ev_facilities in (High,medium and low)

# Weather_API Transformation

        Weather_df["City"] = Weather_df["City"].str.strip().str.title()         # Normalizing the cities in wheather api for properly merging 

        Weather_df["Temp_Label"] = np.where(Weather_df["Temperature"] >= 35,"Very Hot",np.where(Weather_df["Temperature"] >= 28,"Hot",np.where(Weather_df["Temperature"] >= 20,"Pleasant","Cold")))        # Categorize the cities temeperature by (Very Hot,Hot,Pleasent and Cold) as per city temperature in percentage

        Weather_df["Humidity_Label"] = np.where(Weather_df["Humidity"] >= 80,"High Humidity",np.where(Weather_df["Humidity"] >= 50,"Moderate","Low Humidity"))      # Categorize the city humiidity level in (High Humidity,Moderate and Low Humidity) as per humidity level in each cities

        Weather_df["Condition"] = Weather_df["Condition"].str.title()       # Converting Condition in title case for clear looks

        Weather_df["Weather_Score"] = np.where(Weather_df["Temperature"].between(20,30),100 - Weather_df["Humidity"]*0.5,100 - Weather_df["Humidity"] * 0.5 - 10).round(2)   # Derive the weather score  for livability analysis,balancing temperature comfort and humidity 

# Mearging the three tables and normalizing the data overall

        df = pd.merge(City_Demo,City_Infra,        # Mearging the City_Demo CSV file and City_Infra JSON file by city in inner join 
                      on = "City",
                      how = "inner")
        
        df = pd.merge(df,Weather_df,               # Mearging the previously mearged files and Weather API by city and Using left join for handaling the null values carefully
                      on = "City",
                      how = "left")
        
        df["Overall_City_Score"] = (df["smart_city_score"]*0.4 + df["Literacy_Rate"]*0.3 + df["Weather_Score"]*0.3).round(2)        # Giving each city the final score based on it's (smart_city_score,literacy rate and its weather_score)

        df["investment_Potential"] = df.apply(lambda x:"High" if x["City_Tier"] == "Tier 1" and x["Smart_City_Label"] in ["Excellent","Good"] else "Medium" if x["City_Tier"] == "Tier 2" else "Low", axis = 1)    # Classifed the city in there (city_tier and smart_city_label) and putting them in (High,Medium and Low) category for investement

        df["Livability_Score"] = (df["Literacy_Rate"] * 0.3 + df["smart_city_score"] * 0.4 + df["Hospitals"] * 0.01 + df["Schools"] * 0.001).round(2)      # giving each cities livability score as per its facility available for citizens

        df["City_Rank"] = df["Overall_City_Score"].rank(ascending=False).fillna(0).astype("Int64")       # Giving final rank to each cities as per overall city score and also using (int64) to handale null values if present while marging the data

        return df
    
    except KeyError as e:        # Handaling the KeyError of column not found error 

        logging.error(f"Colunm not found: {e}")
        return None

    except AttributeError as e:     # Handaling the AttributeError like error if there is null values present in string

        logging.error(f"Null values causes string operations failure: {e}")
        return None

    finally:

        logging.info("Transformation  process is completed")          #Conformation of completion of Transformation process

#========================
#Load process 
#========================

def load(df):

    try:
        logging.info("Load Process Started.....")         # Conformation of starting the load process

        conn = create_engine(                     # Use create_engine from sqlalchemy to load data in mysql alos use envirnomental variable for avoiding hardcoding
            f"mysql+pymysql://"
            f"{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:"
            f"{os.getenv('DB_PORT')}/"
            f"{os.getenv('DB_NAME')}"
        )

        df.to_sql("india_smart_city_analytics",conn,         # Use to_sql of pandas function to load data into mysql and name it 
                  if_exists = "replace",
                  index = False)
        
        logging.info("Data Load Successfully")           # Conformation that data is loaded into mysql

    except Exception as e:          # Handalad Exception error by using exception handaling

        logging.error(f"Load Failed:{e}")

    finally:
        try:
          conn.dispose()           # Use dispose to dissconnect the sql connection to avoid data loss
        except:
            pass
        logging.info("Load Process Completed")          # Conformation of complection of data loading

#===================
#Run Pipeline
#===================

City_Demo,City_Infra,Weather_df = extract()            #Calling extract function 

if City_Demo is not None:                # using conditional statements to make sure City_Demo does not have any None Values

    df = transformation(City_Demo,City_Infra,Weather_df)          # Calling transformation process 

    if df is not None:                 # Handaling None value using conditional sstatement

        load(df)               # Calling load process 
    
    else:

        logging.error("Transform Failed!")      

else:

    logging.error("Extract Failed!")

logging.info("Pipeline Execution Completed!")         # Conformation pipeline is executed completely



    


    