from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from appusers.models import User
from appusers.serializers import UserSerializer

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.mail import send_mail
from django.conf import settings
import requests
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

# Create your views here.

#@csrf_exempt
@api_view(['GET'])
def user_list(request):
    # TODO: if no token, omit email and lastname
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                #TODO: email not working
                "User activation",
                "Use this link to activate: http://127.0.0.1:8000/activate/%s/%s" % (str(serializer.data['id']), str(serializer.data['activation_token'])),
                "admin@so.com",
                [str(serializer.data['email'])],
                fail_silently=True,
            )
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

#@csrf_exempt
@api_view(['GET','PATCH','DELETE'])
def user_detail(request, pk, t=None):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PATCH':
        if not user.activation_token == t:
            return HttpResponse("Invalid token", status=403)
        data = {}
        data["email"] = user.email
        data["password"] = user.password
        data["active"] = 1

        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse("User removed", status=204)

@api_view(['POST'])
def access_token(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    if request.method == 'POST':
        # TODO: validate email and password
        required_params = ['email', 'password']
        params = JSONParser().parse(request)
        param_complete =  all(item in params for item in required_params)
        if not param_complete:
            return HttpResponse("Incomplete data", status=400)

        app = settings.APPUSER_APP
        client = settings.APPUSER_CLIENT
        auth_url = settings.AUTHSERVER
        payload = {'username': app['USERNAME'], 'password': app['PASSWORD'], 'grant_type': 'password'}
        r = requests.post(auth_url, auth=(client['ID'], client['SECRET']), data = payload)
        return JsonResponse(r.json(), safe= False)

@api_view(['POST'])
@authentication_classes((OAuth2Authentication,))
@permission_classes((IsAuthenticated,))
def user_password(request, pk):
    required_params = ['old_password', 'new_password']
    params = request.data
    param_complete =  all(item in params for item in required_params)
    if not param_complete:
        return HttpResponse("Incomplete data", status=400)

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    if not user.password == params["old_password"]:
        return HttpResponse("Incorrect password", status=403)

    data = {}
    data["email"] = user.email
    data["password"] = params["new_password"]

    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)
