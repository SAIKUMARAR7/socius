from django.urls import path
from Coupons import views



urlpatterns = [
    
    path('coupons/', views.Coupon_SU_table, name="SUCoupon_table"),
    path('superuser_couponcode/', views.create_SU_coupon_, name='SuCoupon'),
    path('<id>/SUCoupon_update', views.SuCoupon_update, name='SuCoupon_update' ),

]