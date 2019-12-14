from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    duration = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Customer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Showtime(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.room.name} {self.movie.title} {self.time}"


class Ticket(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.showtime.movie.title} {self.showtime.room.name} {self.showtime.time} {self.customer.name}"




