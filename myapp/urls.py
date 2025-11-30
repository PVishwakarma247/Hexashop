from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('product_details/<str:category>/<int:product_id>/', views.product_details, name='product_details')
]