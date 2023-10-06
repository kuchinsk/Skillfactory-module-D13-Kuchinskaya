from django.urls import path, include
from .views import Board, PostView, PostCreate, PostUpdate
from django.conf import settings
from django.conf.urls.static import static
app_name = 'board'
urlpatterns = [
    path('', Board.as_view(), name='board'),
    path('<int:pk>/', PostView.as_view(), name='post'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('update/<int:pk>/', PostUpdate.as_view(), name='post_update'),
    path('profile/', include('profile.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
