import random
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd


start_date =datetime(2025,1,16)

defaul_args = {
    'owner':'olivier',
    'depends_on_past':False,
    'backfill':False
}


num_rows = 50
output_file = './account_dim_largedata.csv'



def generate_random_data(row_num):
    account_id = f'A{row_num:05d}'
    account_type = random.choice(['SAVINGS','CHECKING'])
    status = random.choice(['ACTIVE', 'INACTIVE'])
    customers_id = f'C{random.randint(1,1000):05d}'
    balance = round(random.uniform(100.00,10000.00), 2)

    now = datetime.now()
    random_date = now-timedelta(days=random.randint(1,365))
    opening_date_milli = int(random_date.timestamp()*1000)
    return account_id, account_type, status, customers_id, balance, opening_date_milli

def generate_account_dim_data(num_rows):

    account_ids=[]
    account_types=[]
    statuses=[]
    customers_ids=[]
    balances=[]
    opening_dates=[]

    
    row_num = 1
    while row_num <= num_rows:
        account_id, account_type, status, customers_id, balance, opening_date_milli = generate_random_data(row_num)
        account_ids.append(account_id)
        account_types.append(account_type)
        statuses.append(status)
        customers_ids.append(customers_id)
        balances.append(balance)
        opening_dates.append(opening_date_milli)
        row_num+=1 
        
    data = {
        'account_id': account_ids,
        'account_type': account_types,
        'status': statuses, 
        'customer_id': customers_ids,
        'balance': balances,
        'opening_date': opening_date_milli
    }

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

    print(f'CSV file with {num_rows} has been generated successfully!')


with DAG('account_dim_generator',
         default_args= defaul_args,
         description= 'Generate large account dimension data in a csv file',
         schedule_interval= timedelta(days=1),
         start_date= start_date,
         tags= ['schema']) as dag:
    start= EmptyOperator(
        task_id= 'start_task'
    )

    generate_account_dimension_data= PythonOperator(
        task_id= 'generate_account_dim_data',
        python_callable= generate_account_dim_data,
        op_args=[num_rows]
    )

    end= EmptyOperator(
        task_id= 'end_task'
    )

    start >> generate_account_dimension_data >> end