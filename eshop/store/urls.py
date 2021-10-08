from django.urls import path

from .views import index, Cart, CheckOut, Signup, Login, empty, logout, Base, emptycart, success, Order
from.middleware.auth import auth_middleware
urlpatterns = [
	path('', index),
	path('home', index,name='home'),
	path('products', Base.as_view(), name='products'),
	path('signup', Signup.as_view(), name="signup"),
    path('login', Login.as_view(), name="login"),
	path('logout', logout,name='logout'),
	path('cart/', auth_middleware(Cart.as_view()), name="cart"),
	path('checkout/', CheckOut.as_view(), name="checkout"),
    path('empty', empty, name='empty'),
    path('ecart', emptycart, name='ecart'),
	path('success', success, name='success'),
	path('order', auth_middleware(Order.as_view()), name='order')
]