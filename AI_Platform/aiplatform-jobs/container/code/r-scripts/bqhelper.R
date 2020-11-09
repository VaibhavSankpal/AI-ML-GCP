readfrombigquery <- function (query) {
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
          df <- bq_table_download(bq_project_query(projectid,query=query))
          return(df)
      },
      error=function(cond) {
          print(paste("readfrombigquery: Error reading bigquery table -> " ,cond$message))
      },
      finally = {
          #print("readfrombigquery: IN FINALLY")
      }
    )
}

writetobigquery <- function (df, targetbqtable) {
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
          #print("writetobigquery: IN FINALLY")
      }
    )
    }