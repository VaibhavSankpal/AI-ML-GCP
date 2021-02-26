upload_to_bucket <- function (bucket_name, blob_path, local_path) {

# This function will upload a BLOB to GCS bucket. 
# Use this function while using Notebook service account to authenticate for GCS service usage.
# Parameters: 
# local_path: source path such as local directory where the object is available for upload
# bucket_name: name of the destination bucket
# blob_path: path within the bucket where the object will get uploaded
        
    output <- tryCatch(
      {
          # Command to upload file from local to GCS bucket
          command <- paste('gsutil cp -r ', local_path , ' gs://', bucket_name, '/', blob_path, '/', sep="")
          #print(command)
          system(command)          
      },
      error=function(cond) {
          print(paste("upload_to_bucket: Error uploading to bucket -> " ,cond$message))
          print(command)
      },
      finally = {
          print("Exiting the gcshelper function: upload_to_bucket")
      }
    )
}

# Example for calling the function: upload_to_bucket from R script
# source('gcshelper.R')
# LOCAL_PATH <- "/home/jupyter/test_folder/file1.csv"
# BUCKET_NAME <- "testbkt-temp"
# BLOB_PATH <- "folder1"
# upload_to_bucket(BUCKET_NAME, BLOB_PATH, LOCAL_PATH)


download_from_bucket <- function (bucket_name, blob_path, local_path) {
    
# This function will download a BLOB from a GCS bucket. 
# Use this function while using Notebook service account to authenticate for GCS service usage.
# Parameters: 
# bucket_name: name of the source bucket
# blob_path: path within the bucket where the object is available for download
# local_path: destination path such as local directory where the object will be downloaded
    
    output <- tryCatch(
      {
          # Command to download file from GCS bucket to local
          command <- paste('gsutil cp -r ', ' gs://', bucket_name, '/', blob_path, ' ', local_path , sep="")
          #print(command)
          system(command)
      },
      error=function(cond) {
          print(paste("download_from_bucket: Error downloading to bucket -> " ,cond$message))
          print(command)
      },
      finally = {
          print("Exiting the gcshelper function: download_from_bucket")
      }
    )
}

# Example for calling the function: download_from_bucket from R script
# source('gcshelper.R')
# BUCKET_NAME <- "testbkt-temp"
# BLOB_PATH <- "folder6/file1.csv"
# LOCAL_PATH <- "/home/jupyter/test_folder"
# download_from_bucket(BUCKET_NAME, BLOB_PATH, LOCAL_PATH)