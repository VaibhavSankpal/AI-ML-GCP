import argparse
#
import trainer.model as model  # Your model.py file.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Input Arguments
    parser.add_argument(
        '--bucket_name',
        help = 'GCS Bucket name for storing output model files',
        required = True
    )
    # Output Arguments
    parser.add_argument(
        '--output_dir',
        help = 'GCS location to export models',
        required = True
    )
    args = parser.parse_args()
    # Assign model variables to commandline arguments
    model.BUCKET_NAME = args.bucket_name
    model.OUTPUT_DIR = args.output_dir
    # Run the training job
    model.train_and_evaluate(args)