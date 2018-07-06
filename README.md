# simpleflask-mongo

This is a simple api application using python flask and mongodb

prerequisite
1. docker
2. docker stack



To run this setup
1. Clone the repository
2. cd simpleflask-mongo
3. ./setup.sh


URLs
 GET
 http://0.0.0.0/songs
 http://0.0.0.0/songs/page/2
 http://songs/avg/difficulty/6
 http://0.0.0.0/songs/avg/rating/song_id
 http://0.0.0.0/songs/search/<keyword>
  
 POST:
 http://0.0.0.0/songs/rating
 parameters
{song_id: id, rating:5}
