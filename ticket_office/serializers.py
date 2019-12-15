import datetime as dt

from ticket_office.models import Room, Movie, Ticket, Showtime, Customer
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'capacity']
        extra_kwargs = {'name': {'required': True}, 'capacity': {'required': True}}


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'duration']
        extra_kwargs = {'title': {'required': True}, 'duration': {'required': True}}


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name']
        extra_kwargs = {'name': {'required': True}}


class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = ['room', 'movie', 'start_date']
        extra_kwargs = {'room': {'required': True}, 'movie': {'required': True}, 'start_date': {'required': True}}

    def validate(self, data):
        """
        Check there is not other showtime overlapped with the new one

        :rtype dict data: dictionary with the data sent to create new showtime
        :return: dictionary of validated data
        """
        movie = Movie.objects.get(id=data['movie'].id) if data.get('movie') else None
        start = data.get('start_date')
        end = start + dt.timedelta(minutes=movie.duration) if start and movie else None
        overlap_start = Showtime.objects.filter(room=data['room'].id, start_date__gte=start, end_date__gte=end).count()
        overlap_end = Showtime.objects.filter(room=data['room'].id, start_date__lte=start, end_date__lte=end).count()

        if overlap_start > 0 or overlap_end > 0:
            raise serializers.ValidationError("There is a showtime overlapped")

        data['end_date'] = end
        return data

    def to_representation(self, instance):
        """
        Method to get the movie and room name in the list, instad of getting the ids

        :param instance:
        :return:
        """
        rep = super(ShowtimeSerializer, self).to_representation(instance)
        rep['room'] = instance.room.name
        rep['movie'] = instance.movie.title
        return rep


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['showtime', 'customer']
        extra_kwargs = {'showtime': {'required': True}, 'customer': {'required': True}}
