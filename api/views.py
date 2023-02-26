import firebase_admin
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

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
        ip = '192.168.245.33'
        url = f'http://{ip}:8000/media/{pk}/'
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

@api_view(['GET'])
def stripe_config(request):
    stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
    return Response(stripe_config)

@api_view(['GET'])
def create_checkout_session(request,user_id):
    print('create checkout session')
    print(user_id)
    domain_url = 'http://localhost:8000/'
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

@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print('gg')
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
    print('gg')
    print(event['type'])
    if event['type'] == 'checkout.session.completed':

        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')

        stripe_customer_id = session.get('customer')

        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        subscription = stripe.Subscription.retrieve(stripe_subscription_id)
        print(subscription)
        user = User.objects.get(uid=client_reference_id)
        #TODO: add user from table to stripecostemer table
        start_date = subscription['current_period_start']
        end_date = subscription['current_period_end']
        stripe_costomer = StripeSubscriber(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
            start_date=start_date,
            end_date=end_date
        )
        stripe_costomer.save()
        print(' just subscribed.')

    return Response(status=200)
# Create your views here.


