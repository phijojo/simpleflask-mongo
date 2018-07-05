import unittest
from songs import app
import json
import random

class SongsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_get_all_songs(self):
        result = self.app.get('/songs/page/1', follow_redirects=True)
        json_data = json.loads(result.get_data(as_text=True))
        #print(json_data)
        assert 'result' in json_data
        assert '_id' in json_data['result'][0]
        assert 'artist' in json_data['result'][0]
        assert 'difficulty' in json_data['result'][0]
        assert 'level' in json_data['result'][0]
        assert 'released' in json_data['result'][0]
        assert 'title' in json_data['result'][0]

    def test_get_all_songs_paginate(self):
        result = self.app.get('/songs/page/2')
        json_data = json.loads(result.get_data(as_text=True))
        assert 'result' in json_data
        assert '_id' in json_data['result'][0]
        assert 'artist' in json_data['result'][0]
        assert 'difficulty' in json_data['result'][0]
        assert 'level' in json_data['result'][0]
        assert 'released' in json_data['result'][0]
        assert 'title' in json_data['result'][0]

    def test_get_all_songs_with_level_of_difficulty(self):
        #diff_level=random.randint(1,100)
        diff_level = random.randint(6,7)
        #diff_level = 6
        if diff_level == 6 :
            baseurl = '/songs/avg/difficulty/'
            url = ''.join([baseurl, str(diff_level)])
            result = self.app.get(url)
            #print(result.get_data())
            json_data = json.loads(result.get_data())
            assert 'average' in json_data
        else:
            baseurl = '/songs/avg/difficulty/'
            url = ''.join([baseurl, str(diff_level)])
            result = self.app.get(url)
            json_data = json.loads(result.get_data())
            assert 'Error' in json_data


    def test_search_songs_with_keywords(self):
        keywords=['yousicians', 'kennel']
        secure_random = random.SystemRandom()
        search_key=secure_random.choice(keywords)
        baseurl='/songs/search/'
        url = ''.join([baseurl, str(search_key)])
        #print(url)
        result = self.app.get(url)
        json_data = json.loads(result.get_data(as_text=True))
        assert 'results' in json_data
        assert '_id' in json_data['results'][0]
        assert 'artist' in json_data['results'][0]
        assert 'difficulty' in json_data['results'][0]
        assert 'level' in json_data['results'][0]
        assert 'released' in json_data['results'][0]
        assert 'title' in json_data['results'][0]



if __name__ == '__main__':
      unittest.main()
