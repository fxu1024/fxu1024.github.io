from dateutil import parser
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from dateutil import parser
from airflow.utils import timezone
from airflow import DAG
from cloudera.cdp.airflow.operators.cde_operator import CDEJobRunOperator


default_args = {
    'owner': 'cdpuser1',
    'retry_delay': timedelta(seconds=5),
    'depends_on_past': False,
}

example_dag = DAG(
    'cdeoperator-job',
    default_args=default_args,
    start_date=parser.isoparse("2020-11-11T20:20:04.268Z").replace(tzinfo=timezone.utc),
    # end_date=datetime.combine(datetime.today() + timedelta(1), datetime.min.time()),
    schedule_interval='@once',
    # catchup=True,
    is_paused_upon_creation=False
)

ingest_step1 = CDEJobRunOperator(
    connection_id='cde_runtime_api',
    task_id='ingest',
    retries=3,
    dag=example_dag,
    job_name='spark-scala-pi-job'
)

prep_step2 = CDEJobRunOperator(
    task_id='data_prep',
    dag=example_dag,
    job_name='spark-scala-pi-job'
)

ingest_step1 >> prep_step2
