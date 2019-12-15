from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError

from ticket_office.serializers import *


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all().order_by('start_date')
    serializer_class = ShowtimeSerializer

    def create(self, request, *args, **kwargs):
        """
        Innitialize availability before creating showtime

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        room = Room.objects.get(id=request.data.get('room'))
        request.data['available'] = room.capacity
        return super().create(request, *args, **kwargs)


class TicketView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        """
        Method to sell a ticket. This will discount the number of seats sold from the availability in the showtime

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        num_tickets = int(request.data.get('num_seats'))
        showtime = Showtime.objects.get(id=request.data.get('showtime'))
        available = showtime.available

        if available - num_tickets >= 0:
            showtime.available = available - num_tickets
            showtime.save()
        else:
            raise ValidationError({'num_seats': 'Not enough Availability'})

        return super().create(request, *args, **kwargs)

