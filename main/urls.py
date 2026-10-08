from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('restaurants/', views.restaurants_list, name='restaurants'),
    path('subscription/', views.subscription_view, name='subscription'),
    path('cart/', views.cart_detail, name='cart'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:dish_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]