from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newtest.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(50))
    city = db.Column(db.String(50))
    VAT = db.Column(db.String(50))

@app.route("/")
def main():
    return render_template('mainpage.html')

@app.route("/customers")
def customers():
    #if request.method == 'POST':
     #   company = request.form['company']
     #   city = request.form['company']
     #   VAT = request.form['vat']
    return render_template('customers.html')
@app.route("/newcustomer")
def newcustomer():
      return render_template('newcustomer.html')

@app.route("/newinvoice")
def newinvoice():
      return render_template('newinvoice.html')

@app.route("/invoice")
def invoice():
      return render_template('invoice.html')


@app.route("/newsupplier")
def newsupplier():
      return render_template('newsupplier.html')


@app.route("/suppliers")
def suppliers():
    return render_template('author.html')

@app.route("/sinvoice")
def sinvoice():
      return render_template('sinvoice.html')

@app.route("/orders")
def orders():
    return render_template('order.html')

@app.route("/issue")
def issue():
    return render_template('author.html')

@app.route("/sinvoices")
def sinvoices():
    return render_template('author.html')


@app.route("/resetdb")
def resetdb():
    db.drop_all()
    db.create_all()
    return redirect(url_for('author'))

if __name__ == '__main__':
    app.run(debug=True,port=5001)