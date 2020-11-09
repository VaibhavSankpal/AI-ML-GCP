# import the helper module
source('bqhelper.R')

# source of the data is from UCLA which has 4 variable called admit, GRE score, GPA and rank of their undergrad school
sql_query <- "SELECT * FROM `prd-65343-datalake-bd-88394358.65343_modelmgmt_ds.binary`"
df <- readfrombigquery(sql_query)

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
targetbqtable <- 'prd-65343-datalake-bd-88394358.65343_modelmgmt_ds.binary_prediction_results'
writetobigquery(df, targetbqtable)