import unittest
from flask import Flask
from main import app, storage
import bcrypt

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the app
        self.app = app.test_client()
        self.app.testing = True

        # Set up the database with a mock user
        self.mock_user = User(email='test@example.com', username='testuser', password_hash=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        storage.add_user(self.mock_user)

    def tearDown(self):
        # Clean up the database after each test
        storage.delete_user(self.mock_user)

    def test_index_redirect(self):
        # Test if the index route redirects to login
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    def test_login_get(self):
        # Test the GET request to the login page
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())

    def test_login_post_success(self):
        # Test a successful login
        response = self.app.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser!', response.data)

    def test_login_post_failure(self):
        # Test an unsuccessful login
        response = self.app.post('/login', data={'username': 'wronguser', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password!', response.data)

    def test_signup_get(self):
        # Test the GET request to the signup page
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'signup', response.data.lower())

    def test_signup_post_success(self):
        # Test a successful signup
        response = self.app.post('/signup', data={
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Succefully signed up! Please log in.', response.data)

    def test_signup_post_failure(self):
        # Test a failed signup due to username already taken
        response = self.app.post('/signup', data={
            'email': 'anotheruser@example.com',
            'username': 'testuser',  # This username already exists
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already taken!', response.data)

if __name__ == '__main__':
    unittest.main()