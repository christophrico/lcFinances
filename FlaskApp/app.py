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
    return render_template('index.html', data = getData())



#route to get the transactions in the server
@app.route('/getData',methods=['POST'])
def getData():
    #connect to the mysql server
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "SELECT *, DATE_FORMAT( transDate, '%m/%d/%Y') FROM transactions ORDER BY transDate ASC"
    cursor.execute(query)
    transactions = cursor.fetchall()

    return transactions

    #clean up
    cursor.close()
    conn.close()



#route to add a transaction via MySQL
@app.route('/addTrans',methods=['POST'])
def addTrans():
    #get user input from the form
    _date = request.form['inputDate']
    _description = request.form['inputDesc']
    _amount = request.form['inputAmt']
    _code = request.form['inputCode']
    _adjAmt = request.form['inputAdjAmt']


    #format date to work with MySQL
    if _date is None:
        return render_template('error.html', error = 'An error occurred!')
    else:
        format_str = '%m/%d/%Y'
        datetime_obj = datetime.datetime.strptime(_date, format_str)
        _date = datetime_obj.date()

    #if no code selected, enter it as NULL into MySQL
    #if there is a code selected, then adjAmt must be null so MySQL will calculate it
    if _code == " ":
        _code = None
    else:
        _adjAmt = None


    #connect to the mysql server
    conn = mysql.connect()
    cursor = conn.cursor()
    query = "INSERT INTO transactions (transDate, description, amt, transCode, adjAmt) VALUES(%s, %s, %s, %s, %s)"
    #insert the user input into the database
    cursor.execute(query, (_date, _description, _amount, _code, _adjAmt))

    #check that all is well and redirect to home if so
    data = cursor.fetchall()
    if len(data) is 0:
        conn.commit()
        return main()
    else:
        return render_template('error.html', error = 'An error occurred!')

    #clean up
    cursor.close()
    conn.close()








if __name__ == "__main__":
    app.run()
