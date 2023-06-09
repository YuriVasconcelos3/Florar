from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import enviar_email

urlpatterns = [
    path('index/', views.home, name='home'),
    path('blog/', views.PostList.as_view(), name='blog'),
    path('enviar_email/', enviar_email, name='enviar_email'),
    path('membros/', views.PostList2.as_view(), name="membros"),
    path('<slug:slug>/', views.DetailView.as_view(), name='post_detail'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)