from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from appusers.models import User
from appusers.serializers import UserSerializer

from rest_framework.decorators import api_view

# Create your views here.

#@csrf_exempt
@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponseBadRequest("Not allowed")

@csrf_exempt
@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return HttpResponseBadRequest("Not allowed")

#@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def user_detail(request, pk):          # TODO: change responses, add messages
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = {}
        data["email"] = user.email
        data["password"] = user.password

        params = JSONParser().parse(request)
        if "password" in params:
            data["password"] = params["password"]

        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)

    else:
        return HttpResponseBadRequest("Not allowed")
