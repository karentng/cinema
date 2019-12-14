from django.urls import include, path
from rest_framework import routers
from ticket_office import views

router = routers.DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'movies', views.MovieViewSet)
router.register(r'tickets', views.TicketViewSet)
router.register(r'showtime', views.TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]