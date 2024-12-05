
import dynamic from "next/dynamic";
import { getGeoTIFFMetadata, downloadGeoTIFF } from "../lib/service";
import {CustomMetaData} from "@/models/metadata.type"
import "../app/globals.css";

const GeoTIFFMap = dynamic(() => import('./Map'), { ssr: false, loading: () => <p>A map is loading</p>, });

export async function getServerSideProps() {
    try {
        const metadata = await getGeoTIFFMetadata();
        return { props: { metadata } };
    } catch (error) {
        return { props: { metadata: null, error: error } };
    }
}

export default function Home({metadata, error}: { metadata: CustomMetaData, error: {message: string} }) {
    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <div>
            <h1>Satellite Data</h1>
            <GeoTIFFMap />
            {metadata ? (
                <div>
                    <p><strong>File Name:</strong> {metadata.file_name}</p>
                    <p><strong>Data Type:</strong> {metadata.data_type}</p>
                    <p><strong>Format:</strong> {metadata.format}</p>
                    <p><strong>CRS:</strong> {metadata.crs}</p>
                    <p><strong>Description:</strong> {metadata.description}</p>
                    <button onClick={downloadGeoTIFF}>Download GeoTIFF</button>
                </div>
            ) : (
                <p>No metadata available</p>
            )}
        </div>
    );
}
