from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect, render_template, url_for
from flask_mail import Mail, Message
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'biostatsGroup'
mysql.init_app(app)

app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = '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'
app.config['MAIL_DEFAULT_SENDER'] = 'biostatsprojects@gmail.com'
mail = Mail(app)

name = ''


@app.route('/')
def index():
    return render_template('index.html', title='Biostats Sign-in')


@app.route('/', methods=['POST'])
def signin():
    inputData = (request.form.get('inputEmail'), request.form.get('inputPassword'))
    cursor = mysql.get_db().cursor()
    query = """SELECT * FROM userAccount WHERE email = %s AND password = %s"""
    cursor.execute(query, inputData)
    result = cursor.fetchall()
    count = cursor.rowcount

    if count == 0:
        return render_template('index.html', title='Biostats Sign-in', response='Incorrect Email / Password')
    else:
        if result[0]['verified'] == 1:
            global name
            name = result[0]['fName'] + ' ' + result[0]['lName']
            return redirect('/home', code=302)
        else:
            return render_template('index.html', title='Biostats Sign-in', response='Account not verified. Please '
                                                                                    'check email to verify account '
                                                                                    'before access.')


@app.route('/register')
def register_page():
    return render_template('register.html', title='Register')


@app.route('/register', methods=['POST'])
def register():
    inputData = (request.form.get('inputFname'), request.form.get('inputLname'), request.form.get('inputEmail'),
                 request.form.get('inputPassword'))
    email = request.form.get('inputEmail')

    cursor = mysql.get_db().cursor()
    email_check_query = """SELECT id FROM userAccount where email=%s"""
    new_input_query = """INSERT INTO userAccount (fName, lName, email, password, verified) VALUES (%s, %s, %s, %s, 
    0) """
    cursor.execute(email_check_query, email)
    email_exist = cursor.rowcount

    if email_exist == 1:
        return render_template('register.html', title='Register', response='An account already exists with this email.')
    else:
        cursor.execute(new_input_query, inputData)
        mysql.get_db().commit()
        cursor.execute(email_check_query, email)
        result = cursor.fetchall()

        msg = Message('Activate Biostats Data Manager Account', recipients=[email])
        msg.body = ('Congratulations and welcome to the Biostats family! Please click here to activate you account. '
                    '**P.S. You will not be able to sign in until account is activated**')
        msg.html = (f'<h1>Activate Biostats Data Manager Account</h1>'
                    f'<p>Congratulations and welcome to the Biostats family! Please '
                    f'<a href=\"http://0.0.0.0:5000/activate/{result[0]["id"]}\">click here</a> to activate your '
                    f'account.</p><br><i>**P.S. You will not be able to sign in until account is activated**</i>')
        mail.send(msg)
        return render_template('register.html', title='Register', response_s=f'Success! Please check email ({email}) '
                                                                             f'for link to verify account')


@app.route('/activate/<int:new_id>', methods=['GET'])
def activate(new_id):
    cursor = mysql.get_db().cursor()
    sql_update_query = """UPDATE userAccount a SET a.verified = 1 WHERE a.id = %s"""
    cursor.execute(sql_update_query, new_id)
    mysql.get_db().commit()
    return render_template('index.html', title='Biostats Sign-in', status='Account VERIFIED!!! You may now sign in.')


@app.route('/home', methods=['GET'])
def home():
    if name:
        user = {'username': name}
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM biostatsData')
        result = cursor.fetchall()
        return render_template('home.html', title='Home', user=user, biostats=result)
    else:
        return redirect(url_for("index"))


# CURRENTLY WORKING --- DO NOT TAMPER
@app.route('/view/<int:stat_id>', methods=['GET'])
def record_view(stat_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostatsData WHERE id=%s', stat_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', biostat=result[0])


@app.route('/edit/<int:stat_id>', methods=['GET'])
def form_edit_get(stat_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostatsData WHERE id=%s', stat_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', biostat=result[0])


@app.route('/edit/<int:stat_id>', methods=['POST'])
def form_update_post(stat_id):
    cursor = mysql.get_db().cursor()
    inputData = (
        request.form.get('Name'), request.form.get('Sex'), request.form.get('Age'), request.form.get('Height_in'),
        request.form.get('Weight_lbs'), stat_id)
    sql_update_query = """UPDATE biostatsData t SET t.Name= %s, t.Sex= %s, t.Age=%s, t.Height_in=%s, t.Weight_lbs=%s
                        WHERE t.id=%s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect('/home', code=302)


@app.route('/biostats/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Biostats Form')


@app.route('/statistics', methods=['GET'])
def statistics():
    if name:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT  Age FROM biostatsData')
        result = cursor.fetchall()
        for row in result:
            print(row)
        return render_template('statistics.html', biostats=result)


@app.route('/biostats/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (
        request.form.get('Name'), request.form.get('Sex'), request.form.get('Age'), request.form.get('Height_in'),
        request.form.get('Weight_lbs'))
    sql_insert_query = """INSERT INTO biostatsData (Name, Sex, Age, Height_in, Weight_lbs) VALUES (%s, %s, %s, %s,
    %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect('/home', code=302)


@app.route('/delete/<int:stat_id>', methods=['POST'])
def form_delete_post(stat_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM biostatsData WHERE id=%s"""
    cursor.execute(sql_delete_query, stat_id)
    mysql.get_db().commit()
    return redirect('/home', code=302)


@app.route('/signout')
def signout():
    global name
    name = ''
    return redirect(url_for('index'))


# API functions

@app.route('/api/v1/biostats', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostatsData')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/biostats/<int:stat_id>', methods=['GET'])
def api_retrieve(stat_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostatsData WHERE id=%s', stat_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/biostats/', methods=['POST'])
def api_add() -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Name'], content['Sex'], content['Age'], content['Height_in'], content['Weight_lbs'])
    sql_insert_query = """INSERT INTO biostatsData (NAME, SEX, AGE, HEIGHT_IN, WEIGHT_LBS) VALUES (%s, %s, %s, %s, 
    %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/biostats/<int:stat_id>', methods=['PUT'])
def api_edit(stat_id) -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Name'], content['Sex'], content['Age'], content['Height_in'], content['Weight_lbs'], stat_id)
    sql_insert_query = """UPDATE biostatsData b SET b.Name = %s, b.Sex =%s, b.Age =%s, b.Height_in = %s, b.Weight_lbs 
    = %s WHERE b.id = %s """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()

    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/biostats/<int:stat_id>', methods=['DELETE'])
def api_delete(stat_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM biostatsData WHERE id = %s"""
    cursor.execute(sql_delete_query, stat_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/simple_chart', methods=['GET'])
def chart():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('chart.html', values=values, labels=labels, legend=legend)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
