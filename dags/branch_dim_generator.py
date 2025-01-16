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
output_file = './branch_dim_largedata.csv'

cities = ['London', 'Manchester','Birmingham', 'Glasgow', 'Edinburgh']
regions = ['London','Greater Manchester', 'West Midlands', 'Scotland']
postcodes = ['EC1A 1BB', 'M1 1AE', 'B1 1AA', 'G1 1AA', 'EM1 1AA']





def generate_random_data(row_num):
    branch_id = f'B{row_num:05d}'
    branch_name = f'Branch {row_num}'
    branch_address= f"{random.randint(1,999)} {random.choice(['High St', 'King St', 'Queen St', 'Churh Rd'])}"
    city= random.choice(cities)
    region= random.choice(regions)
    postcode= random.choice(postcodes)

    now = datetime.now()
    random_date = now-timedelta(days=random.randint(1,3650))
    opening_date_milli = int(random_date.timestamp()*1000)
    return branch_id, branch_name, branch_address, city, region, postcode, opening_date_milli

def generate_branch_dim_data(num_rows):

    branch_ids=[]
    branch_names=[]
    branch_addresses=[]
    branch_cities=[]
    branch_regions=[]
    branch_postcodes=[]
    opening_dates=[]

    row_num = 1
    while row_num <= num_rows:
        branch_id, branch_name, branch_address, city, region, postcode, opening_date_milli = generate_random_data(row_num)
        branch_ids.append(branch_id)
        branch_names.append(branch_name)
        branch_addresses.append(branch_address)
        branch_cities.append(city)
        branch_regions.append(region)
        branch_postcodes.append(postcode)
        opening_dates.append(opening_date_milli)
        row_num+=1 
        
    data = {
        'branch_id': branch_ids,
        'branch_name': branch_names,
        'branch_address': branch_addresses, 
        'city': branch_cities,
        'region': branch_regions,
        'postcode': branch_postcodes,
        'opening_date': opening_date_milli
    }

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

    print(f'CSV file with {num_rows} has been generated successfully!')


with DAG('branch_dim_generator',
         default_args= defaul_args,
         description= 'Generate large branch dimension data in a csv file',
         schedule_interval= timedelta(days=1),
         start_date= start_date,
         tags= ['schema']) as dag:
    start= EmptyOperator(
        task_id= 'start_task'
    )

    generate_branch_dimension_data= PythonOperator(
        task_id= 'generate_branch_dim_data',
        python_callable= generate_branch_dim_data,
        op_args=[num_rows]
    )

    end= EmptyOperator(
        task_id= 'end_task'
    )

    start >> generate_branch_dimension_data >> end

