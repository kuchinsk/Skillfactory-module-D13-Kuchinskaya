from django.urls import path, include
from .views import ProfileView, ResponseView, SignView, LoginView, LogoutView, CodeView, accept, delete
from django.conf import settings
from django.conf.urls.static import static

app_name = 'profile'

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('response/', ResponseView.as_view(), name='response'),
    path('signup/', SignView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('code/', CodeView.as_view(), name='code'),
    path('accept/<int:pk>', accept, name='accept'),
    path('delete/<int:pk>', delete, name='delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)