# Cinema Project
### Requirements and Installation:

Inside the project's folder install all the requirements with:

        pip install -r requirements.txt

### Running the project
There is one app in the project named ticket_office. All the logic and implementation was done there.
Once all requirements are successfully installed, run the project like this:

        python manage.py runserver
        
## Models
- ticket_office application has four models: Room, Movie, Showtime, Ticket


        [Room]
        listing / creating = http://localhost:8000/rooms
        editing / delete = http://localhost:8000/rooms/<int:id>
        
        [Movie]
        listing / creating = http://localhost:8000/movies
        editing / delete = http://localhost:8000/movies/<int:id>
        
        [Showtime]
        listing / creating = http://localhost:8000/showtimes
        editing / delete = http://localhost:8000/showtimes/<int:id>
        
        [Ticket]
        listing / creating = http://localhost:8000/tickets
        editing / delete = http://localhost:8000/tickets/<int:id>
    
    After running the server you can access in the browser or through curl command
    those urls.

## Movies playing in the theatre
The list of movies currently playing in the theatre could be access:

        http://localhost:8000/movies_playing
        
You can set a timeframe to filter results by the showtime's start_date like this:

        http://localhost:8000/movies_playing?start=2019-12-14&end=2019-12-20

You can use either one of those filter parameters or both.
     
        
## Rooms playing in the theatre
The list of movies currently playing in the theatre could be access:

        http://localhost:8000/rooms_playing
        
It is available the same feature to filter results in this list by start and end datetime. 

## Examples to access the API through cURL command
        
        creating a room:
        curl -X POST http://localhost:8000/rooms/ -d name="test" -d capacity=50
        creating a movie:
        curl -X POST http://localhost:8000/movies/ -d title="movie title name" -d duration=160
        listing showtimes:
        curl -X GET http://localhost:8000/showtimes/
        selling a tikcet:
        curl -X POST http://localhost:8000/tickets/ -d showtime=1 -d num_seats=1
        
## Unit Testing
In the file test.py inside ticket_office app you can see all testing implementation for crud in the 4 main models.
Command to run the testing:
    
    python manage.py test




