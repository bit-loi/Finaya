from typing import List, Dict, Any
from secrets import choice, randbelow
import httpx
from app.core.config import settings

class PlacesService:
    BASE_URL = "https://maps.googleapis.com/maps/api/place"

    async def search_nearby(
        self, 
        lat: float, 
        lng: float, 
        radius: int = 1000, 
        keyword: str = "food",
        place_type: str = None
    ) -> List[Dict[str, Any]]:
        """
        Search for nearby places using Google Places API
        """
        if not settings.GOOGLE_MAPS_API_KEY:
            # Return dummy data if no key is present for dev/demo purposes 
            # or raise error if strict. Let's return dummy for hackathon safety.
            return self._get_dummy_competitors(lat, lng)

        async with httpx.AsyncClient() as client:
            params = {
                "location": f"{lat},{lng}",
                "radius": radius,
                "key": settings.GOOGLE_MAPS_API_KEY
            }
            if keyword:
                params["keyword"] = keyword
            if place_type:
                params["type"] = place_type

            try:
                response = await client.get(f"{self.BASE_URL}/nearbysearch/json", params=params)
                data = response.json()
                
                if data.get("status") not in ["OK", "ZERO_RESULTS"]:
                    print(f"Places API Error: {data.get('status')} - {data.get('error_message')}")
                    # Fallback to dummy if API fails (e.g. quota, invalid key)
                    return self._get_dummy_competitors(lat, lng)
                
                results = data.get("results", [])
                return self._format_places(results)

            except Exception as e:
                print(f"Places Service Exception: {e}")
                return self._get_dummy_competitors(lat, lng)

    def _format_places(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        formatted = []
        for place in results:
            formatted.append({
                "id": place.get("place_id"),
                "name": place.get("name"),
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"],
                "rating": place.get("rating", 0),
                "user_ratings_total": place.get("user_ratings_total", 0),
                "vicinity": place.get("vicinity"),
                "price_level": place.get("price_level", 1), # 0-4
                "types": place.get("types", [])
            })
        return formatted

    def _get_dummy_competitors(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        """
        Generates realistic dummy competitors around the location for demo/fallback.
        """
        competitors = []
        types = ["Cafe", "Restaurant", "Retail", "Coffee Shop"]
        names = ["Kopi Kenangan", "Janji Jiwa", "Starbucks", "Indomaret", "Alfamart", "Local Warung", "Fancy Bistro"]
        
        for i in range(5):
            # Demo-only jitter using OS-backed randomness.
            lat_offset = ((randbelow(10001) / 10000) - 0.5) * 0.005
            lng_offset = ((randbelow(10001) / 10000) - 0.5) * 0.005
            
            competitors.append({
                "id": f"dummy_{i}",
                "name": f"{choice(names)} {randbelow(100) + 1}",
                "lat": lat + lat_offset,
                "lng": lng + lng_offset,
                "rating": round(3.0 + (randbelow(21) / 10), 1),
                "user_ratings_total": randbelow(491) + 10,
                "vicinity": "Nearby St.",
                "price_level": randbelow(4) + 1,
                "types": [choice(types).lower()]
            })
        return competitors

places_service = PlacesService()
