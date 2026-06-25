# 🏙️ India Smart City Analytics — Multi-Source ETL Pipeline

---

## 📌 About This Project

A production-style **Multi-Source ETL Pipeline** that combines **3 different data sources** —
a **Live Weather REST API**, a **CSV file**, and a **JSON file** — to build a comprehensive
**India Smart City Analytics** platform.

This pipeline extracts real-time weather data for Indian cities, combines it with
demographic and infrastructure data, generates business KPIs, and loads the final
analytics-ready dataset into a **MySQL database**.

---

## 🌟 Key Highlights

```
✅ 3 Data Sources     → Live API + CSV + JSON (all in one pipeline!)
✅ Live Weather Data  → Real-time from OpenWeatherMap API
✅ 10 Indian Cities   →  city list from CSV 
✅ 10+ KPIs Generated → City Score, Tier, Rank, Investment Potential
✅ Security           → dotenv for API keys & DB credentials
✅ Error Handling     → try/except/finally in all 3 functions
✅ Python Logging     → Full pipeline monitoring with timestamps
✅ Pipeline Safety    → Double None check before execution
✅ MySQL Storage      → Clean analytics table loaded
✅ Professional Code  → Comments explain WHY not just WHAT
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core programming language |
| Pandas | Data manipulation & transformation |
| NumPy | Conditional logic & calculations |
| Requests | Live REST API data fetching |
| SQLAlchemy | MySQL database connectivity |
| MySQL | Final data storage |
| python-dotenv | Secure credential management |
| Logging | Pipeline monitoring & tracking |
| VS Code | Development environment |
| GitHub | Version control & portfolio |

---

## 📊 Data Sources

### Source 1 — Live Weather REST API 🌤️
```
Provider → OpenWeatherMap (Free Plan)
Type     → REST API (HTTP GET request)
Format   → JSON response
Data     → Temperature, Humidity, Weather Condition
Cities   → Dynamically fetched from CSV file
URL      → api.openweathermap.org/data/2.5/weather
```

### Source 2 — City Demographics (CSV) 🏘️
```
File     → City_Demographics.csv
Format   → CSV → Pandas DataFrame
Data     → Population, Area, Literacy Rate,
           Hospitals, Schools, GDP
Cities   → 10 major Indian cities
```

### Source 3 — City Infrastructure (JSON) 🏗️
```
File     → City_infrastructure.json
Format   → JSON → Pandas DataFrame
Data     → Roads KM, Metro Lines, Airports,
           Railway Stations, Smart City Score,
           EV Charging Stations
Cities   → 10 major Indian cities
```

---

## 🗺️ Pipeline Architecture

```
┌─────────────────────────────────────────────────┐
│                   EXTRACT                        │
│                                                  │
│  CSV File    JSON File    OpenWeatherMap API      │
│     ↓            ↓              ↓                │
│ City_Demo   City_Infra    Weather_df              │
│ (10 cities) (10 cities)  (Live data)             │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│                 TRANSFORM                        │
│                                                  │
│  City_Demo:    City_Infra:    Weather_df:        │
│  → fillna()    → fillna()     → Temp_Label       │
│  → Pop_Density → Smart_Label  → Humidity_Label   │
│  → City_Tier   → Infra_Score  → Weather_Score    │
│  → Literacy    → EV_Readiness → Condition Title  │
│  → GDP_Category                                  │
│                                                  │
│  Merge: Demo + Infra (INNER) + Weather (LEFT)    │
│                                                  │
│  KPIs Generated:                                 │
│  → Overall_City_Score                            │
│  → Investment_Potential                          │
│  → Livability_Score                              │
│  → City_Rank                                     │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│                    LOAD                          │
│                                                  │
│  MySQL Database → practice                       │
│  Table → india_smart_city_analytics              │
│  Method → if_exists = "replace"                  │
└─────────────────────────────────────────────────┘
```

---

## 🧹 Transformation Details

### 🏘️ City Demographics (CSV)

| Column | Action | Reason |
|--------|--------|--------|
| Population | fillna(mean) | Avoid wrong analysis |
| Literacy_Rate | fillna(mean) | Avoid wrong analysis |
| GDP | fillna(0) | Avoid skewing averages |
| City | str.strip().str.title() | Standardize for merging |
| Pop_Density | Population×1M / Area | Compare city crowding |
| City_Tier | lambda (Tier 1/2/3) | Population classification |
| Literacy_Label | lambda (3 levels) | Education classification |
| GDP_Category | lambda (3 levels) | Economic classification |

### 🏗️ City Infrastructure (JSON)

| Column | Action | Reason |
|--------|--------|--------|
| City | str.strip().str.title() | Normalize for merging |
| smart_city_score | fillna(0) | Avoid scoring errors |
| ev_charging_stations | fillna(0) | Avoid scoring errors |
| Smart_City_Label | np.where (4 levels) | Infrastructure quality |
| Infra_Score | Weighted calculation | Overall infra rating |
| EV_Readiness | np.where (3 levels) | EV infrastructure level |

### 🌤️ Weather API (Live Data)

| Column | Action | Reason |
|--------|--------|--------|
| City | str.strip().str.title() | Normalize for merging |
| Temp_Label | np.where (4 levels) | Temperature classification |
| Humidity_Label | np.where (3 levels) | Humidity classification |
| Condition | str.title() | Clean presentation |
| Weather_Score | np.where formula | Livability calculation |

---

## 📈 Business KPIs Generated

```python
# 1. Overall City Score
Overall_City_Score = (
    smart_city_score × 0.4 +
    Literacy_Rate × 0.3 +
    Weather_Score × 0.3
)

# 2. Investment Potential
"High"   → Tier 1 + Excellent/Good infrastructure
"Medium" → Tier 2 cities
"Low"    → Tier 3 cities

# 3. Livability Score
Livability = (
    Literacy_Rate × 0.3 +
    smart_city_score × 0.4 +
    Hospitals × 0.01 +
    Schools × 0.001
)

# 4. City Rank
City_Rank → Ranked by Overall_City_Score
```

---

## 🔒 Security Implementation

```python
# All credentials stored in .env file
# Never hardcoded in source code!

# .env file (never pushed to GitHub):
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=practice
API_KEY=your_openweathermap_key

# In code:
API_KEY = os.getenv("API_KEY")
conn = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:..."
)
```

---

## 🛡️ Error Handling

```python
# Extract → File not found
except FileNotFoundError as e:
    logging.error(f"File Missing: {e}")
    return None, None, None

# Transform → Column not found
except KeyError as e:
    logging.error(f"Column not found: {e}")

# Transform → String operation on null
except AttributeError as e:
    logging.error(f"String operation failed: {e}")

# Load → Database errors
except Exception as e:
    logging.error(f"Load Failed: {e}")

# Safe connection disposal
finally:
    try:
        conn.dispose()
    except:
        pass
```

---

## 📝 Logging Output

```
2024-05-29 11:30:15 - INFO - Extract Process Started
2024-05-29 11:30:16 - INFO - Extract Completed
2024-05-29 11:30:16 - INFO - Transformation Started
2024-05-29 11:30:17 - INFO - Transformation Completed
2024-05-29 11:30:17 - INFO - Load Process Started
2024-05-29 11:30:18 - INFO - Data Loaded Successfully
2024-05-29 11:30:18 - INFO - Load Process Completed
2024-05-29 11:30:18 - INFO - Pipeline Execution Completed!
```

---

## 🚀 How to Run

### 1. Install Requirements
```bash
pip install pandas numpy requests sqlalchemy pymysql python-dotenv
```

### 2. Get Free API Key
```
→ Go to openweathermap.org
→ Sign up (FREE!)
→ Go to "My API Keys"
→ Copy your key
```

### 3. Create .env File
```
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3306
DB_NAME=practice
API_KEY=your_api_key_here
```

### 4. Create .gitignore File
```
.env
Logs
```

### 5. Setup MySQL
```sql
CREATE DATABASE practice;
```

### 6. Run Pipeline
```bash
python Pipeline.py
```

### 7. Verify Output
```sql
USE practice;
SELECT * FROM india_smart_city_analytics;
```

---

## 📸 Output Preview

```
City      | City_Tier | Smart_City_Label | Temp | Overall_Score | City_Rank
Mumbai    | Tier 1    | Excellent        | 29°C | 87.5          | 1
Delhi     | Tier 1    | Excellent        | 35°C | 85.2          | 2
Bangalore | Tier 2    | Good             | 24°C | 82.1          | 3
Pune      | Tier 2    | Good             | 31°C | 79.8          | 4
Chennai   | Tier 2    | Average          | 33°C | 75.3          | 5
```

---

## 🎯 Concepts Demonstrated

```
✅ REST API Integration (requests library)
✅ Live JSON API response processing
✅ CSV file reading and processing
✅ JSON file reading and processing
✅ Multi-source ETL pipeline (3 sources!)
✅ Dynamic city list from CSV (no hardcoding)
✅ Missing value handling (fillna, dropna)
✅ String standardization (str.strip, str.title)
✅ Feature Engineering (6 new columns)
✅ np.where() for conditional logic
✅ lambda functions for categorization
✅ apply() with axis=1 for row operations
✅ Multi-table merging (INNER + LEFT JOIN)
✅ Business KPI calculations
✅ try/except/finally error handling
✅ Specific exception types (KeyError, AttributeError)
✅ Python logging with timestamps
✅ dotenv for secure credential management
✅ SQLAlchemy MySQL connectivity
✅ Pipeline None validation (double check)
✅ Safe connection disposal
✅ Professional code documentation
```

---

## 📚 What I Learned

- Building production-style ETL pipelines with multiple data sources
- Fetching and processing live REST API data
- Reading and transforming JSON and CSV files simultaneously
- Implementing security best practices with dotenv
- Feature engineering using NumPy and Pandas
- Writing professional code comments that explain WHY
- Building safe pipelines with proper error handling
- Monitoring pipelines with Python logging
- Generating business KPIs from raw data

---

---

## 👨‍💻 About Me

I am **Saurabh Jadhav**, an aspiring Data Engineer actively learning:
- Python & Pandas — Advanced data engineering
- REST API integration and JSON processing
- Multi-source ETL Pipeline development
- Security best practices (dotenv)
- Error handling & logging
- SQL (MySQL) — Advanced queries & stored procedures
- NumPy for analytical calculations
- Data Engineering tools & best practices

Currently pursuing **BCA** and building real-world projects
to strengthen my data engineering skills! 🚀

---


⭐ **If you found this helpful, give it a star!** ⭐
