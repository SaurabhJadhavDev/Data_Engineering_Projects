import pandas as pd

data = {

    "City":["Pune","Mumbai","Delhi","Bangaloru","Chennai","Kolkata","Hyderabad","Ahmedabad","jaipur","Lucknow"],
    "State":["Maharashtra","Maharashtra","Delhi","Karnataka","Tamil Nadu","West Bengal","Telangana","Gujarat","Rajasthan","Uttar Pradesh"],
    "Population":[7,20,19,12,11,15,10,8,4,3.5],
    "Area":[331,603,1484,709,426,205,650,464,485,631],
    "Literacy_Rate":[89,89,86,88,90,87,84,88,87,84],
    "Hospitals":[120,300,250,200,150,180,170,100,80,70],
    "Schools":[900,2000,1800,1500,1200,1400,1300,850,600,500],
    "GDP":[69,310,293,110,78,150,74,68,24,20]
}

df = pd.DataFrame(data)

df.to_csv("City_Demographics.csv",index = True,index_label = "RowID")
