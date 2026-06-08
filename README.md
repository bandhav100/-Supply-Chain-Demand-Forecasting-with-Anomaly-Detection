# GitHub Developer Trend Analytics

## Overview

GitHub Developer Trend Analytics is a SQL-focused data analytics project that collects repository data from the GitHub API, stores it in PostgreSQL, and analyzes open-source development trends through SQL queries and an interactive Streamlit dashboard.

The project helps identify:

* Popular programming languages
* Trending repositories
* Repository popularity based on stars
* Technology adoption patterns
* Open-source ecosystem insights

---

## Project Architecture

GitHub API

↓

Python ETL Pipeline

↓

PostgreSQL Database

↓

SQL Analysis

↓

Streamlit Dashboard

---

## Features

* Collects repository data using GitHub API
* Stores repository metadata in PostgreSQL
* Performs SQL-based trend analysis
* Repository search functionality
* Language filtering
* Language popularity analysis
* Repository ranking analysis
* Interactive Streamlit dashboard

---

## Database Schema

### repositories

| Column     | Type    |
| ---------- | ------- |
| id         | SERIAL  |
| repo_name  | VARCHAR |
| owner      | VARCHAR |
| language   | VARCHAR |
| stars      | INTEGER |
| forks      | INTEGER |
| watchers   | INTEGER |
| created_at | DATE    |
| updated_at | DATE    |

---

## Technologies Used

* Python
* PostgreSQL
* SQL
* GitHub API
* Pandas
* Streamlit
* Matplotlib

---

## Dashboard Features

* Repository Overview
* Top Repositories
* Language Popularity Analysis
* Language Distribution
* Repository Search
* Repository Details
* Key Insights

---

## Example SQL Analysis

### Most Popular Languages

```sql
SELECT language,
COUNT(*) AS total_repositories
FROM repositories
GROUP BY language
ORDER BY total_repositories DESC;
```

### Top Repositories by Stars

```sql
SELECT repo_name, stars
FROM repositories
ORDER BY stars DESC
LIMIT 10;
```

---

## Installation

```bash
git clone <repository-url>

cd github-trend-analytics

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

## Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Future Improvements

* Contributor Analytics
* Technology Growth Tracking
* Advanced SQL Window Functions
* Trend Forecasting
* Interactive Visualizations

---

## Author

Bandhav A
