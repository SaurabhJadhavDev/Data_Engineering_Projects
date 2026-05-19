import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging
logging.basicConfig(filename="Logs_Outputs",level= logging.INFO,format= '%(asctime)s - %(levelname)s - %(message)s',datefmt= '%Y-%m-%d  %H:%M:%S')

#Extract Data From MySQl
def Extract():

    try:

     connection = create_engine(

        "mysql+pymysql://root:root@localhost:3306/Ecommerce_etl"
     )

     Customers = pd.read_sql("Select * From Customers",connection)

     Orders = pd.read_sql("Select * From Orders",connection)

     Order_Items = pd.read_sql("Select * From Order_Items",connection)

     Products = pd.read_sql("Select * From Products",connection)

     return Customers,Orders,Order_Items,Products
    
    except FileNotFoundError as e:
       
       logging.error(f"File Could Not be Found{e}")
       return None,None,None,None
    
    finally:
       
       logging.info("Extract Process is Complete!")

#Transforming 
def Cleaning(Customers,Orders,Order_Items,Products):

    try:

      logging.info("Transforming process is started....")

      Customers["Email"] = Customers["Email"].fillna("not_provided@gmail.com")

      Customers["City"] = Customers["City"].str.title()

      Products["Stock"] = Products["Stock"].fillna(0)

      df = pd.merge(Customers,Orders,
                    on = "Customer_ID",
                    how = "inner")
    
      df = pd.merge(df,Order_Items,
                    on = "Order_ID",
                    how = "inner")
    
      df = pd.merge(df,Products,
                    on = "Product_ID",
                    how = "inner")
    
      df["Total_Values"] = df["Price"] * df["Quantity"]

      df["Tax"] = df["Total_Values"]*0.18

      df["Final_Value"] = df["Total_Values"] + df["Tax"]

      df = df[df["Status"] == "delivered"]

      df["Order_Size"] = np.where(df["Total_Values"] > 100000,"High", np.where(df["Total_Values"] > 50000,"Medium","Low"))
 
      return df
    
    except KeyError as e:
       
       logging.error(f"The column could not find {e}")

    finally:
       
       logging.info("The Transformation process is Complete")

# Load Data into MySQL

def Load(df):

    try:

      conn = create_engine(

          "mysql+pymysql://root:root@localhost:3306/Ecommerce_etl"
      )

      df.to_sql("clean_data2020",conn,
                if_exists = "replace",
                index = False)
    
    except KeyError as e:
       
       logging.error("Data failed to load {e}")

    finally:
       
       logging.info("Data loaded successfully")



Customers,Orders,Order_Items,Products = Extract()

Clean = Cleaning(Customers,Orders,Order_Items,Products)

if Clean is not None:
   
    Load(Clean)

else:
   
   logging.info("Data Failed to load")
   
