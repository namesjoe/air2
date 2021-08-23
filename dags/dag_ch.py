from datetime import timedelta
from airflow import DAG
import requests
from urllib.parse import urlencode
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import logging
import os


fn = 'event-data.json'
logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )

default_args = {
    'owner': 'sedov',
    'depends_on_past': False,
    'email': ['namesoe@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}


def download_it():

    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = 'https://disk.yandex.ru/d/ARJShvDUgazjMQ'

    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']

    download_response = requests.get(download_url)
    with open(fn, 'w') as f:
        f.write(download_response.text)
    logging.info('File event-data.json downloaded')


def upload_ch():
    bsh_q = f'cat {fn} | clickhouse-client --query= "INSERT INTO default.songs FORMAT JSONEachRow"'
    os.system(f"{bsh_q}")
    logging.info('Data Uploaded')


def clean():
    try:
        os.remove(fn)
        logging.info(f'File {fn} removed')
    except OSError:
        pass


with DAG('ch_dag', default_args=default_args, description='Clickhouse dag', schedule_interval=timedelta(days=1),
         start_date=days_ago(7)) as dag:

    t1 = PythonOperator(task_id='download_data', python_callable=download_it)
    t2 = PythonOperator(task_id='upload_to_db', python_callable=upload_ch)
    t3 = PythonOperator(task_id='collect_garbage', python_callable=clean)


t1 >> t2 >> t3

