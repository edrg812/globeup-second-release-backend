from django.urls import path
from . import views
from .views import update_reseller_supplier_request, create_reseller_supplier_request



urlpatterns = [
    path('user-profile/', views.UserProfileViewSet.as_view(), name='user-profile-list'),
    path("reseller-supplier-request/", create_reseller_supplier_request, name="reseller-request-create"),
    path("reseller-supplier-request/<int:pk>/", update_reseller_supplier_request, name="reseller-request-update"),
    path("user/requested", views.RequestedUsersListView.as_view(), name="requested-users-list"),
    path("all-users-list/", views.AllUsersListView.as_view(), name="all-users-list")
]
