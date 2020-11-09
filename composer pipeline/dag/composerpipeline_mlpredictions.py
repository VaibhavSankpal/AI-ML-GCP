import datetime
import time
import uuid
from airflow import models
from airflow.contrib.operators import mlengine_operator

updated_time = time.strftime('%d-%m-%Y %H:%M:%S')

#gcs_bucket = models.Variable.get('gcs_bucket1')
#bq_dataset_name = models.Variable.get('bq_dataset_name')
#bq_table_id = bq_dataset_name + '.temp_table'
#output_file = '{bq_dataset_name}/composer_test_data {current_time}.csv'.format(
#    bq_table_id=models.Variable.get('bq_dataset_name'), current_time=updated_time)

#BUCKET_ID = models.Variable.get('BUCKET_ID')
#PROJECT_ID = models.Variable.get('PROJECT_ID')
#RUNTIME_VERSION = models.Variable.get('runtime_version')
#PYTHON_VERSION = models.Variable.get('python_version')
#TRAIN_DATA_PATHS = models.Variable.get('TRAIN_DATA_PATHS')
#OUTPUT_DIR = models.Variable.get('OUTPUT_DIR')
BUCKET_NAME = 'cap-4985-modelmanagement'
OUTPUT_DIR = 'census/output'


yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

default_dag_args = {
    'start_date': yesterday,
    #'retries': 0,
    #'retry_delay': datetime.timedelta(minutes=2),
    #'project_id': models.Variable.get('gcp_project')
}

with models.DAG(
        'composer_ml_batch_predictions',
        # Manually trigger the DAG, so no schedule required
        schedule_interval=None, default_args=default_dag_args) as dag:

    predict_model = mlengine_operator.MLEngineTrainingOperator(
        task_id='predict_model',
        project_id='sb-bigdata-4985-da852265',
        job_id='{}_{}'.format('census_batch_prediction_job', str(uuid.uuid4())),
        package_uris='gs://cap-4985-modelmanagement/census/package/prediction/census-batch-prediction-package-0.1.tar.gz',
        training_python_module='trainer.task',
        training_args=['--bucket_name', BUCKET_NAME, '--output_dir', OUTPUT_DIR],
        region='us-central1',
        scale_tier='BASIC',
        runtime_version='1.13',
        python_version='3.5'
    )

    predict_model