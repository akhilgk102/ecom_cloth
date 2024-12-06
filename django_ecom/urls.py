"""
URL configuration for django_ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.SignUpView.as_view(),name="signup"),
    path("signin",views.SignInView.as_view(),name="signin"),
    path("signout",views.SignOutView.as_view(),name="signout"),
    
    path("verify/otp/",views.VerifyEmailView.as_view(),name="verify-email"),
    path("index/",views.ProductListView.as_view(),name="index"),
    path("product/<int:pk>/detail",views.ProductDetailView.as_view(),name="product-detail"),
    path("product/<int:pk>/add/cart",views.AddToCartView.as_view(),name="addtocart"),
    path("cart/summary",views.CartSummaryView.as_view(),name="cart-summary"),
    path("product/<int:pk>/remove",views.CartItemDeleteView.as_view(),name="cart-delete"),

    path("place/order",views.PlaceOrderView.as_view(),name="place_order"),
    path("order/summary/",views.OrderSummaryView.as_view(),name="order-summary"),
    path("order/<int:pk>/delete/",views.OrderDeleteView.as_view(),name="order-delete"),
    
    path("payment/verify/",views.PaymentVerificationView.as_view(),name="payment-verify"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
