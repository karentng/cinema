import datetime as dt
from django.utils import timezone

from ticket_office.models import Room, Movie, Ticket, Showtime
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        extra_kwargs = {'name': {'required': True}, 'capacity': {'required': True}}


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        extra_kwargs = {'title': {'required': True}, 'duration': {'required': True}}


class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = ['id', 'room', 'movie', 'start_date']
        extra_kwargs = {'room': {'required': True}, 'movie': {'required': True}, 'start_date': {'required': True}}

    def validate(self, data):
        """
        Check there is not other showtime overlapped with the new one

        :rtype dict data: dictionary with the data sent to create new showtime
        :return: dictionary of validated data
        """
        start = data.get('start_date')
        now = dt.datetime.now()

        if start < timezone.now():
            raise serializers.ValidationError('Start Date must be a future time.')

        movie = Movie.objects.get(id=data['movie'].id)
        room = Room.objects.get(id=data['room'].id)
        end = start + dt.timedelta(minutes=movie.duration)
        overlap_start = Showtime.objects.filter(room=room.id, start_date__gte=start, start_date__lte=end).count()
        overlap_end = Showtime.objects.filter(room=room.id, end_date__gte=start, end_date__lte=end).count()

        if overlap_start > 0 or overlap_end > 0:
            raise serializers.ValidationError("There is a showtime overlapped")

        data['end_date'] = end  # set up the end time to the show
        data['available'] = room.capacity  # initialize availability with the room's size
        return data

    def to_representation(self, instance):
        """
        Method to get the movie and room name in the list, instead of getting the ids

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
        fields = "__all__"
        extra_kwargs = {'showtime': {'required': True}, 'num_seats': {'required': True}}

    def validate_num_seats(self, seats):
        """
        Check if the number of seats is an integer value

        :rtype str seats: number of seats to buy in ticket
        :return: value
        """
        try:
            int(seats)
        except:
            raise serializers.ValidationError('Number of seats must be integer')

        return seats

    def to_representation(self, instance):
        """
        Method to get the showtime information instead of getting the ids

        :param instance:
        :return:
        """
        rep = super(TicketSerializer, self).to_representation(instance)
        rep['showtime'] = f"{instance.showtime.room.name} {instance.showtime.movie.title} " \
                          f"{instance.showtime.start_date}"
        return rep


class RoomSummarySerializer(serializers.ModelSerializer):
    """
    Serialize list of showtimes per room
    """
    showtimes = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = ['name', 'capacity', 'showtimes']


class RoomsPlayingSerializer(serializers.Serializer):
    """
    Serialize list of rooms with showtimes
    """
    rooms = serializers.ListField(child=RoomSummarySerializer())


class MovieSummarySerializer(serializers.ModelSerializer):
    """
    Serialize a list of showtimes per movie
    """
    showtimes = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = ['title', 'duration', 'showtimes']


class MoviesPlayingSerializer(serializers.Serializer):
    """
    Serialize list of movies with showtimes
    """
    movies = serializers.ListField(child=MovieSummarySerializer())

