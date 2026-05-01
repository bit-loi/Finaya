import React, { useState, useEffect, useRef } from 'react';
import L from 'leaflet';
import { MapPin } from 'lucide-react';
import 'leaflet/dist/leaflet.css';
import { Skeleton } from './ui/Skeleton';

// Ensure Leaflet is available globally
if (typeof window !== 'undefined') {
  window.L = L;
}

// Fix Leaflet marker icons in Vite/React - using CDN URLs
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

// A premium golden/yellow glowing marker icon for target locations
const redMarkerIcon = L.divIcon({
  className: 'custom-leaflet-marker-red',
  html: `
    <div style="position: relative; display: flex; justify-content: center; align-items: center; width: 36px; height: 36px;">
      <div style="position: absolute; width: 32px; height: 32px; border-radius: 50%; background: #f59e0b; opacity: 0.4; animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;"></div>
      <div style="position: relative; width: 18px; height: 18px; border-radius: 50%; background: #f59e0b; border: 3px solid #fff; box-shadow: 0 0 8px rgba(0,0,0,0.4);"></div>
    </div>
  `,
  iconSize: [36, 36],
  iconAnchor: [18, 18],
  popupAnchor: [0, -18]
});

// Neon blue marker icon for user's current location
const blueMarkerIcon = L.divIcon({
  className: 'custom-leaflet-marker-blue',
  html: `
    <div style="position: relative; display: flex; justify-content: center; align-items: center; width: 36px; height: 36px;">
      <div style="position: absolute; width: 32px; height: 32px; border-radius: 50%; background: #3b82f6; opacity: 0.4; animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;"></div>
      <div style="position: relative; width: 18px; height: 18px; border-radius: 50%; background: #3b82f6; border: 3px solid #fff; box-shadow: 0 0 8px rgba(0,0,0,0.4);"></div>
    </div>
  `,
  iconSize: [36, 36],
  iconAnchor: [18, 18],
  popupAnchor: [0, -18]
});

// Emerald green marker icon for premium competitors
const greenMarkerIcon = L.divIcon({
  className: 'custom-leaflet-marker-green',
  html: `
    <div style="position: relative; display: flex; justify-content: center; align-items: center; width: 36px; height: 36px;">
      <div style="position: absolute; width: 28px; height: 28px; border-radius: 50%; background: #10b981; opacity: 0.4; animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;"></div>
      <div style="position: relative; width: 16px; height: 16px; border-radius: 50%; background: #10b981; border: 3px solid #fff; box-shadow: 0 0 6px rgba(0,0,0,0.4);"></div>
    </div>
  `,
  iconSize: [36, 36],
  iconAnchor: [18, 18],
  popupAnchor: [0, -18]
});

// Subtle orange/gold for other competitors
const goldMarkerIcon = L.divIcon({
  className: 'custom-leaflet-marker-gold',
  html: `
    <div style="position: relative; display: flex; justify-content: center; align-items: center; width: 36px; height: 36px;">
      <div style="position: absolute; width: 28px; height: 28px; border-radius: 50%; background: #f59e0b; opacity: 0.4; animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;"></div>
      <div style="position: relative; width: 16px; height: 16px; border-radius: 50%; background: #f59e0b; border: 3px solid #fff; box-shadow: 0 0 6px rgba(0,0,0,0.4);"></div>
    </div>
  `,
  iconSize: [36, 36],
  iconAnchor: [18, 18],
  popupAnchor: [0, -18]
});

/**
 * Calculates the appropriate zoom level for a map to display a given radius around a point.
 * Uses the Web Mercator projection formula to determine zoom level.
 *
 * @param {number} latitude - Latitude of the center point in degrees (-90 to 90)
 * @param {number} radiusMeters - Radius to display in meters (must be > 0)
 * @param {number} mapWidthPx - Width of the map container in pixels (must be > 0)
 * @returns {number} Zoom level between 10 and 18
 */
const calculateZoomFromRadius = (latitude, radiusMeters, mapWidthPx) => {
  // Input validation
  if (!radiusMeters || radiusMeters <= 0 || !mapWidthPx || mapWidthPx <= 0) {
    return 18; // Safe zoom level (OSM max is usually 19)
  }

  // Validate latitude range
  if (latitude < -90 || latitude > 90) {
    console.warn('Invalid latitude provided to calculateZoomFromRadius:', latitude);
    return 12;
  }

  try {
    // Formula: zoom = log2((156543.03392 * cos(latitude) * mapWidthPx) / (2 * radiusMeters))
    // This shows the diameter (2 * radius) across the map width
    const cosLat = Math.cos(latitude * Math.PI / 180);
    const zoom = Math.log2((156543.03392 * cosLat * mapWidthPx) / (2 * radiusMeters));

    // Clamp zoom between reasonable bounds and handle edge cases
    if (!isFinite(zoom)) {
      console.warn('Calculated zoom is not finite, using default zoom');
      return 12;
    }

    return Math.max(10, Math.min(18, Math.round(zoom)));
  } catch (error) {
    console.error('Error calculating zoom level:', error);
    return 12; // Fallback to default zoom
  }
};

const MapComponent = ({ onLocationSelect, selectedLocation, onMapReady, buildingWidth, competitors = [] }) => {
  const [mapLoaded, setMapLoaded] = useState(false);
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const circleRef = useRef(null);

  // Inject marker styles for animation and popup styling
  useEffect(() => {
    let style = document.getElementById('leaflet-custom-marker-styles');
    if (!style) {
      style = document.createElement('style');
      style.id = 'leaflet-custom-marker-styles';
      document.head.appendChild(style);
    }
    style.innerHTML = `
      @keyframes pulse {
        0%, 100% {
          transform: scale(0.95);
          opacity: 0.3;
        }
        50% {
          transform: scale(1.2);
          opacity: 0.7;
        }
      }
      .leaflet-div-icon {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
      }
      .leaflet-popup-content-wrapper {
        background: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        padding: 0 !important;
      }
      .leaflet-popup-tip {
        background: #000000 !important;
        border: 1px solid #333333 !important;
      }
      .leaflet-popup-content {
        margin: 0 !important;
        padding: 0 !important;
        background: #000000 !important;
        color: #ffffff !important;
      }
    `;
  }, []);

  // Get user's current location (non-blocking)
  const getUserLocation = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported by this browser'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => {
          console.warn('Geolocation error:', error);
          reject(error);
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000 // 5 minutes
        }
      );
    });
  };

  // Initialize map
  useEffect(() => {
    const initMap = () => {
      // Prevent multiple initializations
      if (mapInstanceRef.current) {
        console.log('Map already initialized, skipping...');
        return;
      }

      try {
        console.log('Starting map initialization...');

        // Check if Leaflet is available
        if (typeof L === 'undefined') {
          console.error('Leaflet not loaded, trying to load from window.L');
          if (typeof window !== 'undefined' && window.L) {
            console.log('Using window.L instead');
            window.L = window.L;
          } else {
            throw new Error('Leaflet not loaded');
          }
        }

        // Wait for DOM to be ready (no delay for instant loading)

        // Get the map container
        const container = document.getElementById('business-map');
        if (!container) {
          throw new Error('Map container not found');
        }

        // Check if container already has a map
        if (container._leaflet_id) {
          console.log('Container already has a map, skipping initialization');
          return;
        }

        console.log('Creating Leaflet map...');

        // Get dynamic map width
        const mapWidthPx = container.offsetWidth || 800; // Fallback to 800 if container not ready

        // Start with Jakarta as default location
        const defaultLocation = { lat: -6.2088, lng: 106.8456 }; // Jakarta coordinates

        const zoomLevel = calculateZoomFromRadius(defaultLocation.lat, parseFloat(buildingWidth) || 0, mapWidthPx);

        // Create map with default location as center
        const map = L.map(container, {
          center: [defaultLocation.lat, defaultLocation.lng],
          zoom: zoomLevel,
          zoomControl: true,
          scrollWheelZoom: true,
          dragging: true
        });

        // Try to get user's location asynchronously (non-blocking)
        console.log('Attempting to get user location...');
        getUserLocation()
          .then((userLocation) => {
            console.log('User location obtained:', userLocation);
            // Update map center to user's location
            map.setView([userLocation.lat, userLocation.lng], zoomLevel);

            // Add blue marker for user's current location
            L.marker([userLocation.lat, userLocation.lng], { icon: blueMarkerIcon })
              .addTo(map)
              .bindPopup(`
                <div style="background: #000000; color: #ffffff; padding: 12px; border-radius: 6px; font-family: 'Inter', sans-serif; line-height: 1.4; border: 1px solid #333333; min-width: 160px;">
                  <strong style="color: #ffffff; font-size: 13px; display: block; margin-bottom: 4px;">Your Current Location</strong>
                  <div style="font-size: 11px; color: #a3a3a3; display: flex; flex-direction: column; gap: 2px;">
                    <div>Lat: <span style="color: #ffffff; font-family: monospace;">${userLocation.lat.toFixed(6)}</span></div>
                    <div>Lng: <span style="color: #ffffff; font-family: monospace;">${userLocation.lng.toFixed(6)}</span></div>
                  </div>
                </div>
              `)
              .openPopup();
          })
          .catch((error) => {
            console.log('Using default location (Jakarta) due to geolocation error:', error.message);
          });

        console.log('Adding map layer...');

        // Define Base Layers
        const streetLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
          maxZoom: 19,
          attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
        });

        const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
          maxZoom: 19,
          attribution: 'Tiles &copy; Esri'
        });

        // Add default layer (Street)
        streetLayer.addTo(map);

        // Add Layer Control (Switch betweeen Street & Satellite)
        const baseMaps = {
          "Carto Street": streetLayer,
          "Satellite View": satelliteLayer
        };

        L.control.layers(baseMaps, null, { position: 'topright' }).addTo(map);

        // Handle tile errors for both
        [streetLayer, satelliteLayer].forEach(layer => {
          layer.on('tileerror', (e) => {
             console.warn('Tile load error:', e);
             if (!layer._backupUsed) {
                layer._backupUsed = true;
                layer.setUrl('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png');
             }
          });
        });

        // Store map instance
        mapInstanceRef.current = map;

        // Add click handler
        map.on('click', (e) => {
          console.log('Map clicked:', e.latlng);
          const { lat, lng } = e.latlng;
          onLocationSelect({ lat, lng });

          // Clear existing markers
          map.eachLayer((layer) => {
            if (layer instanceof L.Marker) {
              map.removeLayer(layer);
            }
          });

          // Add red marker for selected location
          L.marker([lat, lng], { icon: redMarkerIcon })
            .addTo(map)
            .bindPopup(`
              <div style="background: #000000; color: #ffffff; padding: 12px; border-radius: 6px; font-family: 'Inter', sans-serif; line-height: 1.4; border: 1px solid #333333; min-width: 160px;">
                <strong style="color: #ffffff; font-size: 13px; display: block; margin-bottom: 4px;">Selected Location</strong>
                <div style="font-size: 11px; color: #a3a3a3; display: flex; flex-direction: column; gap: 2px;">
                  <div>Lat: <span style="color: #ffffff; font-family: monospace;">${lat.toFixed(6)}</span></div>
                  <div>Lng: <span style="color: #ffffff; font-family: monospace;">${lng.toFixed(6)}</span></div>
                </div>
              </div>
            `)
            .openPopup();
        });

        console.log('Map initialized successfully!');
        console.log('Map instance:', map);
        console.log('Map container size:', container.offsetWidth, 'x', container.offsetHeight);

        // Notify parent component that map is ready
        if (onMapReady) {
          onMapReady(map);
        }

        // Set loaded state immediately after successful initialization
        setMapLoaded(true);

      } catch (error) {
        console.error('Map initialization failed:', error);
        // Create a fallback clickable area
        const container = document.getElementById('business-map');
        if (container) {
          container.innerHTML = `
            <div style="
              width: 100%;
              height: 100%;
              background: linear-gradient(45deg, #fef3c7 25%, transparent 25%),
                          linear-gradient(-45deg, #fef3c7 25%, transparent 25%),
                          linear-gradient(45deg, transparent 75%, #fef3c7 75%),
                          linear-gradient(-45deg, transparent 75%, #fef3c7 75%);
              background-size: 20px 20px;
              background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
              display: flex;
              align-items: center;
              justify-content: center;
              cursor: crosshair;
              color: #1f2937;
              font-family: Arial, sans-serif;
            ">
              <div style="text-align: center; background: rgba(255,255,255,0.9); padding: 20px; border-radius: 8px; border: 2px solid #fbbf24;">
                <h3 style="color: #1f2937;">Click to Select Location</h3>
                <p style="font-size: 14px; color: #6b7280;">Map tiles unavailable - using fallback mode</p>
              </div>
            </div>
          `;

          container.onclick = (e) => {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Convert to approximate lat/lng (very rough approximation)
            const lat = 51.505 + (y - rect.height/2) * -0.001;
            const lng = -0.09 + (x - rect.width/2) * 0.001;

            onLocationSelect({ lat, lng });
            console.log('Fallback location selected:', { lat, lng });
          };
        }
        setMapLoaded(true);
      }
    };

    initMap();
  }, [onLocationSelect]);

  // Handle map resize when window resizes
  useEffect(() => {
    const handleResize = () => {
      if (mapInstanceRef.current) {
        setTimeout(() => {
          mapInstanceRef.current.invalidateSize();
        }, 100);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Update marker and circle when selectedLocation or buildingWidth changes
  useEffect(() => {
    if (mapInstanceRef.current && selectedLocation) {
      // Clear existing markers and circles
      mapInstanceRef.current.eachLayer((layer) => {
        if (layer instanceof L.Marker || layer instanceof L.Circle) {
          mapInstanceRef.current.removeLayer(layer);
        }
      });

      // Calculate appropriate zoom level for the building width radius
      const radiusMeters = parseFloat(buildingWidth) || 0;
      const mapSize = mapInstanceRef.current.getSize();
      const mapWidthPx = (mapSize && mapSize.x > 0) ? mapSize.x : 800;
      const zoomLevel = calculateZoomFromRadius(selectedLocation.lat, radiusMeters, mapWidthPx);

      // Fly to the location with calculated zoom
      mapInstanceRef.current.flyTo([selectedLocation.lat, selectedLocation.lng], zoomLevel, {
        animate: true,
        duration: 1.5
      });

      // Add new marker
      L.marker([selectedLocation.lat, selectedLocation.lng], { icon: redMarkerIcon })
        .addTo(mapInstanceRef.current)
        .bindPopup(`
            <div style="background-color: #000000; color: #ffffff; padding: 12px; border-radius: 6px; border: 1px solid #333333; min-width: 220px; font-family: 'Inter', sans-serif;">
              <h3 style="margin: 0 0 8px 0; font-size: 14px; font-weight: 600; color: #ffffff; display: flex; align-items: center; gap: 6px; padding-right: 24px;">
                 Target Location
              </h3>
              <div style="font-size: 11px; color: #a3a3a3; display: flex; flex-direction: column; gap: 4px; border-top: 1px solid #333333; padding-top: 8px;">
                <div style="display: flex; justify-content: space-between;">
                  <span>Lat:</span> <span style="color: #ffffff; font-family: monospace;">${selectedLocation.lat.toFixed(6)}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                  <span>Lng:</span> <span style="color: #ffffff; font-family: monospace;">${selectedLocation.lng.toFixed(6)}</span>
                </div>
              </div>
            </div>
        `, { autoClose: false, closeOnClick: false, className: 'custom-popup' })
        .openPopup();

      // Add circle overlay for radius visualization if radius > 0
      if (radiusMeters > 0) {
        try {
          circleRef.current = L.circle([selectedLocation.lat, selectedLocation.lng], {
            color: 'blue',
            fillColor: 'blue',
            fillOpacity: 0.1,
            radius: radiusMeters,
            weight: 2,
            dashArray: '5, 5'
          }).addTo(mapInstanceRef.current);
        } catch (error) {
          console.error('Error adding circle overlay:', error);
        }
      }
    }
  }, [selectedLocation, buildingWidth]);

  // Handle Competitors Rendering
  useEffect(() => {
    if (mapInstanceRef.current && competitors) {
      // Clear existing competitor markers (identify them by a custom property or keep track in a ref)
      // For simplicity, we can remove all markers that are NOT the selected location or user location
      // But better: keep a ref of competitor layers
      
      // Remove previous competitor markers
      if (window.competitorLayers && Array.isArray(window.competitorLayers)) {
         window.competitorLayers.forEach(layer => mapInstanceRef.current.removeLayer(layer));
      }
      window.competitorLayers = [];

      competitors.forEach(comp => {
        let icon = redMarkerIcon;
        if (comp.rating >= 4.5) icon = blueMarkerIcon; // Premium
        else if (comp.rating >= 4.0) icon = greenMarkerIcon; // Strong
        else if (comp.rating >= 3.0) icon = goldMarkerIcon; // Moderate
        // else Red (< 3.0)

        const marker = L.marker([comp.lat, comp.lng], { icon })
          .addTo(mapInstanceRef.current)
          .bindPopup(`
            <div style="background-color: #000000; color: #ffffff; padding: 12px; border-radius: 6px; border: 1px solid #333333; min-width: 220px; font-family: 'Inter', sans-serif;">
              <h3 style="margin: 0 0 8px 0; font-size: 14px; font-weight: 600; color: #ffffff; line-height: 1.4; padding-right: 24px;">${comp.name}</h3>
              <div style="display: flex; gap: 12px; margin-bottom: 6px;">
                <div style="font-size: 12px; color: #e5e5e5; display: flex; align-items: center; gap: 4px;">
                  <span style="color: #f59e0b;">Rating</span> 
                  <span>${comp.rating > 0 ? comp.rating : 'N/A'}</span>
                  <span style="color: #737373; font-size: 10px;">(${comp.user_ratings_total})</span>
                </div>
                <div style="font-size: 12px; color: #a3a3a3;">
                  ${'$'.repeat(comp.price_level || 1)}
                </div>
              </div>
              <div style="font-size: 11px; color: #a3a3a3; margin-top: 8px; border-top: 1px solid #333333; padding-top: 8px; line-height: 1.4;">
                ${comp.vicinity || 'Address not available'}
              </div>
            </div>
          `, { className: 'custom-popup' });
        
        window.competitorLayers.push(marker);
      });
    }
  }, [competitors]);

  return (
    <div className="w-full h-full relative min-h-[400px]">
      <div
        id="business-map"
        ref={mapRef}
        className="absolute inset-0 w-full h-full z-0"
        style={{
          minHeight: '400px',
          backgroundColor: '#e5e5e5', // Light gray background to prevent black screen
          width: '100%',
          height: '100%',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          margin: 0,
          padding: 0,
          border: 'none',
          position: 'absolute',
        }}
      />
      {/* Simple Instructions */}
      {!selectedLocation && (
        <div className="absolute top-4 left-4 z-40 pointer-events-none">
          <div className="bg-black/90 backdrop-blur-sm text-white px-4 py-2.5 rounded-xl text-sm border border-neutral-800 shadow-xl flex items-center gap-2">
            <MapPin className="w-4 h-4 text-yellow-400" />
            <span className="font-medium">Click map to select location</span>
          </div>
        </div>
      )}
      {/* Location Status */}
      <div className="absolute top-4 right-4 z-40 pointer-events-none">
        <div className="bg-black/90 backdrop-blur-sm text-white px-4 py-2.5 rounded-xl text-sm border border-neutral-800 shadow-xl flex items-center gap-2">
          <MapPin className="w-4 h-4 text-yellow-400" />
          <span className="font-medium">Map centered on your location</span>
        </div>
      </div>
      {/* Loading overlay */}
      {!mapLoaded && (
        <div className="absolute inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-10">
          <div className="text-center text-white">
            <Skeleton className="h-8 w-8 rounded-full mx-auto mb-3" />
            <Skeleton className="h-4 w-24 mx-auto" />
          </div>
        </div>
      )}
    </div>
  );
};

export default MapComponent;
