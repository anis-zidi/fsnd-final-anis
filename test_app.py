import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import app
from models import setup_db, Movies, Actors, database_path
from flask import request, _request_ctx_stack, abort


Access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRsUG0zaG1UNm1odGhOOHEtU0dwUSJ9.eyJpc3MiOiJodHRwczovL3Rlc3Qtbm8tMS5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDQxNTYyNzExODkyNTU5MjA3MzMiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTYxNzI4OTU3NywiZXhwIjoxNjE3Mzc1OTc3LCJhenAiOiIzUjd3bTZWWFdaQ1lDWTBXOXdRN3Jmd1Y0ZGZRWDRydSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.KM6Yxdau-lkigawskgarKgO5HBaEg0QMHUu8DGkcATXRqGEohWuNpfbxTWfsnr0Jqxg2Pv4ly9kYzU3A-TN8vahqQhd9bICI9jROY_HBsZnk-yUMjSanUt7TBHYeVy_Ghf5aNYSvQBqE1HGFUKaw9cEXp6puqp4jLgB_YXJTtQwbVfpEE8Ioe2Wv20mTUcBJHVKNkO6JRi-brLwiLMGrCNxPNi-sYE9Znpe8prWfBokDgqF-GDq5NbGuLWFNRAzFyT4M6xakY2XclMVfpDL6CkvlaIWGznFUCd5KKNXR8BFT7LtxSM5cfI3LQKYJxySkh9mg8vG7pt-589hFAK5GPQ'

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = database_path
        self.exec_prod = Access_token
        self.app.config['TESTING'] = True

        self.new_movie = {
            "title": "Titanic",
            "release_date": "1997",
        }
        self.update_movie = {
            "title": "This movie is updated"
        }
        self.new_actor = {
            "name":"Anis",
            "age": "26",
            "gender":"male"
        }
        self.update_actor = {
            "name":"Name-Updated"
        }
        
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_movies(self):
        res = self.client().get('/Movies',
                                     headers={
                                         'Authorization': 'Bearer ' + self.exec_prod
                                     })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    def test_create_new_movie(self):
        res = self.client().post('/Movies',
                                    headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    },
                                    json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_movie(self):
        create_movie = {
            'title' : 'This is a delete test movie',
            'release_date' : '2000'
                        } 
        res = self.client().post('/Movies',headers={
                                            'Authorization': 'Bearer ' + self.exec_prod
                                                    }, json = create_movie)
        data = json.loads(res.data)
        movie_id= data['movie']['id']
        res = self.client().delete('/Movies/{}'.format(movie_id), headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                                                            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_update_movie(self):
        create_movie = {
            'title': 'This an update test movie',
            'release_date':'1990'
                        }
        res = self.client().post('/Movies', headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    }, json = create_movie)
        data = json.loads(res.data)
        movie_id= data['movie']['id']
        update_movie = self.update_movie
        res = self.client().patch('/Movies/{}'.format(movie_id), headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    }, json = update_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_get_actors(self):
        res = self.client().get('/Actors',
                                    headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_create_new_actor(self):
        res = self.client().post('/Actors',
                                    headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    }, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_delete_actor(self):
        create_actor = {
            'name': 'Test_name',
            'age': '30',
            'gender': 'Male'
        }
        res = self.client().post('/Actors', headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    }, json = create_actor)
        data = json.loads(res.data)
        actor_id= data['actor']['id']
        res = self.client().delete('/Actors/{}'.format(actor_id),  headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_update_actor(self):
        create_actor = {
            'name': 'Name-Non-Updated',
            'age': '30',
            'gender': 'Male'
        }
        res = self.client().post('/Actors', headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    } ,json = create_actor)
        data = json.loads(res.data)
        actor_id= data['actor']['id']
        update_actor = self.update_actor
        res = self.client().patch('/Actors/{}'.format(actor_id), headers={
                                        'Authorization': 'Bearer ' + self.exec_prod
                                    },json = update_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_actors_without_permessions(self):
        res = self.client().get('/Actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    unittest.main()