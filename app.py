from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Customer,Invoice
from datetime import datetime

app = Flask(__name__)

# تنظیمات دیتابیس
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # برای flash messages

# راه‌اندازی دیتابیس
db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/invoices')
def invoices():
    search = request.args.get('search', '')
    
    if search:
        # جستجو در نام مشتری یا شماره پلاک
        customers = Customer.query.filter(
            db.or_(
                Customer.full_name.ilike(f'%{search}%'),
                Customer.plate_number.ilike(f'%{search}%')
            )
        ).order_by(Customer.id.desc()).all()
    else:
        # نمایش همه فاکتورها به ترتیب جدیدترین
        customers = Customer.query.order_by(Customer.id.desc()).all()
    
    return render_template('invoices.html', customers=customers)

@app.route('/invoice/<int:id>')
def show_invoice(id):
    # پیدا کردن فاکتور با شناسه مورد نظر
    invoice = Invoice.query.get_or_404(id)
    
    # تبدیل services از JSON به لیست دیکشنری
    if invoice.services:
        services = invoice.services
    else:
        services = []
    
    return render_template('invoice_detail.html', 
                         invoice=invoice, 
                         services=services)
@app.route('/invoice/<int:id>/edit', methods=['GET', 'POST'])
def edit_invoice(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        # کد ویرایش اطلاعات
        pass
    return render_template('edit_invoice.html', customer=customer)

SERVICES = [
    {'id': 1, 'name': 'خدمات زیرسازی و اجرای نانوسرامیک بدنه', 'price': 5000000},
    {'id': 2, 'name': 'اجرای کاور رنگی بدنه خودرو', 'price': 4000000},
    {'id': 3, 'name': 'اجرای بادی فنس (کاور محافظ بی رنگ)', 'price': 3500000},
    {'id': 4, 'name': 'پولیش حرفه ای چند مرحله', 'price': 2500000},
    {'id': 5, 'name': 'اجرای شیشه دودی (چهار درب و شیشه عقب)', 'price': 2000000},
    {'id': 6, 'name': 'آنتی UV شیشه جلو', 'price': 1500000},
    {'id': 7, 'name': 'صفر شویی کامل', 'price': 1000000},
]

@app.route('/customer/<int:customer_id>/services', methods=['GET', 'POST'])
def select_services(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'POST':
        selected_service_ids = request.form.getlist('selected_services')
        notes = request.form.get('notes')
        
        # انتخاب خدمات از لیست ثابت
        selected_services = [s for s in SERVICES if str(s['id']) in selected_service_ids]
        total_amount = sum(service['price'] for service in selected_services)
        
        # ایجاد فاکتور جدید
        invoice = Invoice(
            customer_id=customer.id,
            services=selected_services,
            total_amount=total_amount,
            notes=notes
        )
        
        db.session.add(invoice)
        db.session.commit()
        
        flash('فاکتور با موفقیت ثبت شد', 'success')
        return redirect(url_for('view_invoice', id=invoice.id))
    
    return render_template('select_services.html', customer=customer, services=SERVICES)
@app.route('/new-invoice', methods=['GET', 'POST'])
def new_invoice():
    if request.method == 'POST':
        try:
            new_customer = Customer(
                full_name=request.form['full_name'],
                plate_number=request.form['plate_number'],
                phone_number=request.form['phone_number'],
                car_color=request.form['car_color'],
                mileage=int(request.form['mileage']) if request.form['mileage'] else 0,
                reception_date=datetime.strptime(request.form['reception_date'], '%Y-%m-%d'),
                entry_date=datetime.strptime(request.form['entry_date'], '%Y-%m-%d'),
                car_model=request.form['car_model']
            )
            
            db.session.add(new_customer)
            db.session.commit()
            
            flash('اطلاعات مشتری با موفقیت ثبت شد', 'success')
            return redirect(url_for('select_services', customer_id=new_customer.id))
            
        except Exception as e:
            flash('خطا در ثبت اطلاعات', 'error')
            print(e)
            
    return render_template('new_invoice.html')

# ساخت دیتابیس
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)