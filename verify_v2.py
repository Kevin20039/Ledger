from app import create_app, db
from models import User, Customer, Transaction

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['WTF_CSRF_ENABLED'] = False
client = app.test_client()

with app.app_context():
    db.create_all()
    
    # 1. Register & Login
    print("Testing Registration...")
    client.post('/', data=dict(signup='true', username='user', password='pw', business_name='SmartBiz'), follow_redirects=True)
    
    # 2. Check Dashboard for new elements
    print("Testing Dashboard Elements...")
    response = client.get('/dashboard')
    html = response.data.decode('utf-8')
    
    if 'SmartLedger - Business Manager' in html:
        print("PASS: New Title Found")
    else:
        print("FAIL: Old Title or Missing")

    if 'canvas id="balanceChart"' in html:
        print("PASS: Chart Canvas Found")
    else:
        print("FAIL: Chart Canvas Missing")
        
    if 'id="searchInput"' in html:
        print("PASS: Search Input Found")
    else:
        print("FAIL: Search Input Missing")

    # 3. Add Customer & Check Report Route
    print("Testing Report Route...")
    resp_add = client.post('/add_customer', data=dict(name='New Guy', phone='999'), follow_redirects=True)
    if b'New Guy' in resp_add.data:
        print("Add Customer: SUCCESS")
    else:
        print("Add Customer: FAILED")
        
    print("Checking Session after Add...")
    resp_dash = client.get('/dashboard')
    if resp_dash.status_code == 200:
        print("Session OK")
    else:
        print(f"Session LOST: {resp_dash.status_code}")

    # ID should be 1
    response = client.get('/customer/1/report')
    if response.status_code == 200:
        print("PASS: Report Generated")
    else:
        print(f"FAIL: Report Route. Status: {response.status_code}")
        if response.status_code == 302:
            print(f"Redirecting to: {response.headers.get('Location')}")

