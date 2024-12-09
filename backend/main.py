from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
import os
import rasterio
import boto3
from dotenv import load_dotenv
from io import BytesIO
from pyproj import Proj, transform
from rasterio.plot import show
from PIL import Image
import numpy as np
import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import rasterio
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME= os.getenv('AWS_BUCKET_NAME')
AWS_OBJECT_KEY = os.getenv('AWS_OBJECT_KEY')

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def get_geotiff_data():
    try:
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=AWS_OBJECT_KEY)
        file_content = response['Body'].read()
        file_like_object = BytesIO(file_content)
        return rasterio.open(file_like_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to satellite data"}

@app.get("/data/metadata")
def query_data():
        try:
            with get_geotiff_data() as dataset:
                print("dataset", dataset)
                print(dataset.bounds)
            
            src_proj = Proj("epsg:32633")
            dest_proj = Proj("epsg:4326")

            left, bottom, right, top = dataset.bounds

            print(left, bottom, right, top)

            south_west = transform(src_proj, dest_proj, left, bottom)
            north_east = transform(src_proj, dest_proj, right, top)

            print(dataset)

            return {
                "bounds": [south_west, north_east],
                "crs": str(dataset.crs) if dataset.crs else "Unknown",
                "data_type": str(dataset.dtypes[0]) if dataset.dtypes[0] else "Unknown",
                "file_format": str(dataset.driver) if dataset.driver else "Unknown",
                "description": dataset.tags().get('DESCRIPTION', "No description available"),
                "file_name": AWS_OBJECT_KEY
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/image")
async def generate_image():
    try:
        with get_geotiff_data() as dataset:
            raster_data = dataset.read(1)
            
            normalized_data = ((raster_data - raster_data.min()) / 
                              (raster_data.max() - raster_data.min()) * 255).astype(np.uint8)

            # Convert the normalized data to a grayscale image
            image = Image.fromarray(normalized_data, mode="L")

            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            return StreamingResponse(buffer, media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/download")
def download_data():
    try:
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=AWS_OBJECT_KEY)
        
        file_content = response['Body'].read()
        file_like_object = BytesIO(file_content)

        filename = AWS_OBJECT_KEY  # You can also get this directly from `response` if needed

        return Response(file_like_object.getvalue(), media_type="image/tiff", headers={"Content-Disposition": f"attachment; filename={AWS_OBJECT_KEY}"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))