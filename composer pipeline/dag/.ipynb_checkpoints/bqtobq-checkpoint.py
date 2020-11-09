import datetime
import time

from airflow import models
from airflow.contrib.operators import bigquery_operator
from airflow.contrib.operators import bigquery_to_bigquery
from airflow.contrib.operators import bigquery_table_delete_operator
from airflow.utils import trigger_rule

updated_time = time.strftime('%d-%m-%Y_%H:%M:%S')
project_id = 'sb-bigdata-4985-da852265'
#gcs_bucket = 'gs://cap-4985-modelmanagement/census/output'
input_bq_table = 'modelmanagement.census_income_data'
output_bq_dataset = 'modelmanagement'
#bq_table_id = output_bq_dataset + '.temp_table'
output_file = '{bq_dataset}.composer_census_data'.format(
    bq_dataset=output_bq_dataset)

yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    'start_date': yesterday,
#    'retries': 1,
#    'retry_delay': datetime.timedelta(minutes=2),
#    'project_id': models.Variable.get('gcp_project')
}


##SELECT DocumentNo,Emp_ID from myte.mytedatatable where Experienced_Hire = true

with models.DAG(
        'current_data',
        schedule_interval=None,
        default_args=default_dag_args) as dag:

    query_census_table = bigquery_operator.BigQueryOperator(
        task_id='query_table',
        bql="""
        SELECT age, workclass, functional_weight, education, education_num, marital_status, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income_bracket FROM `{bq_table}`
        """.format(bq_table=input_bq_table),
        use_legacy_sql=False,
        destination_dataset_table=output_file,
        write_disposition='WRITE_TRUNCATE')

    ( 
    query_census_table
    )