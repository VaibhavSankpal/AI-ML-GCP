import argparse
import trainer.model as model  # Your model.py file.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Input Arguments
    parser.add_argument(
        '--model-bucket',
        help = 'GCS Bucket name where model files are located',
        required = True
    )
    parser.add_argument(
        '--output-dir',
        help = 'GCS location to load models from',
        required = True
    )
    args,unknown  = parser.parse_known_args()

    # Assign model variables to commandline arguments
    model.BUCKET_NAME = args.model_bucket
    model.OUTPUT_DIR = args.output_dir
    
    # Run the prediction job
    model.run()