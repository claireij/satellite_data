# Satellite Data Visualization
This project provides a web-based tool for visualizing geospatial data using satellite imagery. It integrates with AWS S3 to fetch GeoTIFF files and offers functionality to transform, display, and interact with geospatial data on the web.

## Features
Coordinate Transformation: Converts bounding box coordinates from EPSG:32633 (UTM) to EPSG:4326 (latitude/longitude).
Satellite Image Rendering: Generates grayscale visualizations from GeoTIFF raster data.
Map Integration: Displays geospatial data on an interactive map using Leaflet.js.
File Download: Provides GeoTIFF files for download via a REST API.
Cloud Integration: Fetches satellite data from AWS S3 storage.

## Tech Stack
- Backend: Python, FastAPI, Rasterio, PyProj
- Frontend: Next.js (React framework), Leaflet.js for map rendering
- Cloud Services: AWS S3 for storing and retrieving satellite data
- Testing: Selenium (E2E tests), unittest (backend)

## Installation

Clone the Repository:
```
git clone https://github.com/claireij/satellite_data.git
cd satellite_data
```

Install Dependencies:
```
pip install -r requirements.txt
```

Environment Variables: Create a .env file in the project root and add the following variables:
```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=your_bucket_name
AWS_OBJECT_KEY=your_geotiff_file_key
```

Run the Application:
```
Access the API: Open your browser at http://127.0.0.1:8000.
```

## API Endpoints
Method	Endpoint	Description
- GET	/	Welcome message
- GET	/data/query	Fetch metadata about the GeoTIFF file
- GET	/data/download	Download the GeoTIFF file
- GET	/generate-image	Generate and download an image (PNG)

## Usage
### Fetch GeoTIFF Metadata
Make a GET request to /data/query. Example response:
```
{
  "bounds": [[lon_min, lat_min], [lon_max, lat_max]],
  "crs": "EPSG:4326",
  "data_type": "float32",
  "file_format": "GTiff",
  "description": "No description available",
  "file_name": "example.tiff"
}
```
### Visualize Satellite Data
Use the /generate-image endpoint to get a normalized grayscale PNG of the satellite raster data.

### Download the GeoTIFF File
Make a GET request to /data/download to download the original GeoTIFF file.

## Development
### Run Tests
Unit tests are located in the tests directory. Use the following command to run them:
```
python -m unittest discover
```

