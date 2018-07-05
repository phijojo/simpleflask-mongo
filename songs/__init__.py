from flask import Flask, jsonify,request
from flask_pymongo import PyMongo
from songs.utils import get_instance_folder_path
from songs.config import configure_app
from bson import json_util, ObjectId
from pymongo import ReturnDocument,IndexModel, ASCENDING, DESCENDING, TEXT
import json

app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True)
# app.debug = True
# app.secret_key = 'development key'
# app.config['MONGO_DBNAME'] = 'devdb'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/devdb'
configure_app(app)

#print(app.config)
mongo = PyMongo(app)

class InvalidObjectId(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def create_index():
    songs = mongo.db.songs
    try:
        songs.create_index([('artist', TEXT),('title', TEXT)], default_language='english')
    except:
        print('index already exists')
        pass
    return 0

@app.errorhandler(InvalidObjectId)
def handle_invalid_object_id(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/songs',defaults={'page':1}, methods=['GET'])
@app.route('/songs/page/<int:page>', methods=['GET'])
def get_all_songs(page):
    songs = mongo.db.songs
    output = []
    n = (page * 3) - 3
    for q in songs.find().skip(n).limit(3):
        #output.append({'artist': q['artist'],'title': q['title'],'difficulty': q['difficulty'],'level':q['level'],'released': q['released']})
        id = str(q.pop('_id'))
        q['_id'] = id
        output.append(q)
    #jsonify(output)
    return jsonify({'result' : output}), 200


@app.route('/songs/avg/difficulty/<int:level_id>', methods=['GET'])
def get_all_songs_with_level_of_difficulty(level_id):
    songs = mongo.db.songs
    sum = 0.0
    len = 0.0
    for q in songs.find({'level': level_id}):
        #print(q['difficulty'])
        sum = sum + q['difficulty']
        len = len + 1.0
    try:
        avg = round((sum/len),2)
    except ZeroDivisionError:
    #    jsonify({'Error' : 'Unknown difficult level'})
        return jsonify({'Error' : 'Unknown difficult level'})
    #jsonify({'average' : avg})
    return jsonify({'average' : avg})
@app.route('/songs/rating', methods=['POST'])
def add_ratings():
    songs = mongo.db.songs
    content = request.json
    sid = request.json['song_id']
    rating = request.json['rating']
    song_objectid = ObjectId(sid)
    if 1 <= rating <=5:
        update_rating=songs.find_one_and_update({'_id': song_objectid}, {'$push': {'rating': rating }},return_document=ReturnDocument.AFTER)
        if update_rating is None:
            raise InvalidObjectId('Invalid SongId', status_code=410)
        print(update_rating)
        update_rating['_id'] = str(update_rating['_id'])
        status = 'Rating updated successfully'
        return jsonify(update_rating,{'status':status})
    else:
        return jsonify({'status': "Error, Rating should be between 1 and 5"})

@app.route('/songs/avg/rating/<song_id>', methods=['GET'])
def get_avg_ratings(song_id):
    print(song_id)
    sid=ObjectId(song_id)
    songs = mongo.db.songs
    ratings=songs.find_one({'_id': ObjectId(song_id)})['rating']
    low_rating=sorted(ratings)[0]
    high_rating=sorted(ratings,reverse=True)[0]
    avg_rating=(sum(ratings)/len(ratings))
    return jsonify({'ratings':{ 'high' : high_rating, 'low': low_rating, 'avg': avg_rating}})

@app.route('/songs/search/<keyword>', methods=['GET'])
def search_songs_with_keywords(keyword):
    create_index()
    songs = mongo.db.songs
    result = songs.find( { '$text': { '$search': keyword } } )
    output = []
    for r in result:
        r['_id'] = str(r['_id'])
        output.append(r)
    return jsonify({'results': output})
