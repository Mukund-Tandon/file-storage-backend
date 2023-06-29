import decimal

import firebase_admin
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django.shortcuts import render
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import *

from firebase_admin import auth,credentials
from django.conf import settings
import os
import stripe
from .models import StripeSubscriber
from django.views.decorators.csrf import csrf_exempt

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
        user = User.objects.get(email=data['uploaded_by'])
        if serializer.is_valid():
            serializer.save()
            print('file valid')
            upload_file = request.FILES['files']
            print(upload_file.size)
            user.used_space = user.used_space +  decimal.Decimal(upload_file.size/1e9)
            user.save()
            return Response({
                'status': 200,
                'message': 'files uploaded successfully',
            })
        print('file invalid')
        return Response({
            'status': 400,
            'message': 'something went wrong',
            'data': serializer.errors
        })
    except Exception as e:
        print(e)

    return Response({'no': 'nope'})

@api_view(['GET'])
def get_file(request,email,file_name):
    try:
        auherization_header = request.META.get('HTTP_AUTHORIZATION')
        print(auherization_header)
        token = auherization_header.replace("Bearer ", "")
        print(token)

        decoded_token = auth.verify_id_token(token)
        print(decoded_token)
        file_instance = get_object_or_404(File, file__icontains=file_name, uploaded_by=email)

        return FileResponse(file_instance.file, filename=file_name)
    except :
        return Response({
            'status': 400,
            'message': 'file not found',
        })

@api_view(['GET'])
def get_sharable_file(request,email,file_name):
    try:

        file_instance = get_object_or_404(File, file__icontains=file_name, uploaded_by=email)
        if file_instance.sharable:
            return FileResponse(file_instance.file, filename=file_name)
        return Response({
            'status': 400,
            'message': 'file not found',
        })
    except :
        return Response({
            'status': 400,
            'message': 'file not found',
        })
@api_view(['PATCH'])
def update_file_visibility(request,email,file_name,value):
    try:
        # auherization_header = request.META.get('HTTP_AUTHORIZATION')
        # print(auherization_header)
        # token = auherization_header.replace("Bearer ", "")
        # print(token)
        #
        # decoded_token = auth.verify_id_token(token)
        # print(decoded_token)
        file_instance = get_object_or_404(File, file__icontains=file_name, uploaded_by=email)
        file_sharable = True
        if value.lower() == 'false':
            file_sharable = False

        if file_sharable != file_instance.sharable:
            file_instance.sharable = file_sharable
            file_instance.save()

        return Response({
            'status': 200,
            'message': 'file updated successfully',
        })
    except :
        return Response({
            'status': 400,
            'message': 'file not found',
        })
@api_view(['GET'])
def get_all_files(request, pk):

    try:
        # auherization_header = request.META.get('HTTP_AUTHORIZATION')
        # print(auherization_header)
        # token = auherization_header.replace("Bearer ", "")
        # print(token)
        #
        # decoded_token = auth.verify_id_token(token)
        # print(decoded_token)
        # print(pk)
        folder_path = f'./media/{pk}'
        ip = '192.168.135.33'
        url = f'http://{ip}:8000/get_file/{pk}/'
        sharable_url_base = f'http://{ip}:8000/get_sharable_file/{pk}/'
        #django code to return all rows in file table fro a partucular table
        rows = File.objects.filter(uploaded_by=pk).order_by('-created_at')
        print(rows)
        files = []
        # for row in rows:
        #     fileName = os.path.basename(row.file.name)
        #     fileUrl = url + fileName
        #     fileCreationTime = row.created_at
        #     files.append({'name':fileName,'url':fileUrl,'created_at':fileCreationTime})
        try:
            for row in rows:
                fileName = os.path.basename(row.file.name)
                fileType = 'notImage'
                if fileName.endswith('.jpg') or fileName.endswith('.png') or fileName.endswith('.jpeg') or fileName.endswith('.gif'):
                    fileType = 'image'
                fileUrl = url + fileName
                sharable_url = sharable_url_base + fileName
                fileCreationTime = row.created_at
                files.append({'name': fileName, 'url': fileUrl,'fileType':fileType ,'created_at': fileCreationTime,'sharable_url':sharable_url,'sharable':row.sharable})
        except:
            print('jj')
            os.mkdir(f'media/{pk}')
            print('kk')

        return Response({'good': files})
    except Exception as e:
        print('Error in  get_all_files')
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

@api_view(['GET'])
def stripe_config(request):
    stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
    return Response(stripe_config)

@api_view(['GET'])
def create_checkout_session(request,user_id):
    print('create checkout session')
    ip = '192.168.245.33'
    print(user_id)
    domain_url = f'http://{ip}:8000/'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    print(request.user.id)
    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=user_id,
            success_url=domain_url + 'success',
            cancel_url=domain_url + f'stripe_home/{user_id}',
            payment_method_types=['card'],
            mode='subscription',
            line_items=[
                {
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': 1,
                }
            ]
        )

        return Response({'sessionId': checkout_session['id']})
    except Exception as e:
        return Response({'error': str(e)})

@api_view(['GET'])
def home(request,user_id):
    context={'user_id':user_id}
    return render(request, 'api/home.html',context)

@api_view(['GET'])
def success(request):
    return render(request, 'api/success.html')


@api_view(['GET'])
def cancel(request):
    return render(request, 'api/cancel.html')

@api_view(['GET'])
def subcribtion_details(request,user_id):
    user = User.objects.get(uid=user_id);
    if not user.premium:
        print('user not premium')
        return Response({
            'subcribtion_status':False
        })
    else:
        subcriber = StripeSubscriber.objects.get(user=user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subcribtion_details = stripe.Subscription.retrieve(subcriber.stripeSubscriptionId)
        print(subcribtion_details)
        if subcribtion_details['status'] == 'active':
            return Response({
                'subcribtion_status':True,
                'subcribtion_details':{
                    'cancelled':subcriber.cancelled,
                    'end_time':subcribtion_details['current_period_end']
                }
            })
        else:
            subcriber.cancelled = True
            subcriber.save()
            user.premium = False
            user.save()
            return Response({
                'subcribtion_status': False
            })



@api_view(['POST'])
def cancel_subcribtion(request,user_id):
    user = User.objects.get(uid=user_id);
    if not user.premium:
        return Response({
            'subcribtion_status':False
        })
    else:
        try:
            subcribtion_details = StripeSubscriber.objects.get(user=user)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.Subscription.delete(subcribtion_details.stripeSubscriptionId)
            subcribtion_details.cancelled = True
            subcribtion_details.save()
            return Response({
                'subcribtion_status':True,
                'subcribtion_details':{
                    'cancelled':subcribtion_details.cancelled,
                    'end_time':subcribtion_details.end_time
                }
            })
        except Exception as e:
            return Response({
                'error':str(e)
            })

@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        print('ggfd')
    except ValueError as e:
        # Invalid payload
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return Response(status=400)

    # Handle the checkout.session.completed event

    if event['type'] == 'checkout.session.completed':

        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')

        stripe_customer_id = session.get('customer')

        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        subscription = stripe.Subscription.retrieve(stripe_subscription_id)
        print('Subbibtion details')
        print(subscription)
        user = User.objects.get(uid=client_reference_id)
        print(user)
        user.premium = True
        user.save()
        user = User.objects.get(uid=client_reference_id)
        print(user)
        #TODO: add user from table to stripecostemer table
        start_date = subscription['current_period_start']
        end_date = subscription['current_period_end']
        try:
            subcriber = StripeSubscriber.objects.get(user=user)
            print(subcriber)
            print('subcriber exists')
            subcriber.stripeCustomerId = stripe_customer_id
            subcriber.stripeSubscriptionId = stripe_subscription_id
            subcriber.start_time = start_date
            subcriber.end_time = end_date
            subcriber.cancelled = False
            subcriber.save()
        except ObjectDoesNotExist:
            print('subcriber not exists')
            stripe_costomer = StripeSubscriber(
                user=user,
                stripeCustomerId=stripe_customer_id,
                stripeSubscriptionId=stripe_subscription_id,
                start_time=start_date,
                end_time=end_date,
            )
            stripe_costomer.save()


        # stripe_costomer = StripeSubscriber.objects.update_or_create(
        #     user=user,
        #     stripeCustomerId=stripe_customer_id,
        #     stripeSubscriptionId=stripe_subscription_id,
        #     start_time=start_date,
        #     end_time=end_date,
        #     cancelled=False
        # )
        # stripe_costomer.save()
        print(' just subscribed.')

    return Response(status=200)
# Create your views here.


