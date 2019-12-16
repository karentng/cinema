from django.urls import include, path
from rest_framework import routers
from ticket_office import views

router = routers.DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'movies', views.MovieViewSet)
router.register(r'showtimes', views.ShowtimeViewSet)
router.register(r'tickets', views.TicketView)

urlpatterns = [
    path('', include(router.urls)),
    path('rooms_playing', views.RoomsPlayingView.as_view()),
    path('movies_playing', views.MoviesPlayingView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
