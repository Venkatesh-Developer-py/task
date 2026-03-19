from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('staff-products/', views.staff_products, name='staff_products'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('buy-now/<int:id>/', views.buy_now, name='buy_now'),
    path('place-order/<int:id>/', views.place_order, name='place_order'),
    path('products/', views.products, name='products'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('buy-cart/', views.buy_cart, name='buy_cart'),
    path('increase/<int:id>/', views.increase_qty, name='increase'),
    path('decrease/<int:id>/', views.decrease_qty, name='decrease'),
    path('remove/<int:id>/', views.remove_item, name='remove'),
    path('profile/', views.profile, name='profile'),
]
