from django.urls import path
from .views import (
    EarningListView,
    WithdrawRequestView,
    MarkAsPaidView,
    MarkAsFailedView,
)
from . import views


urlpatterns = [
    #this url is used by admin to get list of payment request users
    path('amin/earnings/', views.EarningAdminListView.as_view(), name='amin-earnings-list'),
    path('admin/earnings/<int:pk>/', views.EarningAdminDetailView.as_view(), name='admin-earnings-detail'),
    path("earnings/", EarningListView.as_view(), name="earning-list"),
    #this is used by reseller to request for withdraw
    path("earnings/withdraw/", WithdrawRequestView.as_view(), name="withdraw-request"),
    #admin use url to change status of payment
    path("earnings/<int:pk>/paid/", MarkAsPaidView.as_view(), name="mark-as-paid"),
    path("earnings/<int:pk>/failed/", MarkAsFailedView.as_view(), name="mark-as-failed"),
    path("status-change/", views.ChangeEarningStatusView.as_view(), name="change-earning-status"),
    #this endpoint needs to be called while ordering 
    path("add-to-upcoming-balance/", views.upcoming_balance_update, name="add-to-upcoming-balance"),
]









