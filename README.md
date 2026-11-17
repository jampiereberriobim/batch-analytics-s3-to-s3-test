
Get-ChildItem -Path . -Directory -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force

docker run -p 9000:8080 `
-e AWS_PROFILE=PDP-ANALYTICS-QA `
-e AWS_REGION=us-east-1 `
-e TABLE_NAME=s3_to_s3_copy `
-v "${env:USERPROFILE}\.aws:/root/.aws" `|

