from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'secret_key_here'  # استخدم مفتاح حقيقي في مشروع فعلي

# قاعدة بيانات وهمية للمستخدمين
users = {
    "test@example.com": "1234"
}

# الصفحة الرئيسية
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', advice=None, show_advice=False)

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['user'] = email
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="بيانات الدخول غير صحيحة")
    return render_template('login.html')

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/calculate', methods=["POST"])
def calculate():
    name = request.form["name"]
    age = int(request.form["age"])
    height = float(request.form["height"])
    weight = float(request.form["weight"])
    condition = request.form["condition"]

    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        bmi_category = "نقص في الوزن"
    elif 18.5 <= bmi <= 24.9:
        bmi_category = "وزن مثالي"
    elif 25 <= bmi <= 29.9:
        bmi_category = "زيادة في الوزن"
    else:
        bmi_category = "سمنة"

    return render_template("home.html", show_advice=True,
                           name=name,
                           age=age,
                           bmi_category=bmi_category,
                           condition=condition)




# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
