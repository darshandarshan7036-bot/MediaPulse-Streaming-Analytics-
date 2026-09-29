Absolutely. Below is a **complete root-level `README.md`** for your MediaPulse project. It is written around what you have **actually implemented**, while clearly separating components that are planned rather than falsely claiming they are already completed.

Copy everything below into:

```text
C:\Users\rammi\OneDrive\Desktop\mediapulse\README.md
```

````markdown
# MediaPulse

## Media, Streaming & Audience Intelligence Platform

MediaPulse is an end-to-end data engineering and analytics platform designed to process media, streaming, advertising, subscription, and support data to generate actionable audience insights.

The platform combines batch data processing, live Kafka streaming, PostgreSQL analytics, dbt transformations, machine learning, FastAPI APIs, and a React dashboard.

---

## 1. Project Overview

MediaPulse provides a unified platform for understanding:

- User viewing behavior
- Content performance
- Audience engagement
- Advertising performance
- Subscription status
- Customer support activity
- Live streaming activity
- Audience forecasting
- Churn-risk indicators
- Data quality
- Operational alerts

The system supports both historical/batch analytics and near-real-time audience monitoring.

---

## 2. Business Problem

Media and streaming platforms generate large volumes of data from multiple sources, including:

- User activity
- Content consumption
- Advertising events
- Subscription activity
- Customer support interactions
- Live viewing events

Without a centralized data platform, it becomes difficult to:

- Monitor audience behavior
- Measure content performance
- Track advertising engagement
- Understand subscription patterns
- Detect potential churn
- Monitor live audience activity
- Forecast future audience levels
- Maintain data quality

MediaPulse addresses these problems by building an integrated data pipeline and analytics platform.

---

## 3. Key Features

### Data Engineering

- Synthetic media and audience data generation
- Data validation and quality checks
- Bronze and Silver data layers
- PostgreSQL data warehouse
- Dimensional/star schema
- Fact and dimension tables
- Incremental live event ingestion

### Real-Time Streaming

- Apache Kafka producer
- Kafka topic for live view events
- Kafka consumer
- PostgreSQL persistence of live events
- Duplicate event protection
- Near-real-time KPI updates

### Analytics

- Audience KPIs
- Content performance
- Campaign performance
- Subscription analysis
- Live audience metrics
- Completion rate
- Watch-time analysis
- Churn-risk indicators

### Machine Learning

- Audience forecasting using Random Forest Regression
- MAE evaluation
- RMSE evaluation
- Next-period audience prediction

### Data Transformation

- dbt models
- dbt tests
- Analytical marts
- PostgreSQL-based transformations

### API

FastAPI provides REST endpoints for:

- Live audience metrics
- Audience forecasting
- Content performance
- Campaign performance
- Subscriber health
- Churn risk
- Data quality
- Alerts
- Alert actions
- API health

### Dashboard

The React dashboard provides:

- Live KPI cards
- Live audience metrics
- AI audience forecast
- Campaign performance chart
- Alert monitoring
- Automatic refresh

---

# 4. System Architecture

```text
                     ┌─────────────────────┐
                     │   Source Data       │
                     │                     │
                     │ Users               │
                     │ Content             │
                     │ Views               │
                     │ Ads                 │
                     │ Subscriptions       │
                     │ Support             │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Data Generation /   │
                     │ Batch Ingestion     │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Bronze Layer     │
                     │ Raw / Immutable     │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   Silver Layer     │
                     │ Cleaned / Prepared  │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │    PostgreSQL      │
                     │    Data Warehouse  │
                     └──────────┬──────────┘
                                │
                ┌───────────────┼────────────────┐
                │               │                │
                ▼               ▼                ▼
             dbt             SQL/ML          FastAPI
          Transformations   Analytics         REST API
                │               │                │
                └───────────────┼────────────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   React Dashboard   │
                     └─────────────────────┘


              LIVE STREAMING PIPELINE

     Live Events
          │
          ▼
   Kafka Producer
          │
          ▼
   Kafka Topic
 mediapulse_views
          │
          ▼
   Kafka Consumer
          │
          ▼
   PostgreSQL
 live_view_events
          │
          ▼
 live_audience_kpis
          │
          ▼
      FastAPI
          │
          ▼
   React Dashboard
````

---

# 5. Technology Stack

| Component                   | Technology                           |
| --------------------------- | ------------------------------------ |
| Programming                 | Python                               |
| Data Processing             | Pandas, PySpark                      |
| Streaming                   | Apache Kafka                         |
| Message Broker Coordination | Apache ZooKeeper                     |
| Database                    | PostgreSQL                           |
| Transformation              | dbt                                  |
| Machine Learning            | Scikit-learn                         |
| API                         | FastAPI                              |
| API Server                  | Uvicorn                              |
| Frontend                    | React                                |
| Frontend Build Tool         | Vite                                 |
| Charts                      | Recharts                             |
| Data Generation             | Faker                                |
| Version Control             | Git                                  |
| Containerization            | Docker (planned/finalization stage)  |
| Orchestration               | Airflow (planned/finalization stage) |

---

# 6. Project Structure

```text
mediapulse/
│
├── data/
│   ├── raw/
│   ├── bronze/
│   └── silver/
│
├── data_generation/
│   ├── generate_data.py
│   └── kafka_producer.py
│
├── scripts/
│   ├── data_quality_check.py
│   ├── create_bronze.py
│   ├── create_silver.py
│   └── kafka_consumer.py
│
├── sql/
│   └── SQL scripts and analytical queries
│
├── ml/
│   └── audience_forecast.py
│
├── mediapulse_dbt/
│   ├── analyses/
│   ├── macros/
│   ├── models/
│   │   ├── schema.yml
│   │   └── marts/
│   │       ├── content_performance.sql
│   │       ├── campaign_performance.sql
│   │       ├── audience_kpis.sql
│   │       └── subscription_performance.sql
│   ├── seeds/
│   ├── snapshots/
│   ├── tests/
│   ├── dbt_project.yml
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   ├── package-lock.json
│   ├── index.html
│   └── vite.config.js
│
├── docs/
│
├── api.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 7. Data Sources

MediaPulse currently uses generated datasets representing common media-platform sources.

### Users

Contains user/customer information.

Example fields:

```text
user_id
name
age
gender
city
subscription-related attributes
```

### Content

Contains media/content metadata.

Example fields:

```text
content_id
title
genre
language
duration
```

### Views

Contains historical viewing events.

Example fields:

```text
view_id
user_id
content_id
event_timestamp
watch_seconds
event_type
```

### Ads

Contains advertising events.

Example fields:

```text
ad_id
campaign_id
user_id
impression
click
event_timestamp
```

### Subscriptions

Contains subscription information.

Example fields include:

```text
subscription_id
user_id
plan
status
start_date
end_date
```

### Support

Contains customer-support activity.

Example fields include:

```text
ticket_id
user_id
issue_type
created_at
status
```

---

# 8. Data Generation

Synthetic data is generated using Python and Faker.

Run:

```powershell
python data_generation/generate_data.py
```

The generated datasets are stored under:

```text
data/raw/
```

The project currently generates approximately:

```text
Users          : 1,000
Content        : 100
Views          : 10,000
Ads            : 2,000
Subscriptions  : 1,000
Support        : 500
Total records  : 14,600
```

---

# 9. Data Quality

The project includes a data-quality validation script:

```powershell
python scripts/data_quality_check.py
```

The checks include:

* Missing values
* Duplicate records
* Duplicate primary keys
* Invalid foreign keys
* Negative watch duration
* Invalid impressions
* Invalid clicks
* Clicks without impressions

The initial generated dataset passed these validation checks with no detected invalid records.

---

# 10. Bronze and Silver Layers

MediaPulse follows a layered data-processing approach.

### Bronze

The Bronze layer stores raw ingested data with minimal transformation.

Purpose:

* Preserve source data
* Maintain traceability
* Support reprocessing
* Maintain an immutable/raw representation

### Silver

The Silver layer contains cleaned and prepared data.

Typical processing includes:

* Schema validation
* Data type normalization
* Cleaning
* Deduplication
* Preparation for analytical processing

The project currently uses a local Windows-compatible processing approach for the Silver output. A containerized/Linux execution environment can be used for production-style Spark processing.

---

# 11. PostgreSQL Data Warehouse

PostgreSQL is used as the analytical warehouse.

The warehouse follows a dimensional/star-schema approach.

### Dimension Tables

```text
dim_user
dim_content
dim_date
dim_campaign
```

### Fact Tables

```text
fact_view
fact_ad
fact_subscription
fact_engagement
```

### Live Tables

```text
live_view_events
```

### Analytical Views

```text
live_audience_kpis
churn_risk
```

The warehouse also includes:

* Primary keys
* Foreign keys
* Constraints
* Referential integrity
* Analytical views
* Audit timestamps

---

# 12. Kafka Live Streaming

MediaPulse supports live streaming using Apache Kafka.

### Kafka Topic

```text
mediapulse_views
```

### Producer

The producer generates live viewing events.

Run:

```powershell
python data_generation/kafka_producer.py
```

Example event:

```json
{
  "event_id": "LIVE_1234567890_01",
  "user_id": "U0001",
  "content_id": "C0001",
  "timestamp": "2026-09-27T10:30:00",
  "watch_seconds": 120,
  "event_type": "play"
}
```

### Consumer

The consumer reads events from Kafka and stores them in PostgreSQL.

Run:

```powershell
python scripts/kafka_consumer.py
```

The consumer uses the event ID to prevent duplicate event insertion.

Duplicate handling is implemented using:

```sql
ON CONFLICT (event_id) DO NOTHING
```

---

# 13. Live Audience KPIs

Live audience metrics are exposed through:

```text
live_audience_kpis
```

Current metrics include:

* Total live events
* Unique active users
* Active content
* Total watch seconds
* Average watch seconds
* Completed events
* Completion rate

These metrics are exposed through the FastAPI endpoint:

```text
GET /api/audience/live
```

The React dashboard automatically refreshes the live metrics.

---

# 14. dbt Transformation Layer

dbt is used to build analytical models on top of the PostgreSQL warehouse.

The dbt project is located at:

```text
mediapulse_dbt/
```

### Models

```text
content_performance
campaign_performance
audience_kpis
subscription_performance
```

Run dbt:

```powershell
cd mediapulse_dbt
dbt run
```

Run tests:

```powershell
dbt test
```

The current dbt project has successfully executed its models and tests.

---

# 15. Analytics

## Audience KPIs

Current historical metrics include:

```text
Total views              : 10,000
Total watch seconds      : 29,722,223
Total watch hours        : 8,256.17
Completed views          : 2,414
Completion rate          : 24.14%
```

## Content Performance

Content-level metrics include:

* Total views
* Watch seconds
* Watch hours
* Completed views
* Completion rate

## Campaign Performance

Campaign metrics include:

* Ad events
* Impressions
* Clicks
* CTR

Example:

```text
CMP001 : 11.76%
CMP004 : 10.84%
CMP003 : 10.83%
CMP002 :  8.98%
CMP005 :  6.91%
```

## Subscription Analysis

Subscription analysis includes:

* Subscription plan
* Subscription status
* Status counts
* Status percentages

Subscription status percentages should be interpreted as status distributions rather than automatically being treated as true churn rates.

---

# 16. Machine Learning

MediaPulse includes an audience forecasting model.

File:

```text
ml/audience_forecast.py
```

The model uses:

```text
RandomForestRegressor
```

### Features

The current model uses:

* Day number
* Day of week
* Month

Historical daily audience data is divided chronologically into training and testing datasets.

### Evaluation Metrics

The model calculates:

* MAE
* RMSE

Example model result:

```text
Training records : 25
Testing records  : 7
MAE              : 34.76
RMSE             : 44.75
```

The forecast is stored in PostgreSQL and exposed through:

```text
GET /api/audience/forecast
```

---

# 17. Churn Risk

MediaPulse currently implements a rule-based churn-risk classification.

Risk levels include:

```text
High
Medium
Low
```

The classification uses signals such as:

* Subscription status
* Total views
* Support tickets

The churn-risk output is exposed through:

```text
GET /api/churn-risk
```

This is currently a rule-based analytical feature and should not be described as a trained machine-learning churn model.

---

# 18. Alerts and Automation

MediaPulse contains an alerting framework for important operational and analytical conditions.

Examples include:

### Churn Risk Alert

Generated for users meeting high-risk conditions.

### Ad Performance Alert

Generated when campaign CTR falls below the configured threshold.

### Engagement Alert

Can be generated when live completion performance falls below the configured threshold.

Alerts contain fields such as:

```text
alert_id
alert_type
severity
owner
status
reason
created_at
acknowledged_at
```

Alert actions are also recorded for audit purposes.

API endpoints:

```text
GET  /api/alerts
POST /api/alerts/{alert_id}/acknowledge
GET  /api/alert-actions
```

The current implementation records alert actions as an application audit/notification log. External email or messaging delivery can be added later.

---

# 19. FastAPI Backend

The backend is implemented using FastAPI.

Start the API:

```powershell
uvicorn api:app --reload
```

Default address:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 20. API Endpoints

### Health

```text
GET /api/health
```

### Live Audience

```text
GET /api/audience/live
```

### Audience Forecast

```text
GET /api/audience/forecast
```

### Content Performance

```text
GET /api/content/{content_id}/performance
```

### Campaigns

```text
GET /api/campaigns
```

### Subscriber Health

```text
GET /api/subscriber/{user_id}/health
```

### Churn Risk

```text
GET /api/churn-risk
```

### Data Quality

```text
GET /api/data-quality
```

### Alerts

```text
GET /api/alerts
```

### Acknowledge Alert

```text
POST /api/alerts/{alert_id}/acknowledge
```

### Alert Actions

```text
GET /api/alert-actions
```

---

# 21. React Dashboard

The frontend is built using React and Vite.

Directory:

```text
frontend/
```

Install dependencies:

```powershell
cd frontend
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend is normally available at:

```text
http://localhost:5173
```

The dashboard displays:

* Live Events
* Active Users
* Active Content
* Completion Rate
* Live Watch Time
* Average Watch Time
* Completed Events
* AI Audience Forecast
* MAE
* RMSE
* Campaign Performance
* Alerts

The dashboard refreshes API data automatically every 10 seconds.

---

# 22. Running the Complete System

## Step 1 — Start PostgreSQL

Make sure PostgreSQL is running.

Database:

```text
mediapulse
```

Default local configuration:

```text
Host     : localhost
Port     : 5432
Database : mediapulse
```

---

## Step 2 — Activate Python Environment

From the project root:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Step 3 — Start ZooKeeper

From the Kafka installation directory:

```powershell
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

Keep this terminal running.

---

## Step 4 — Start Kafka

Open another PowerShell terminal:

```powershell
cd "C:\kafka\kafka_2.13-2.6.0"
```

Run:

```powershell
.\bin\windows\kafka-server-start.bat .\config\server.properties
```

Keep this terminal running.

---

## Step 5 — Start Kafka Consumer

Open another terminal:

```powershell
cd "C:\Users\rammi\OneDrive\Desktop\mediapulse"
.\venv\Scripts\Activate.ps1
python scripts/kafka_consumer.py
```

---

## Step 6 — Start FastAPI

Open another terminal:

```powershell
cd "C:\Users\rammi\OneDrive\Desktop\mediapulse"
.\venv\Scripts\Activate.ps1
uvicorn api:app --reload
```

---

## Step 7 — Start React

Open another terminal:

```powershell
cd "C:\Users\rammi\OneDrive\Desktop\mediapulse\frontend"
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## Step 8 — Generate Live Events

When Kafka and the consumer are running:

```powershell
cd "C:\Users\rammi\OneDrive\Desktop\mediapulse"
.\venv\Scripts\Activate.ps1
python data_generation/kafka_producer.py
```

The events should flow through:

```text
Producer
   ↓
Kafka
   ↓
Consumer
   ↓
PostgreSQL
   ↓
FastAPI
   ↓
React
```

The dashboard should update automatically.

---

# 23. Data Quality and Validation

The project includes validation at multiple stages.

### Source Data

Checks include:

* Missing values
* Duplicates
* Primary-key duplicates
* Foreign-key validity
* Invalid numerical values

### Database

PostgreSQL uses:

* Primary keys
* Foreign keys
* NOT NULL constraints
* CHECK constraints
* Unique constraints

### Streaming

Kafka events use:

```text
event_id
```

as the duplicate-protection key.

### dbt

dbt tests are defined in:

```text
mediapulse_dbt/models/schema.yml
```

Run:

```powershell
cd mediapulse_dbt
dbt test
```

---

# 24. Security

Sensitive configuration should not be hardcoded in source code.

The project uses `.gitignore` rules to prevent secrets from being committed.

Environment variables should be used for production configuration, for example:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
KAFKA_BOOTSTRAP_SERVERS
```

A local `.env` file should never be committed to Git.

An `.env.example` file can be provided as a safe configuration template.

---

# 25. Docker and Airflow

The project architecture is designed to support containerized execution and workflow orchestration.

The next productionization stage includes:

### Docker

Containerization of:

* PostgreSQL
* Kafka
* FastAPI
* React
* Data-processing services

### Airflow

Airflow can orchestrate:

* Data ingestion
* Data-quality checks
* Bronze processing
* Silver processing
* dbt transformations
* ML forecasting
* Alert generation

These components can be added as part of the production deployment architecture.

---

# 26. Monitoring and Observability

The platform includes basic operational monitoring through:

* API health endpoint
* Kafka consumer logs
* Data-quality checks
* Alert records
* Alert action audit records
* Streaming KPI monitoring

Future production enhancements can include:

* Prometheus
* Grafana
* Centralized logging
* Kafka lag monitoring
* Pipeline failure alerts
* Airflow task monitoring

---

# 27. Current Project Status

### Implemented

* [x] Synthetic data generation
* [x] Data-quality validation
* [x] Bronze processing
* [x] Silver processing
* [x] PostgreSQL warehouse
* [x] Dimensional model
* [x] Kafka producer
* [x] Kafka topic
* [x] Kafka consumer
* [x] Duplicate event handling
* [x] Live audience KPI view
* [x] dbt models
* [x] dbt tests
* [x] Audience forecasting
* [x] Churn-risk rules
* [x] Alert framework
* [x] FastAPI backend
* [x] Swagger API documentation
* [x] React dashboard
* [x] Campaign performance visualization
* [x] Automatic dashboard refresh
* [x] Git ignore configuration
* [x] Python requirements file

### Productionization / Finalization

* [ ] Docker containerization
* [ ] Docker Compose orchestration
* [ ] Airflow DAG
* [ ] Environment-based secret configuration
* [ ] Production monitoring
* [ ] Cloud deployment

---

# 28. Known Data Limitations

The current source data does not contain all fields required for certain advertising KPIs.

For example, true:

* Ad spend
* Revenue
* CPM
* Fill rate
* Ad opportunity/request counts

cannot be calculated accurately without the required source fields.

The project therefore calculates available metrics such as:

```text
Impressions
Clicks
CTR
```

rather than inventing unavailable business measurements.

---

# 29. Future Enhancements

Potential improvements include:

* Docker-based deployment
* Airflow orchestration
* Cloud deployment
* Streaming with stronger fault tolerance
* Advanced data-quality monitoring
* Feature store for ML
* Improved audience forecasting
* Trained churn prediction model
* Recommendation system
* Advanced campaign attribution
* Prometheus/Grafana monitoring
* Automated email/Slack alert delivery
* Authentication and authorization
* CI/CD pipeline

---

# 30. Project Goal

The goal of MediaPulse is to demonstrate an end-to-end modern data platform capable of:

```text
Data Ingestion
      ↓
Data Quality
      ↓
Bronze Layer
      ↓
Silver Layer
      ↓
Data Warehouse
      ↓
dbt Transformation
      ↓
Analytics + Machine Learning
      ↓
FastAPI
      ↓
React Dashboard
```

while simultaneously supporting:

```text
Live Streaming
      ↓
Kafka
      ↓
Real-Time Processing
      ↓
Persistent Analytical Output
      ↓
Live Dashboard Updates
.



