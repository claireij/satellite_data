from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
import os
import rasterio
import boto3
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME= os.getenv('AWS_BUCKET_NAME')
AWS_OBJECT_KEY = os.getenv('AWS_OBJECT_KEY')

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

class MetaData(BaseModel):
    id: str
    file_name: str
    data_type: str
    format: str
    crs: str
    description: str


@app.get("/")
def read_root():
    return {"message": "Welcome to satellite data"}

@app.get("/data/query")
def query_data():
        try:
            response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=AWS_OBJECT_KEY)
            
            file_content = response['Body'].read()
            file_like_object = BytesIO(file_content)
            
            with rasterio.open(file_like_object) as dataset:
                custom_metadata = dataset.tags()

            return custom_metadata
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/download")
def download_data():
    try:
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=AWS_OBJECT_KEY)
        
        file_content = response['Body'].read()
        file_like_object = BytesIO(file_content)

        return Response(file_like_object.getvalue(), media_type="image/tiff", headers={"Content-Disposition": "attachment; filename=sample_lst_geotiff.tif"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))