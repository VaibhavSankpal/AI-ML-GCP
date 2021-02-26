readfrombigquery <- function (query, page_size = 1000) {

# This function will read the data from a BQ table 
# Parameters: 
# query: BigQuery query to be executed 
# Returns: 
# df: Pandas dataframe for bigquery table
    
    output <- tryCatch(
      {
          # Load the package
          library(bigrquery)
          # Set Authentication
          bq_auth(scopes="https://www.googleapis.com/auth/bigquery")
          # Get current project id 
          projectid <- system('gcloud config list project --format "value(core.project)"', intern = TRUE)
          # Fix for loading large datasets
          options(scipen = 20)
          # Get the Query output in dataframe
          #print(page_size)
          # Fix (page_size) for selecting tables having ave many fields or large records 
          df <- bq_table_download(bq_project_query(projectid,query=query),page_size = page_size )
          return(df)
      },
      error=function(cond) {
          print(paste("readfrombigquery: Error reading bigquery table -> " ,cond$message))
      },
      finally = {
          print("Exiting the bqhelper function: readfrombigquery")
      }
    )
}

# Example for calling the function: readfrombigquery from R script
# source("./bqhelper.R")
# sql_query <- "SELECT * FROM `prd-65343-datalake-bd-88394358.65343_modelmgmt_ds.binary`"
# df <- readfrombigquery(sql_query) 
# df <- readfrombigquery(query, 2000) ## to pass the pasge size
# page_size : The number of rows returned per page. Make this smaller if you have many
#fields or large records and you are seeing a ’responseTooLarge’ error.
# Reference : https://cran.r-project.org/web/packages/bigrquery/bigrquery.pdf

writetobigquery <- function (df, targetbqtable) {
# This function will write the data to a BQ table. 
# Table columns Fields must contain only letters, numbers, and underscores, start with a letter or underscore, 
# and be at most 128 characters long.
#    
# Parameters: 
# df: dataframe to be written to BQ table
# targetbqtable: destination BQ table
    
    output <- tryCatch(
      {
          # Load the package
          library(bigrquery)
          # Set Authentication
          bq_auth(scopes="https://www.googleapis.com/auth/bigquery")
          # Fix for loading large datasets
          options(scipen = 20)
         
          library(dplyr)
          # Number of items in each chunk
          elements_per_chunk = 100000
          n_chunks <- ceiling(nrow(df)/elements_per_chunk) # 2. identify how many files to make
          chunk_starts <- seq(1, elements_per_chunk*n_chunks, by = elements_per_chunk) #  3. identify the rown number to start on
          for (i in 1:n_chunks) # 4. iterate through the csv to write the files
          {  
              chunk_end <- elements_per_chunk*i # 4a
              df_to_write <- slice(df, chunk_starts[i]:chunk_end) # 4b
              job <- bq_perform_upload(targetbqtable, df_to_write, fields= as_bq_fields(df),create_disposition = "CREATE_IF_NEEDED", write_disposition = "WRITE_APPEND")
              bq_job_wait(job)
          }
      },
      error=function(cond) {
          print(paste("writetobigquery: Error writing bigquery table -> " ,cond$message))
      },
      finally = {
          print("Exiting the bqhelper function: writetobigquery")
      }
    )
    }

# Example for calling the function: writetobigquery from R script
# source("./bqhelper.R")
# targetbqtable <- 'prd-65343-datalake-bd-88394358.65343_modelmgmt_ds.binary_prediction_results1'
# writetobigquery(df1, targetbqtable)
