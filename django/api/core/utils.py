from django.conf import settings

from geopy.geocoders import GoogleV3


def get_coordinates(address: str) -> dict:
    """
    Returns a dictionary containing `lat` and `long`
    """

    geolocation = GoogleV3(api_key=settings.GEO_API)
    coordinates = geolocation.geocode(address, exactly_one=True)
    return {
        "lat": coordinates.latitude,
        "lon": coordinates.longitude
    }
