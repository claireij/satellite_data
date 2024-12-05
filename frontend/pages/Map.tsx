import { MapContainer, TileLayer, ImageOverlay } from 'react-leaflet';
import { useEffect, useState, useCallback } from 'react';
import "leaflet/dist/leaflet.css";
import "leaflet-defaulticon-compatibility";
import "leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css";
import { getGeoTIFFMetadata, getTIFFImage } from '@/lib/service';
import { Bounds } from '@/models/metadata.type';

const Map = () => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [bounds, setBounds] = useState<Bounds | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchMapData = useCallback(async () => {
    try {
      const [metadata, image] = await Promise.all([
        getGeoTIFFMetadata(),
        getTIFFImage(),
      ]);

      setBounds(metadata.bounds);
      setImageUrl(image);
    } catch (error) {
      console.error("Error fetching GeoTIFF data:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMapData();
  }, [fetchMapData]);

  if (loading) return <p>Loading map...</p>;
  if (!bounds || !imageUrl) return <p>Failed to load map data.</p>;

  return (
    <div>
      <MapContainer
        center={bounds[0]}
        zoom={6}
        scrollWheelZoom={false}
        style={{ height: "400px" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <ImageOverlay url={imageUrl} bounds={bounds} />
      </MapContainer>
    </div>
  );
};

export default Map;
