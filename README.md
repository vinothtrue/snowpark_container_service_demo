# snowpark_container_service_demo
SF ML model creation,deployment in SPCS ,and access via streamlit app
1.Ingest the raw data into snowflake
2.run the snowflake notebook to create model,register the model in registry
3.use the container service,image repositroy to create a service
4.create a user and programmatic access token(PAT)
5.check the network ip policy
6.collect the PAT,service end point URL
7.in streamlit secrets ,update the PAT,and endpoint with "/predict" method like below
SCORING_ENDPOINT = "https://XXXXX/predict" and run the script
