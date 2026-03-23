import requests
import unittest
from app import create_app, db
from models import User, Customer, Transaction

class KhatabookTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB for testing
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_full_flow(self):
        # 1. Register
        response = self.client.post('/', data=dict(
            signup='true',
            username='testuser',
            password='password123',
            business_name='Test Biz'
        ), follow_redirects=True)
        self.assertIn(b'Test Biz', response.data)
        
        # 2. Add Customer
        response = self.client.post('/add_customer', data=dict(
            name='Raju',
            phone='1234567890'
        ), follow_redirects=True)
        self.assertIn(b'Raju', response.data)
        self.assertIn(b'1234567890', response.data)

        # Get Customer ID (implied, assuming it will be 1)
        # 3. Add Transaction (YOU GAVE 500)
        response = self.client.post('/customer/1/add_tx', data=dict(
            amount='500',
            type='GAVE',
            description='Rice Bag'
        ), follow_redirects=True)
        # Check if balance updated (Logic: GAVE -> Positive Balance for us)
        self.assertIn(b'500', response.data)
        self.assertIn(b'You Gave', response.data)
        
        # 4. Add Transaction (YOU GOT 200)
        response = self.client.post('/customer/1/add_tx', data=dict(
            amount='200',
            type='GOT',
            description='Part Payment'
        ), follow_redirects=True)
        
        # 5. Check Dashboard Total
        response = self.client.get('/dashboard')
        # Total should be 500 - 200 = 300 (You will get)
        if b'300' not in response.data:
            print(f"FAILED: Response data: {response.data}")
        self.assertIn(b'300', response.data)

if __name__ == '__main__':
    unittest.main()
