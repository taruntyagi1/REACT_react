from django.urls import path
from . import views
from product.views import *

urlpatterns = [
    path('add/<int:product_id>/<int:user_id>/',views.add_to_cart,name = "add"),
    path('login/',views.login_view,name = "login"),
    path('login_view/', LoginView.as_view()),
    path('products/',ProductView.as_view())
]
