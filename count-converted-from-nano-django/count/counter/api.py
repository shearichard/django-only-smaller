from ninja import NinjaAPI

from .models import CountLog

api = NinjaAPI()


@api.get("/add")
def add(request):
    CountLog.objects.create()
    return {"count": CountLog.objects.count()}
