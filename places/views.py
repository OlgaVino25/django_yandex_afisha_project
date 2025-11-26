from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, reverse

from places.models import Place


def home(request):
    places = Place.objects.all()

    features = []
    for place in places:
        lng = float(place.lng)
        lat = float(place.lat)

        details_url = reverse("place-detail", kwargs={"place_id": place.id})

        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lng, lat]},
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": details_url,
            },
        }
        features.append(feature)

    geojson = {"type": "FeatureCollection", "features": features}

    return render(request, "map.html", {"geojson": geojson})


def place_json(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related("images"), id=place_id)

    serialized_place = {
        "title": place.title,
        "imgs": [img.image.url for img in place.images.all()],
        "short_description": place.short_description,
        "long_description": place.long_description,
        "coordinates": {"lng": float(place.lng), "lat": float(place.lat)},
    }

    return JsonResponse(
        serialized_place, json_dumps_params={"ensure_ascii": False, "indent": 2}
    )
