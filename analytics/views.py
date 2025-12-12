from django.http import JsonResponse
from application import models
from application.models import Application


def placement_stats(request):
    data = Application.objects.values("status").annotate(count=models.Count("id"))
    return JsonResponse(list(data), safe=False)
