from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # URLs para login e refresh de token
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # URLs para eventos
    path('generate_qrcode/', views.generate_qrcode, name='generate_qrcode'),
    path('download_pdf/<int:evento_id>/', views.download_pdf, name='download_pdf'),
    path('events/', views.get_events, name='get_events'),
    path('events/<int:evento_id>/', views.get_event_detail, name='get_event_detail'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/edit/<int:evento_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:evento_id>/', views.delete_event, name='delete_event'),
]
