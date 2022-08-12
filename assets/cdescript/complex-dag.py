# Airflow DAG Which Runs Tree of Spark Tasks which are dependent

from datetime import datetime, timedelta
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator
from cloudera.cdp.airflow.operators.cde_operator import CDEJobRunOperator

default_args = {
    'owner': 'dexuser',
    'depends_on_past': False,
}

dag = DAG(
    'spark_cde_dependent_chain_dag',
    default_args=default_args,
    start_date=timezone.utcnow(),
    # end_date=datetime.combine(datetime.today() + timedelta(1), datetime.min.time()),
    schedule_interval='@once',
    catchup=False,
    is_paused_upon_creation=False
)

create_db = CDEJobRunOperator(
    task_id='create-database',
    dag=dag,
    job_name='spark_sql_shell_mimic',
    variables={
        'spark_queries': 'CREATE database if not exists dex_db'
    }
)

drop_table1 = CDEJobRunOperator(
    task_id='drop_table1',
    dag=dag,
    job_name='spark_sql_shell_mimic',
    variables={
        'spark_queries': 'DROP TABLE IF EXISTS dex_db.table1'
    }
)

drop_table2 = CDEJobRunOperator(
    task_id='drop_table2',
    dag=dag,
    job_name='spark_sql_shell_mimic',
    variables={
        'spark_queries': 'DROP TABLE IF EXISTS dex_db.table2'
    }
)

create_table1 = CDEJobRunOperator(
    task_id='create_table1',
    dag=dag,
    job_name='spark_sql_shell_mimic',
    variables={
        'spark_queries': 'CREATE TABLE dex_db.table1 (key INT, value STRING)'
    },
    overrides={
        'spark': {
            'numExecutors': 2
        }
    }
)

create_table2 = CDEJobRunOperator(
    task_id='create_table2',
    dag=dag,
    job_name='spark_sql_shell_mimic',
    variables={
        'spark_queries': 'CREATE TABLE dex_db.table2 (key INT, value STRING)'
    },
    overrides={
        'spark': {
            'numExecutors': 2
        }
    }
)

insert_table1 = CDEJobRunOperator(
    task_id='insert_table1',
    dag=dag,
    job_name='spark_sql_shell_mimic',
    variables={
        'spark_queries': "INSERT INTO TABLE dex_db.table1 values (1, 'airflow')"
    },
    overrides={
        'spark': {
            'numExecutors': 2
        }
    }
)

insert_table2 = CDEJobRunOperator(
    task_id='insert_table2',
    dag=dag,
    job_name='spark_sql_shell_mimic',
    variables={
        'spark_queries': "INSERT INTO TABLE dex_db.table2 values (1, 'custom-dag')"
    },
    overrides={
        'spark': {
            'numExecutors': 2
        }
    }
)

check_task = CDEJobRunOperator(
    task_id='validate_task',
    dag=dag,
    job_name='spark_sql_shell_mimic',
    variables={
        'spark_queries': 'SELECT count(*) from dex_db.table1 as a, dex_db.table2 as b where a.key=b.key'
    },
    overrides={
        'spark': {
            'numExecutors': 3
        }
    }
)

dummy1 = DummyOperator(task_id='run_dummy1', dag=dag,)
dummy2 = DummyOperator(task_id='run_dummy2', dag=dag,)

# pylint: disable=pointless-statement,line-too-long
create_db >> [drop_table1, drop_table2] >> dummy1 >> [create_table1, create_table2] >> dummy2 >> [insert_table1, insert_table2] >> check_task
