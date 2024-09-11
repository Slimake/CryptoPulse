import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, storage
import bcrypt
import models

models.storage_type = "db"


from models.base_model import Base
from models.user import User


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)

        # Set up the sessionmaker and bind it to the in-memory engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Override the storage engine for tests
        storage._DBStorage__engine = self.engine
        storage._DBStorage__session = self.session

        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

        # Mock user for tests
        self.mock_user = User(email='test@example.com', username='testuser', password_hash=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))
        storage.add_user(self.mock_user)

    def tearDown(self):
        # Clean up mock user after each test
        storage.delete_user(self.mock_user)

        # Drop all tables at the end of the test
        Base.metadata.drop_all(self.engine)
        self.session.close()

    def test_index_redirect(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    def test_login_get(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())

    def test_login_post_success(self):
        response = self.app.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser!', response.data)

    def test_login_post_failure(self):
        response = self.app.post('/login', data={'username': 'wronguser', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password!', response.data)

    def test_signup_get(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'signup', response.data.lower())

    def test_signup_post_success(self):
        response = self.app.post('/signup', data={
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully signed up! Please log in.', response.data)

    def test_signup_post_failure(self):
        response = self.app.post('/signup', data={
            'email': 'anotheruser@example.com',
            'username': 'testuser',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already taken!', response.data)

if __name__ == '__main__':
    unittest.main()