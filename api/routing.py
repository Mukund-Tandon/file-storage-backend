from django.urls import re_path
from . import consumers

websockets_urlpatterns = [
    # re_path(r'ws/checkout/<user_id>/',consumers.StripeCheckoutConsumer.as_asgi())
    re_path(r'ws/checkout/',consumers.StripeCheckoutConsumer.as_asgi())
]