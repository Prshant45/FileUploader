**Pre-requisite:**
1. you can set the env variable or change the values of s3_cred.txt or gcloud_cred.txt with actual value for s3 bucket and Google Storage
2. If you are setting the env variable for google storage set the name of variable as GOOGLE_STORAGE_CREDENTIALS and value as 

		{
		"json_auth":{
					"type": "service_account",
					"client_id": "client_id",
					"client_email": "client_email",
					"private_key_id": "private_key_id",
					"private_key": "private_key"
		},
		"project_name":"project_name",
		"bucket_name":"bucket_name"
		}
		(Note: change the value with actual value before using it )

3. If you are setting the env variable for s3 bucket set the name of variable as S3_CREDENTIALS and value as 
		{
			"aws_access_key_id": "aws_access_key_id",
			"aws_secret_access_key": "aws_secret_access_key",
			"bucket_name": "uipath-test-xlsx"
		}
		(Note: change the value with actual value before using it )

4. You can give file type configuration file at runtime or you can use default settings set in the s3_file.txt(you can modify as per your need) or g_file.txt(you can modify as per your need)


**Project setting:**
1. To create the virtual env, run below command in the prompt
	python -m venv env
2. activate the virtual env
	for windows: .\env\Scripts\activate
	for linux: source ./env/bin/activate
3. install the requirements.txt
	pip install -r requirements.txt
4. to run:
	python main.py

**To run pytest:**
run below command to check coverage and test

coverage run --source=exam -m pytest -v . && coverage report -m
