from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Customer, Invoice, Service  # فرض می‌کنیم مدل Service اضافه شده باشد
from datetime import datetime

app = Flask(__name__)

# تنظیمات دیتابیس
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# راه‌اندازی دیتابیس
db.init_app(app)

# لیست خدمات ثابت
SERVICES = [
    {'id': 1, 'name': 'خدمات زیرسازی و اجرای نانوسرامیک بدنه', 'price': 5000000},
    {'id': 2, 'name': 'اجرای کاور رنگی بدنه خودرو', 'price': 4000000},
    {'id': 3, 'name': 'اجرای بادی فنس (کاور محافظ بی رنگ)', 'price': 3500000},
    {'id': 4, 'name': 'پولیش حرفه ای چند مرحله', 'price': 2500000},
    {'id': 5, 'name': 'اجرای شیشه دودی (چهار درب و شیشه عقب)', 'price': 2000000},
    {'id': 6, 'name': 'آنتی UV شیشه جلو', 'price': 1500000},
    {'id': 7, 'name': 'صفر شویی کامل', 'price': 1000000},
]

@app.route('/invoice', methods=['GET', 'POST'])
def create_invoice():
    total_amount = 0
    selected_services = []

    if request.method == 'POST':
        # دریافت اطلاعات مشتری
        full_name = request.form['full_name']
        plate_number = request.form['plate_number']
        phone_number = request.form['phone_number']
        car_color = request.form['car_color']
        mileage = request.form['mileage']
        car_model = request.form['car_model']

        # دریافت خدمات انتخاب شده
        selected_service_ids = request.form.getlist('selected_services')
        selected_services = [s for s in SERVICES if str(s['id']) in selected_service_ids]
        total_amount = sum(service['price'] for service in selected_services)
        
        # می‌توانیم در اینجا اطلاعات مشتری را ذخیره کنیم
        customer = Customer(
            full_name=full_name,
            plate_number=plate_number,
            phone_number=phone_number,
            car_color=car_color,
            mileage=mileage,
            car_model=car_model
        )
        
        db.session.add(customer)
        db.session.commit()

        flash('پیش‌فاکتور با موفقیت ایجاد شد', 'success')
        return redirect(url_for('create_invoice'))
    
    return render_template('create_invoice.html', services=SERVICES, total_amount=total_amount, selected_services=selected_services)

# ساخت دیتابیس
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)