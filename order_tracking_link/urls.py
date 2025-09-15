# from django.urls import path
# from . import views

# urlpatterns = [
#     path("seller/order/tracking/", views.get_cutomer_tracking_link_view),
#     path("seller/order/tracking/post/", views.post_customer_tracking_link_view),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path("customer/<int:order_id>/", views.get_customer_tracking_link_view, name="get_customer_tracking"),
    path("customer/<int:order_id>/post/", views.post_customer_tracking_link_view, name="post_customer_tracking"),
    path("seller/<int:order_id>/", views.get_seller_tracking_link_view, name="get_seller_tracking"),
    path("seller/<int:order_id>/post/", views.post_seller_tracking_link_view, name="post_seller_tracking"),
]

