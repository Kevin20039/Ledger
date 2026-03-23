from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Customer, Transaction

main = Blueprint('main', __name__)

@main.route('/dashboard')
@login_required
def dashboard():
    customers = Customer.query.filter_by(user_id=current_user.id).all()
    
    total_get = 0
    total_give = 0
    
    for c in customers:
        bal = c.balance
        if bal > 0:
            total_get += bal
        elif bal < 0:
            total_give += abs(bal)
            
    return render_template('dashboard.html', customers=customers, total_get=total_get, total_give=total_give)

@main.route('/add_customer', methods=['POST'])
@login_required
def add_customer():
    name = request.form.get('name')
    phone = request.form.get('phone')
    
    if name:
        new_customer = Customer(name=name, phone=phone, user_id=current_user.id)
        db.session.add(new_customer)
        db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/customer/<int:id>')
@login_required
def customer_detail(id):
    customer = Customer.query.get_or_404(id)
    if customer.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
        
    return render_template('customer.html', customer=customer)

@main.route('/customer/<int:id>/add_tx', methods=['POST'])
@login_required
def add_transaction(id):
    customer = Customer.query.get_or_404(id)
    if customer.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
        
    amount = float(request.form.get('amount'))
    tx_type = request.form.get('type') # 'GAVE' or 'GOT'
    description = request.form.get('description')
    
    new_tx = Transaction(amount=amount, type=tx_type, description=description, customer_id=customer.id)
    db.session.add(new_tx)
    db.session.commit()
    
    return redirect(url_for('main.customer_detail', id=id))

@main.route('/customer/<int:id>/delete')
@login_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    if customer.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
        
    # Delete transactions first (cascade usually handles this but being explicit is safe)
    Transaction.query.filter_by(customer_id=id).delete()
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/customer/<int:id>/report')
@login_required
def customer_report(id):
    customer = Customer.query.get_or_404(id)
    if customer.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
    return render_template('print_layout.html', customer=customer)
