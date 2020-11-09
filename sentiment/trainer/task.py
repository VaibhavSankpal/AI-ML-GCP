import argparse
import logging
import trainer.model as model

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input_table_name',
        help = 'Input Big Query Table Name',
        required = True
    )
    parser.add_argument(
        '--model_gcs_bucket_name',
        help = 'GCS Bucket name having the model files',
        required = True
    )
    parser.add_argument(
        '--model_gcs_bucket_path',
        help = 'GCS Bucket path having the model files',
        required = True
    )
    parser.add_argument(
        '--output_table_name',
        help = 'Output Big Query Table Name',
        required = True
    )

    args = parser.parse_args()
    # Assign model variables to commandline arguments
    model.varinputbqtable = args.input_table_name
    model.varmodelgcsbucketname = args.model_gcs_bucket_name
    model.varmodelgcsbucketpath = args.model_gcs_bucket_path
    model.varoutputbqtable = args.output_table_name
    
    # Run the training job
    model.run()