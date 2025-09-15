from django.urls import path
from . import views

urlpatterns = [
    path("withdraw-request/", views.list_my_withdraw_requests, name="withdraw-request-list"),
    path("withdraw-request/create/", views.create_withdraw_request, name="create-withdraw-request"),
    path("list_all_withdraw_requests_admin/", views.list_all_withdraw_requests_admin),
    path("withdraw-request/<int:pk>/update/", views.update_withdraw_request, name="update_withdraw_request"),

]
