from django.urls import path
from .views import SiteSettingListCreateAPIView, SiteSettingDetailAPIView

urlpatterns = [
    path("site-settings/", SiteSettingListCreateAPIView.as_view(), name="site-settings-list-create"),
    path("site-settings/<int:pk>/", SiteSettingDetailAPIView.as_view(), name="site-settings-detail"),
]
