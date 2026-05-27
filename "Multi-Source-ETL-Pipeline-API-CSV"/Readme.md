# 🛒 Multi-Source ETL Pipeline — REST API + CSV

---

## 📌 About This Project

A fully functional **Multi-Source ETL Pipeline** that extracts data from
**two different sources** — a **REST API** and a **CSV file** —
transforms and cleans both datasets, and loads them into a **MySQL database**.

This project demonstrates real-world data engineering skills including
API integration, data cleaning, feature engineering, and database connectivity.

---

## 🌟 Key Highlights

```
✅ Dual Data Source    → REST API + CSV File
✅ Live API Data       → FakeStore API (real HTTP request)
✅ Feature Engineering → Age categorization using lambda
✅ Smart Filtering     → Only relevant product categories
✅ Error Handling      → try/except/finally in all functions
✅ Python Logging      → Full pipeline monitoring with timestamps
✅ MySQL Storage       → Two separate clean tables
✅ None Validation     → Pipeline safety check before loading
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core programming language |
| Pandas | Data manipulation & cleaning |
| Requests | REST API data fetching |
| SQLAlchemy | MySQL database connectivity |
| MySQL | Data storage & persistence |
| Logging | Pipeline monitoring & error tracking |
| VS Code | Development environment |
| GitHub | Version control & portfolio |

---

## 📊 Data Sources

### Source 1 — REST API
```
API    → FakeStore API
URL    → https://fakestoreapi.com/products
Type   → Public REST API
Format → JSON → DataFrame
Data   → Product catalog (id, title, price, category)
```

### Source 2 — CSV File
```
File   → Customers.csv
Type   → Local CSV file
Format → CSV → DataFrame
Data   → Customer records (Name, City, Age, Membership)
```

---

## 📈 Pipeline Architecture

```
Source 1: FakeStore API          Source 2: Customers.csv
         ↓                                ↓
    requests.get()              pd.read_csv()
         ↓                                ↓
    response.json()             DataFrame created
         ↓                                ↓
    pd.DataFrame()              ─────────────────
         ↓                                ↓
         └──────────── extract() ─────────┘
                            ↓
                       transform()
                    ┌──────────────────────────┐
                    │ Customers:               │
                    │ → fillna City/Age/Member │
                    │ → str.lower() cities     │
                    │ → Age_Category (lambda)  │
                    │                          │
                    │ Products (API):          │
                    │ → fillna title           │
                    │ → drop unused columns    │
                    │ → filter clothing only   │
                    └──────────────────────────┘
                            ↓
                         load()
                    ┌─────────────────┐
                    │ MySQL Database  │
                    │ ─────────────── │
                    │ customers_data  │
                    │ products_data   │
                    └─────────────────┘
                            ↓
                    ✅ Pipeline Complete!
```

---

## 🧹 Data Transformation Details

### 👥 Customers (CSV Source)

| Step | Column | Action | Method |
|------|--------|--------|--------|
| 1 | City | Fill missing with "Unknown" | `fillna()` |
| 2 | City | Standardize to lowercase | `str.lower()` |
| 3 | Age | Fill missing with average | `fillna(mean())` |
| 4 | Membership | Fill missing with "Bronze" | `fillna()` |
| 5 | Age_Category | Feature engineering | `apply(lambda)` |

### Age Category Logic
```python
Age < 18  → "Teenager"
Age < 60  → "Adult"
Age >= 60 → "Senior_Citizen"
```

### 🛍️ Products (API Source)

| Step | Column | Action | Method |
|------|--------|--------|--------|
| 1 | title | Fill missing with "Unknown" | `fillna()` |
| 2 | description | Drop (not needed) | `drop()` |
| 3 | image | Drop (not needed) | `drop()` |
| 4 | rating | Drop (not needed) | `drop()` |
| 5 | category | Filter clothing only | `isin()` |

### Filter Logic
```python
Keep only:
→ "men's clothing"
→ "women's clothing"
```

---

## 💻 Code Structure

```
Orders_Project_Using_CSV_And_API.py
├── extract()    → Fetch API data + Read CSV
├── transform()  → Clean both DataFrames
└── load()       → Push both to MySQL
```

---

## 🔒 Error Handling

```python
# Extract function
except FileNotFoundError as e:
    logging.error(f"File Could not found {e}")

# Transform function
except KeyError as e:
    logging.error(f"Column could not be found {e}")

# Load function
except Exception as e:
    logging.error(f"Error during load {e}")

# Pipeline safety check
if Customers is not None and df is not None:
    transform() → load()
else:
    logging.error("None Values present - Pipeline stopped")
```

---

## 📝 Logging Output

```
2024-05-19 10:30:15 - INFO - Extract process completed
2024-05-19 10:30:16 - INFO - Transform process completed
2024-05-19 10:30:17 - INFO - Data is loaded Successfully
2024-05-19 10:30:17 - INFO - Load Process is Completed
2024-05-19 10:30:17 - INFO - Pipeline Successfully Executed
```

---

## 🚀 How to Run

### 1. Install Requirements
```bash
pip install pandas requests sqlalchemy pymysql
```

### 2. Setup MySQL Database
```sql
CREATE DATABASE practice;
```

### 3. Place CSV File
```
Place Customers.csv in project folder
Update the file path in extract() function
```

### 4. Run Pipeline
```bash
python Orders_Project_Using_CSV_And_API.py
```

### 5. Verify in MySQL
```sql
USE practice;
SELECT * FROM customers_data;
SELECT * FROM products_data;
```

---

## 📸 Output Tables in MySQL

### customers_data
```
Customer_Name | City   | Age  | Membership | Age_Category
Rahul Sharma  | pune   | 28.0 | Gold       | Adult
Priya Verma   | mumbai | 34.0 | Bronze     | Adult
...
```

### products_data
```
id | title              | price  | category
1  | Mens Casual Shirt  | 22.30  | men's clothing
2  | Womens Floral Dress| 15.99  | women's clothing
...
```

---

## 🎯 Concepts Demonstrated

```
✅ REST API Integration (requests library)
✅ JSON to DataFrame conversion
✅ CSV file reading and processing
✅ Multi-source data merging pipeline
✅ Missing value handling (fillna)
✅ String standardization (str.lower)
✅ Feature Engineering (Age_Category)
✅ Lambda functions for categorization
✅ Column dropping (drop)
✅ Data filtering (isin)
✅ try/except/finally error handling
✅ Python logging with timestamps
✅ SQLAlchemy MySQL connectivity
✅ Multiple table loading
✅ Pipeline None validation
```

---

## 📚 What I Learned

- Fetching live data from REST APIs using requests library
- Converting JSON API response to Pandas DataFrame
- Building ETL pipelines with multiple data sources
- Feature engineering using lambda functions
- Implementing proper error handling with specific exceptions
- Using Python logging for full pipeline monitoring
- Loading multiple cleaned datasets to MySQL
- Validating pipeline data before loading

---

## 🗺️ What's Next

- [ ] Add API key authentication for protected APIs
- [ ] Schedule pipeline with Apache Airflow
- [ ] Deploy to AWS/GCP cloud
- [ ] Add data validation layer
- [ ] Merge both datasets for combined analytics
- [ ] Build dashboard using Power BI

---

## 👨‍💻 About Me

I am **Saurabh Jadhav**, an aspiring Data Engineer actively learning:
- Python & Pandas for data engineering
- REST API integration and JSON processing
- ETL Pipeline development with multiple sources
- Error handling & logging best practices
- SQL (MySQL) — advanced queries & stored procedures
- Data Engineering tools & concepts

Currently pursuing **BCA** and building real-world projects
to strengthen my data engineering skills! 🚀

---


---

⭐ **If you found this helpful, give it a star!** ⭐
