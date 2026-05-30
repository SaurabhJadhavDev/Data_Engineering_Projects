import json

data = [

    {
        "City":"Pune",
        "roads_km":2500,
        "metro_lines":2,
        "airports":1,
        "railway_stations":8,
        "smart_city_score":72,
        "ev_charging_stations":145
    },

    {
        "City":"Mumbai",
        "roads_km":1900,
        "metro_lines":3,
        "airports":2,
        "railway_stations":25,
        "smart_city_score":85,
        "ev_charging_stations":380
    },

    {
        "City":"Delhi",
        "roads_km":2100,
        "metro_lines":10,
        "airports":2,
        "railway_stations":35,
        "smart_city_score":88,
        "ev_charging_stations":420
    },

    {
        "City":"Bangaloru",
        "roads_km":1600,
        "metro_lines":2,
        "airports":1,
        "railway_stations":22,
        "smart_city_score":80,
        "ev_charging_stations":250
    },

    {
        "City":"Hyderabad",
        "roads_km":1400,
        "metro_lines":1,
        "airports":1,
        "railway_stations":18,
        "smart_city_score":81,
        "ev_charging_stations":220
    },

    {
        "City":"Chennai",
        "roads_km":1800,
        "metro_lines":1,
        "airports":1,
        "railway_stations":12,
        "smart_city_score":75,
        "ev_charging_stations":180
    },

    {
        "City":"Ahmedabad",
        "roads_km":1500,
        "metro_lines":1,
        "airports":1,
        "railway_stations":8,
        "smart_city_score":70,
        "ev_charging_stations":160
    },

    {
        "City":"Lucknow",
        "roads_km":1200,
        "metro_lines":1,
        "airports":1,
        "railway_stations":6,
        "smart_city_score":65,
        "ev_charging_stations":120
    }
]

with open ("City_infrastructure.json","w") as file:
    json.dump(data, file ,indent = 4)