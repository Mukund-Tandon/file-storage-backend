from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


@api_view(['POST'])
def upload_files(request):
    try:
        data = request.data

        serializer = FileListSterializer(data=data)
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
    print(pk)
    folder_path = f'./media/{pk}'

    url = f'http://127.0.0.1:8000/media/{pk}/'
    urls = []
    for filename in os.listdir(folder_path):
        print(filename)
        urls.append(url + filename)

    return Response({'goood': urls})
# Create your views here.


