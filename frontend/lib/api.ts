import { CustomMetaData } from "@/models/metadata.type";

export async function getGeoTIFFMetadata() {
    const response = await fetch("http://localhost:8000/data/query");
    if (!response.ok) {
        throw new Error("Failed to fetch metadata");
    }
    return await response.json() as CustomMetaData;
}

export async function downloadGeoTIFF() {
    const response = await fetch("http://localhost:8000/data/download");
    if (!response.ok) {
        throw new Error("Failed to download GeoTIFF");
    }
    
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "sample_lst_geotiff.tif"; // Suggest a filename
    document.body.appendChild(link);
    link.click();
    link.remove();
}