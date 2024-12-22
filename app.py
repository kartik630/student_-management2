from flask import Flask, render_template, request, url_for, flash, session
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
from datetime import date

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'student_management1'

mysql = MySQL(app)
app.secret_key = "super secret key"

@app.route('/index')
def home():
     cur = mysql.connection.cursor()
     cur.execute("SELECT * FROM students")
     data = cur.fetchall()
     cur.close()
     return render_template('home.html' ,students=data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        dob = request.form['dob']
        Class = request.form['Class']
        adm_no = request.form['adm_no']
        contact_info = request.form['contact_info']
        Email = request.form['Email']
        gender = request.form['gender']
        blood = request.form['blood']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        cur.execute("INSERT INTO students (name,dob,Class,adm_no, contact_info,Email,gender,blood) VALUES (%s,%s,%s,%s, %s,%s,%s,%s)", (name,dob,Class,adm_no, contact_info,Email,gender,blood))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    
@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        Class = request.form['Class']
        adm_no = request.form['adm_no']
        dob = request.form['dob']
        contact_info = request.form['contact_info']
        Email = request.form['Email']
        gender = request.form['gender']
        blood = request.form['blood']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students SET name=%s,dob=%s,Class=%s ,adm_no=%s,contact_info=%s,Email=%s,gender=%s,blood=%s
        WHERE id=%s
        """, (name, dob,Class,adm_no, contact_info,Email,gender,blood, id_data))
        flash("Data Updated Successfully")
        cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    
        return redirect(url_for('home'))
                        

@app.route('/studentlogin')
def student_login():        
    return render_template('login2.html')

@app.route('/adminlogin' , methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username=%s AND password=%s',(username,password,))
        record = cur.fetchone()
        cur.close()
        if record:
             session['loggedin']= True
             session['username']= record[1]
             return redirect(url_for('back'))
        else:
            return 'INVALID USERNAME OR PASSWORD'
    return render_template('login.html')

@app.route('/admin')
def back():
    return render_template('back.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index2')
def index2():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    return render_template('index1.html', students=students)

@app.route('/attendance', methods=['GET','POST'])
def attendance():
    student_ids = request.form.getlist('attendance')
    today = date.today()
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM attendance WHERE date = %s", [today])
    for student_id in student_ids:
        cur.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",(student_id, today, 'Present'))
    cur.execute("SELECT id FROM students")
    all_students = cur.fetchall()
    for student in all_students:
        if str(student[0]) not in student_ids:
            cur.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",(student[0], today, 'Absent'))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index2'))


@app.route('/view_attendance', methods=['GET', 'POST'])
def view_attendance():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        selected_date = request.form.get('date')
        cur.execute("""
            SELECT students.name, attendance.status 
            FROM attendance 
            INNER JOIN students ON attendance.student_id = students.id 
            WHERE attendance.date = %s
        """, [selected_date])
        records = cur.fetchall()
        cur.close()
        return render_template('attendance.html', records=records, selected_date=selected_date)
    today = date.today()
    cur.execute("""
        SELECT students.name, attendance.status 
        FROM attendance 
        INNER JOIN students ON attendance.student_id = students.id 
        WHERE attendance.date = %s
    """, [today])
    records = cur.fetchall()
    cur.close()
    return render_template('attendance.html', records=records, selected_date=today)

if __name__ == '__main__':
    app.run(debug=True)


