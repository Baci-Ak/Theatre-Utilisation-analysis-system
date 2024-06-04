


# Theatre Utilisation Analysis System

## Overview

The Theatre Utilisation Analysis System is a sophisticated analytics platform designed to enhance operational efficiency in surgical environments through advanced data-driven insights. This system integrates a comprehensive data pipeline and visualization tools to assist healthcare professionals in making informed decisions.

## Project Genesis

Leveraging a combination of technologies including Azure Data Factory, SQL Server, and Azure Databricks, this project processes data sourced from the NHS's public data hub. The project employs ngrok to facilitate connectivity from Azure Data Factory to an on-premise SQL Server, overcoming integration challenges associated with macOS.

### Data Workflow

1. **Data Ingestion**: Automated ingestion from [NHS Public Data Hub](https://ckan.publishing.service.gov.uk/dataset) via Azure Data Factory.
2. **Data Transformation**: Data cleaning and transformation using Azure Databricks connected to SQL Server.
3. **Data Loading**: Transformed data is loaded back into SQL Server for persistence.
4. **Visualization**: Initial visualizations in Microsoft Excel evolved into a dynamic Streamlit web application, enhancing accessibility and interactivity.

## Key Features

- **Interactive Visualizations**: Engage with interactive charts and graphs to explore metrics related to surgical procedures and performance.
- **SQL Data Analysis**: In-depth analysis through custom SQL queries to identify trends and efficiencies.
- **Real-time Data Integration**: Ensures the dashboard remains current with automated data refresh capabilities.

## Technology Stack

- Azure Data Factory
- SQL Server
- Azure Databricks
- Microsoft Excel
- Streamlit
- Python

## Project Structure

Below is an overview of the key files and directories within the project:


```
/Theatre-Utilisation-analysis-system
|-- .streamlit/
|   |-- config.toml              # Streamlit app configuration
|-- data/
|   |-- Business_Analyst_Test_Theatre_Cases.xlsx               # Excel worksheet containing all the Data sheets including dashboard
|   |-- Business_Analyst_Test_Theatre_Cases.csv                     # csv format of the Raw data
|-- images/
|   |-- Homebanner.png           # Home page banner
|   |-- Navigation.png           # Navigation area banner
|-- scripts/
|   |-- data_analysis.sql          # SQL queries used in the analysis
|-- notebooks/
|-- app.py                       # Main Streamlit application
|-- README.md                    # Project documentation
|-- requirements.txt             # Python dependencies
```

## Getting Started

To get a local copy up and running follow these simple steps:

1. **Clone the repo**:
   ```
   git clone https://github.com/Baci-Ak/Theatre-Utilisation-analysis-system.git
   ```
2. **Install required dependencies**:
   ```
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```
   streamlit run app.py
   ```

## Live Application

Explore the live application [here](https://theatre-utilisation-analysis-system.streamlit.app/).
```
