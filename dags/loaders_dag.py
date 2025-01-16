from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


start_date =datetime(2025,1,16)

defaul_args = {
    'owner':'olivier',
    'depends_on_past':False,
    'backfill':False,
    'start_date': start_date
}


with DAG (
    'dimension_bacth_ingestion',
    default_args=defaul_args,
    description= ' A DAG to load data into Apache Pinot.',
    schedule_interval='@daily',
    catchup=False,
    tags=['loader']) as dag:


    ingest_account_data = BashOperator(
    task_id="ingest_account_data",
    bash_command=(
        "curl -X POST -F file=@/opt/airflow/account_dim_largedata.csv "
        "-H 'Content-Type: multipart/form-data' "
        "'http://pinot-controller:9000/ingestFromFile?"
        "tableNameWithType=account_dim_OFFLINE&batchConfigMapStr=%7B"
        "%22inputFormat%22%3A%22csv%22%2C"
        "%22recordReader.prop.delimiter%22%3A%22%2C%22%7D'"
    )
    )

    ingest_customer_data = BashOperator(
        task_id="ingest_customer_data",
        bash_command=(
            "curl -X POST -F file=@/opt/airflow/customer_dim_largedata.csv "
            "-H 'Content-Type: multipart/form-data' "
            "'http://pinot-controller:9000/ingestFromFile?"
            "tableNameWithType=customer_dim_OFFLINE&batchConfigMapStr=%7B"
            "%22inputFormat%22%3A%22csv%22%2C"
            "%22recordReader.prop.delimiter%22%3A%22%2C%22%7D'"
        )
    )

    ingest_branch_data = BashOperator(
        task_id="ingest_branch_data",
        bash_command=(
            "curl -X POST -F file=@/opt/airflow/branch_dim_largedata.csv "
            "-H 'Content-Type: multipart/form-data' "
            "'http://pinot-controller:9000/ingestFromFile?"
            "tableNameWithType=branch_dim_OFFLINE&batchConfigMapStr=%7B"
            "%22inputFormat%22%3A%22csv%22%2C"
            "%22recordReader.prop.delimiter%22%3A%22%2C%22%7D'"
        )
    )


    ingest_account_data>>ingest_branch_data>>ingest_customer_data

    