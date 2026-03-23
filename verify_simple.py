from app import create_app, db
from models import User, Customer, Transaction

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['WTF_CSRF_ENABLED'] = False
client = app.test_client()

with app.app_context():
    db.create_all()
    
    # 1. Register
    print("Testing Registration...")
    response = client.post('/', data=dict(
        signup='true',
        username='testuser',
        password='password123',
        business_name='Test Biz'
    ), follow_redirects=True)
    
    if b'Test Biz' in response.data:
        print("Registration: SUCCESS")
    else:
        print(f"Registration: FAILED. Response: {response.data}")

    # 2. Add Customer
    print("Testing Add Customer...")
    response = client.post('/add_customer', data=dict(
        name='Raju',
        phone='1234567890'
    ), follow_redirects=True)
    
    if b'Raju' in response.data:
        print("Add Customer: SUCCESS")
    else:
        print(f"Add Customer: FAILED. Response: {response.data}")

    # 3. Add Transaction (YOU GAVE 500)
    print("Testing Add Transaction GAVE...")
    # Need to find customer ID. It should be 1.
    customer = Customer.query.filter_by(name='Raju').first()
    if not customer:
        print("FAIL: Customer not found in DB")
    else:
        response = client.post(f'/customer/{customer.id}/add_tx', data=dict(
            amount='500',
            type='GAVE',
            description='Rice Bag'
        ), follow_redirects=True)
        
        if b'500' in response.data:
            print("Add Tx GAVE: SUCCESS")
        else:
            print(f"Add Tx GAVE: FAILED. Response: {response.data}")

    # 4. Add Transaction (YOU GOT 200)
    print("Testing Add Transaction GOT...")
    response = client.post(f'/customer/{customer.id}/add_tx', data=dict(
        amount='200',
        type='GOT',
        description='Part Payment'
    ), follow_redirects=True)
    
    # 5. Check Dashboard Total
    print("Testing Dashboard Totals...")
    response = client.get('/dashboard')
    # Total should be 500 - 200 = 300 (You will get)
    if b'300' in response.data:
        print("Dashboard Total: SUCCESS")
    else:
        print(f"Dashboard Total: FAILED. Response: {response.data}")
