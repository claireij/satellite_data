import rasterio
import boto3
from io import BytesIO
from fastapi import HTTPException
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, AWS_OBJECT_KEY

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def get_geotiff_data():
    try:
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=AWS_OBJECT_KEY)
        file_content = response['Body'].read()
        file_like_object = BytesIO(file_content)
        return rasterio.open(file_like_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def download_file(file_name: str):
    try:
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=file_name)
        file_content = response['Body'].read()
        return file_content
    except Exception as e:
        raise Exception(f"Error downloading file {file_name}: {str(e)}")