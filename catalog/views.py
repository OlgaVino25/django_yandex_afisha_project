from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from catalog.models import Place
import json


def home(request):
    places = Place.objects.all()

    features = []
    for place in places:
        lng = float(place.lng)
        lat = float(place.lat)

        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": f"/places/{place.id}/",
            },
        }
        features.append(feature)

    geojson_data = {"type": "FeatureCollection", "features": features}
    geojson_str = json.dumps(geojson_data, ensure_ascii=False)

    return render(request, "map.html", {"geojson_data": geojson_str})


def place_json(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    place_data = {
        "title": place.title,
        "imgs": [img.image.url for img in place.images.all()],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {"lng": float(place.lng), "lat": float(place.lat)},
    }

    return JsonResponse(
        place_data, json_dumps_params={"ensure_ascii": False, "indent": 2}
    )
