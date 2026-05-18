# imported the pandas,numpy,logging and sqlalchemy
import pandas as pd
import logging                  #Using logging insted of print to conform keep record of pipeline execution
import numpy as np
logging.basicConfig(filename="logs", level=logging.INFO)       #The Configuration of logging  "Filename" Save the logs in logs Folder if not present make one 
from sqlalchemy import create_engine

#Extract CSV Files

def extract():

    try:
     
     logging.info("Extracting files....")

     suppliers = pd.read_csv("suppliers.csv")      #Read the suppliers csv file

     inventory = pd.read_csv("inventory.csv")      # Read the inventory csv file

     purchase_orders = pd.read_csv("purchase_orders.csv")   #Read the purchase_orders csv file

     production = pd.read_csv("production.csv")      #Read the production csv files

     return suppliers,inventory,purchase_orders,production      #Reaturn the output

    except FileNotFoundError as e:
       
       logging.error(f"File is not available !! {e}")          #Expected Error 
       return None,None,None,None

    finally:
       
       logging.info("Extracting is success")              #Conformation of completing the extract process


#Transforming the data

def transform(suppliers,inventory,purchase_orders,production):         
   
   try:
      
      logging.info("Transformation Started.....")              #Starting Transform Process
      
      suppliers["Email"] = suppliers["Email"].fillna("not_provided")         #Filled The None values in Email with not_provided

      suppliers["Contact_Person"] = suppliers["Contact_Person"].fillna("Unknown")       #Filled The None values in Contact_Person with Unknown

      suppliers = suppliers[suppliers["Status"] == "Active"]        #Filter only those columns who has active status

      suppliers["City"] = suppliers["City"].str.capitalize()        # fix the format of string to capitalize

      inventory["Selling_Price"] = inventory["Selling_Price"].fillna(inventory["Selling_Price"].mean())     #Filling the None values with  average value of Selling_Price 

      inventory["Unit_Cost"] = inventory["Unit_Cost"].fillna(inventory["Unit_Cost"].mean())        #Filling the None Values with average value of Unit_Cost

      inventory["Profit_Margin"] = inventory["Selling_Price"] - inventory["Unit_Cost"]           # Calculating the profit using selling price and unit cost columns

      inventory["Profit_Percent"] = inventory["Profit_Margin"] / inventory["Unit_Cost"] * 100     #Calculating the profit percentage by using profit margin column and unit cost multiply by 100
 
      inventory["Stock_Status"] = inventory.apply(lambda x: "Reorder Needed" if x["Stock_Quantity"] < x["Reorder_Level"] else "Sufficient", axis = 1)     #Categorizing the inventory table to get stock status use stock quantity and recorder level

      inventory = inventory.drop(columns = ["Status"])      #Drop the Status column so there wont be duplicate columns when loading into sql

      purchase_orders["Actual_Delivery"] = purchase_orders["Actual_Delivery"].fillna("Pending")      #Filling the None values in Actual Delivery with pending

      purchase_orders["Quality_Check"] = purchase_orders["Quality_Check"].fillna("Pending")        #Filling the None Values in Quality check with Pending

      purchase_orders["Unit_Price"] = purchase_orders["Unit_Price"].fillna(purchase_orders["Unit_Price"].mean())        #Filling the None values with Unit_Price Average values 

      purchase_orders["Delivery_Status"] = purchase_orders.apply(lambda x: "Not Delivered" if x["Actual_Delivery"] == "Pending" else "On Time" if x["Actual_Delivery"] <= x["Expected_Delivery"] else "Delayed", axis = 1)     #Categorize the purchase orders using lambda to get Delivery status

      purchase_orders = purchase_orders.drop(columns = ["Status"])      #Droping the Status column to avoid duplicate error fearther on while loading into sql

      production["Actual_Quantity"] = production["Actual_Quantity"].fillna(0)   #Filled integer value 0 into None values in column Actual Quantity

      production["Production_Cost"] = production["Production_Cost"].fillna(production["Production_Cost"].mean())       #Filled the None values in production cost column with ites own average value

      production["Defect_Rate"] = np.where(production["Actual_Quantity"] > 0,(production["Defective_Units"] / production["Actual_Quantity"]) * 100,0)    #Use Numpy where function to categorize the production table and get total defect rate overall

      production["Quality_Grade"] = production["Defect_Rate"].apply(lambda x: "Excellent" if x < 1 else "Good" if x < 3 else "Needs Improvement")

      production = production.drop(columns = ["Status"])   #Drop the column status for fearther duplicate issues

      df = pd.merge(suppliers,purchase_orders,
                    on = "Supplier_ID",
                    how = "inner",
                    suffixes=("_supplier","_purchase"))          #Mearge the Suppliers and purchase orders
      
      df = pd.merge(df,production,
                    on = "Product_ID",
                    how = "inner",
                    suffixes=("","_production"))           #Mearge the production table with othere tables
      
      df = pd.merge(df,inventory,
                    on = "Product_ID",
                    how = "inner",
                    suffixes=("","inventory"))          #Mearge the inventory table with other tables
      
      df["Total_Value"] = df["Unit_Price"] * df["Quantity_Ordered"]          #Get the total values using unit prise column and quantity ordered

      return df

   except KeyError as e:
      
      logging.error(f"Column not find {e}")         

   finally:
      
      logging.info("Transformation is completed successfully")         #Conformation the Transformation process is completed 

# Loading the data into MySQL
def load(df):
   
   try:
     
     logging.info("Data Start to load.....")              #Starting of Load process
   
     conn = create_engine(
      
        "mysql+pymysql://root:root@localhost:3306/practice"       #MySQL Connection Info

     )

     df.to_sql("supply_chain_analytics1",conn,        #Table name and connection
              if_exists = "replace",          #if existed replace with current output
              index = False)
   except Exception as e:
      
      logging.error(f"Data Failed to load !! {e}")

   finally:
      
      logging.info("Data Loaded Successfully !!")        #End of Loading process into MySQL

suppliers,inventory,purchase_orders,production = extract()        

filter_df = transform(suppliers,inventory,purchase_orders,production)  

if filter_df is not None:          #Making sure that there are no None values in filter_df
   
   load(filter_df)

else:
   
   logging.error("Loading Failed !!")






      

   


   




    

