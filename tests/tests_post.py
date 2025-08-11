import unittest
import json
from app import db
from app.models import User,Post
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from base import BaseTestCase

class PostTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        user = User(username='testuser', email='test@example.com',
                    password=generate_password_hash('Test@123'))
        db.session.add(user)
        db.session.commit()
        
        post = Post(
            title="Old Title",
            content="Old Title",
            user_id = user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        self.post_id = post.id
        
        login_response = self.client.post(
            "/auth/login/",
            data=json.dumps({
                "email": "test@example.com",
                "password": "Test@123"
            }),
            content_type="application/json"
        )
        self.token = login_response.get_json()["access_token"]

    def test_get_all_posts(self):
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)

    def test_add_post(self):
        headers = {
            'Authorization' : f'Bearer {self.token}'
        }
        response = self.client.post('/post/create/',
                headers = headers,
                data = json.dumps({
                    'title': 'Old Title',
                    'content' : 'Old Title'
                }),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', response.get_json())


    def test_update_post(self):
        headers = {
            'Authorization' : f'Bearer {self.token}'
        }
        update_data = {
            'title': 'New Title',
            'content': 'New Content'
        }
        response = self.client.put(f'/post/update/{self.post_id}',
            data = json.dumps(update_data),
            content_type = 'application/json',
            headers=headers
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Post updated successfully', response.get_json())
        

    def test_delete_post(self):
        headers = {
            'Authorization' : f'Bearer {self.token}'
        }
        response = self.client.delete(f'/post/delete/{self.post_id}',
                headers=headers                   
                )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())
        

if __name__ == '__main__':
    unittest.main()
