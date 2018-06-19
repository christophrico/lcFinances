from flask import Flask, render_template, json, request, redirect, session, jsonify, url_for
from flaskext.mysql import MySQL
import datetime

mysql = MySQL()
app = Flask(__name__)


#MySql config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '503h12MYSQ'
app.config['MYSQL_DATABASE_DB'] = 'lcFinances'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


#home page
@app.route('/')
def main():
    #connect to the mysql server
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT * from transactions"
    cursor.execute(query)
    transactions = cursor.fetchall()

    for trans in transactions:
        

    return render_template('index.html', data=transactions)

    #clean up
    cursor.close()
    conn.close()


#form to enter a transaction
@app.route('/showAddTrans')
def showAddTrans():
    return render_template('addTrans.html')


#route to add a transaction via MySQL
@app.route('/addTrans',methods=['POST'])
def addTrans():
    #get user input from the form
    _date = request.form['inputDate']
    _description = request.form['inputDesc']
    _amount = request.form['inputAmt']
    _code = request.form['inputCode']

    #format date to work with MySQL
    format_str = '%m/%d/%Y'
    datetime_obj = datetime.datetime.strptime(_date, format_str)
    _date = datetime_obj.date()

    #if no code selected, enter it as NULL into MySQL
    if _code == " ":
        _code = None

    #connect to the mysql server
    conn = mysql.connect()
    cursor = conn.cursor()

    #insert the user input into the database
    cursor.callproc('sp_addTrans',(_date, _description, _amount, _code))

    #check that all is well and redirect to home if so
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        return redirect('/')
    else:
        return render_template('error.html', error = 'An error occurred!')

    #clean up
    cursor.close()
    conn.close()



if __name__ == "__main__":
    app.run()
