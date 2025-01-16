from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pinot_table_operator import PinotTableSubmitOperator
import pandas as pd


start_date =datetime(2025,1,16)

defaul_args = {
    'owner':'olivier',
    'depends_on_past':False,
    'backfill':False,
    'start_date': start_date
}



with DAG('table_dag',
         default_args= defaul_args,
         description= 'A DAG to submit all tables in a folder to Apache Pinot',
         schedule_interval= timedelta(days=1),
         start_date= start_date,
         tags= ['table']) as dag:
    start= EmptyOperator(
        task_id= 'start_task'
    )
    
    submit_table = PinotTableSubmitOperator(
        task_id='submit_tables',
        folder_path='/opt/airflow/dags/tables',
        pinot_url='http://pinot-controller:9000/tables'
    )
    end= EmptyOperator(
        task_id= 'end_task'
    )

    start>>submit_table>>end