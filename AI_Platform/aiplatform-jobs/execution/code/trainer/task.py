import argparse
#
import trainer.model as model  # Your model.py file.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # # Input Arguments
    parser.add_argument(
        '--model-bucket',
        help = 'GCS Bucket name for storing output model files',
        required = True
    )
    # Output Arguments
    parser.add_argument(
        '--output-dir',
        help = 'GCS location to export models',
        required = True
    )
    args,unknown  = parser.parse_known_args()
    # Assign model variables to commandline arguments
    model.BUCKET_NAME = args.model_bucket
    model.OUTPUT_DIR = args.output_dir
    
    # Run the prediction job
    model.run()