from flask import Flask, render_template, request, url_for, flash, session
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'student_management1'

mysql = MySQL(app)
app.secret_key = "super secret key"

@app.route('/home')
def home():
     cur = mysql.connection.cursor()
     cur.execute("SELECT * FROM students")
     data = cur.fetchall()
     cur.close()
     return render_template('home.html',username= session['username'] ,students=data)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('home.html', students=data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        dob = request.form['dob']
        contact_info = request.form['contact_info']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        cur.execute("INSERT INTO students (name,dob, contact_info) VALUES (%s,%s, %s)", (name,dob, contact_info))
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
        dob = request.form['dob']
        contact_info = request.form['contact_info']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students SET name=%s,dob=%s, contact_info=%s
        WHERE id=%s
        """, (name, dob, contact_info, id_data))
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
             return redirect(url_for('home'))
        else:
            return 'INVALID USERNAME OR PASSWORD'
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == "__main__":
     app.run(debug=True)