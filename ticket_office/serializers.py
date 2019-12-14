from ticket_office.models import Room, Movie, Ticket, Showtime, Customer
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'capacity']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'duration']


class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = ['room', 'movie', 'time']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['showtime', 'customer']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['name']
