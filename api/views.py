import firebase_admin
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

from firebase_admin import auth,credentials
from django.conf import settings
import os
firebase_creds = credentials.Certificate(settings.FIREBASE_CONFIG)
firebase_app = firebase_admin.initialize_app(firebase_creds)
@api_view(['POST'])
def upload_files(request):
    try:
        # auherization_header = request.META.get('HTTP_AUTHERIZATION')
        # token = auherization_header.replace("Bearer ","")
        # decoded_token = auth.verify_id_token(token)
        # print(decoded_token)
        data = request.data
        print(f'dddd {data}')
        print('jjhkjh')
        serializer = FileListSterializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 200,
                'message': 'files uploaded successfully',
            })

        return Response({
            'status': 400,
            'message': 'something went wrong',
            'data': serializer.errors
        })
    except Exception as e:
        print(e)

    return Response({'no': 'nope'})


@api_view(['GET'])
def get_all_files(request, pk):
    try:
        # auherization_header = request.META.get('HTTP_AUTHORIZATION')
        # print(auherization_header)
        # # token = auherization_header.replace("Bearer ", "")
        # # print(token)
        #
        # decoded_token = auth.verify_id_token(auherization_header)
        # print(decoded_token)
        print(pk)
        folder_path = f'./media/{pk}'

        url = f'http://127.0.0.1:8000/media/{pk}/'
        urls = []
        try:
            for filename in os.listdir(folder_path):
                print(filename)
                urls.append(url + filename)
        except:
            print('jj')
            os.mkdir(f'media/{pk}')
            print('kk')

        return Response({'goood': urls})
    except Exception as e:
        print(e)
        return Response({'no': 'nope'})


@api_view(['GET'])
def get_space_used(request, pk):
    folderPath = f'media/{pk}'
    size = 0
    for ele in os.scandir(folderPath):
        size += os.path.getsize(ele)
    size = size/1000000 #size in mb
    return Response({'size':size})

@api_view(['GET'])
def get_user_data(request, pk):
    user_details = User.objects.filter(email=pk)
    if len(user_details) ==0:
        return Response({'error':'User Not Found'})
    else:

        print(f'user details {user_details}')
        serialized_data = UserSterializer(user_details[0])
        print(f'data details {serialized_data.data}')
        return Response({"user":serialized_data.data})




@api_view(['POST'])
def create_new_user(request):
    data = request.data
    #data will have email and uid
    user_email = data['email']
    user_details = User.objects.filter(email=user_email)
    if len(user_details) == 0:
        print(f'data from user {data}')
        serializer = UserSterializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"user": serializer.data})
        else:
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
    else:
        return  Response({'error':'User already exist'})





@api_view(['GET'])
def check_server(request):
    return Response({'response':'Server Running'})


# Create your views here.


