# Real-Time Data Warehouse

This project sets up a real-time data warehouse leveraging tools such as Apache Airflow, Apache Kafka, PostgreSQL, Redpanda, Apache Pinot, and Apache Superset. The architecture facilitates data ingestion, processing, storage, and visualization in real-time for scalable and efficient analytics.

## Features
- **Data Ingestion**: Redpanda as a Kafka-compatible broker for real-time streaming.
- **Workflow Orchestration**: Apache Airflow for scheduling and managing ETL processes.
- **Data Storage**: PostgreSQL for metadata storage and Apache Pinot for real-time OLAP queries.
- **Data Visualization**: Apache Superset for interactive dashboards and analytics.

## Architecture Overview
The project consists of the following components:
1. **Redpanda (Kafka Broker)**: Handles real-time data streaming.
2. **Zookeeper**: Manages Kafka cluster configurations.
3. **Apache Airflow**: Schedules and manages ETL workflows.
4. **PostgreSQL**: Stores metadata for Airflow and other services.
5. **Apache Pinot**: Provides real-time OLAP capabilities for high-speed data queries.
6. **Apache Superset**: Visualizes the processed data through interactive dashboards.
7. **Redpanda Console**: Monitors and manages Kafka topics.

## Prerequisites
- Docker and at least 4GB of memory and 2 CPUs allocated to Docker.
- Python 3.10+

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Oiver237/RealTimeDatawarehouse.git
   cd RealTimeDatawarehouse
2. Start the services using Docker Compose:
    ```bash
    docker-compose up -d
3. Run all the DAGs in airflow by starting to generate the data (**_generator.py), then run the schema_dag, then the table_dag, and finally the loaders_dag.
4. Create dashboards on Apache superset as you want. 

## Notes
- Default credentials for each service can be modified in the docker-compose.yml file.
- Make sure to set up email configurations for Airflow if email notifications are needed.
