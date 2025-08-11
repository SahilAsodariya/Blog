import unittest
import json
from app import db
from app.models import User
from werkzeug.security import generate_password_hash
from base import BaseTestCase

class AuthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        user = User(username='testuser', email='test@example.com',
                    password=generate_password_hash('Test@123'))
        db.session.add(user)
        db.session.commit()


    def test_login_success(self):
        response = self.client.post('/auth/login/',
            data=json.dumps({
                'email': 'test@example.com',  # ✅ Use email here
                'password': 'Test@123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertIn('access_token', data)


    def test_register_success(self):
        response = self.client.post('/auth/register/',
            data=json.dumps({
                'name': 'newuser',
                'email': 'new6@gmail.com',
                'password': 'Newpass@123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())
        
if __name__ == '__main__':
    unittest.main()
