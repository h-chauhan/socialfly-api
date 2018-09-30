from django.shortcuts import render
from .serializers import SeatSerializer
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.parsers import JSONParser
from .models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def get_seats(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        interests = data.get('interests')
        number_of_seats = data.get('number_of_seats')
        seats = InterestGroup.get_seats(interests, number_of_seats)
        serializer = SeatSerializer(seats, many=True)
        return JsonResponse(serializer.data, safe=False)

