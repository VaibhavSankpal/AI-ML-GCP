## install packages ##
dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE)  # create personal library
.libPaths(Sys.getenv("R_LIBS_USER"))  # add to the path
 
source('gcshelper.R')
install.packages("dplyr")
message('dplyr is installed now...')

# ## Test dplyr package
library("dplyr")
message('dplyr is loaded now...')

# ## Test tidyverse package
# library("tidyverse")
# message('tidyverse is loaded now...')

# An example of loading objects from GCS bucket

bucket_name = 'prd-65343-modelmgmt-ds-ml'
blob_path = 'census/output/model.joblib'
local_path = '.'
download_from_bucket(bucket_name, blob_path, local_path)
message('model uploaded successfully!')

list.dirs('.', recursive=FALSE)

# import the helper module
source('bqhelper.R')

# source of the data is from UCLA which has 4 variable called admit, GRE score, GPA and rank of their undergrad school
sql_query <- "SELECT * FROM `prd-65343-datalake-bd-88394358.modelmgmt_65343_ds.binary_test_data`"
df <- readfrombigquery(sql_query)
message('read data from BQ table...')

# check the type of variables
str(df)

# check for null values
sum(is.na(df))

summary(df)

# check if the admits are distributed well enough in each category of rank
xtabs(~ admit +rank ,data=df)

# convert rank variable from integer to factor
df$rank <- as.factor(df$rank)

# Run the logit function
logit <- glm(admit ~ gre+gpa+rank,data=df,family="binomial")
summary(logit)

# PREDICTION
x <- data.frame(df)
pred <- predict(logit,x)
df['prediction_result'] <- pred

# Writing back the data and its prediction results
targetbqtable <- 'prd-65343-datalake-bd-88394358.65343_modelmgmt_ds.binary_pred_results'
writetobigquery(df, targetbqtable)