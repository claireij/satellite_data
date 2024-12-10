from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel
from aws_service import get_geotiff_data, download_file
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
from config import AWS_OBJECT_KEY, FRONTEND_URL
from data_processing import transform_coordinates, generate_image_from_raster

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to satellite data"}

@app.get("/data/metadata")
def query_data():
        try:
            with get_geotiff_data() as dataset:
            
                south_west, north_east = transform_coordinates(dataset)

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
            buffer = generate_image_from_raster(raster_data)

            return StreamingResponse(buffer, media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/download")
def download_data():
    try:        
        file_content = download_file(AWS_OBJECT_KEY)
        file_like_object = BytesIO(file_content)

        return Response(file_like_object.getvalue(), media_type="image/tiff", headers={"Content-Disposition": f"attachment; filename={AWS_OBJECT_KEY}"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))