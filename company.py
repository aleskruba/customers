from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newtest.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cCompany = db.Column(db.String(50))
    cAddress = db.Column(db.String(50))
    cCity = db.Column(db.String(50))
    cZIP = db.Column(db.String(50))
    cVAT = db.Column(db.Integer)
    cPhone = db.Column(db.String(15))
    cEmail = db.Column(db.String(50))
    
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sCompany = db.Column(db.String(50))
    sAddress = db.Column(db.String(50))
    sCity = db.Column(db.String(50))
    sZIP = db.Column(db.String(50))
    sVAT = db.Column(db.Integer)
    sPhone = db.Column(db.String(15))
    sEmail = db.Column(db.String(50))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)


@app.route("/")
def main():
    return render_template('mainpage.html')

@app.route("/listcustomers")
def listcustomers():
  customers = Customer.query.all()
  return render_template('listcustomers.html',customers=customers)

@app.route("/customers")
def customers():
    return render_template('newcustomer.html')

@app.route("/newcustomer",methods=['POST'])
def newcustomer():
  if request.method == 'POST':
    cCompany = request.form['cCompany']
    cCity = request.form['cCity']
    cVAT = request.form['cVAT']
    cAddress = request.form['cAddress']
    cZIP = request.form['cZIP']
    cPhone = request.form['cPhone']
    cEmail = request.form['cEmail']
    cPost = Customer(cCompany=cCompany, cCity=cCity, cAddress=cAddress, cVAT=cVAT, cZIP=cZIP, cPhone=cPhone, cEmail=cEmail)
    db.session.add(cPost)
    db.session.commit()
    return redirect(url_for('main'))
  return render_template('newcustomer.html')

@app.route("/newinvoice")
def newinvoice():
      return render_template('newinvoice.html')

@app.route("/invoice")
def invoice():
      return render_template('invoice.html')

@app.route("/listsuppliers")
def listsuppliers():
  suppliers = Supplier.query.all()
  return render_template('listsuppliers.html',suppliers=suppliers)


@app.route("/supplier")
def supplier(): 
    return render_template('newsupplier.html')

@app.route("/newsupplier", methods=['POST'])
def newsupplier():
  if request.method == 'POST':
    sCompany = request.form['sCompany']
    sCity = request.form['sCity']
    sVAT = request.form['sVAT']
    sAddress = request.form['sAddress']
    sZIP = request.form['sZIP']
    sPhone = request.form['sPhone']
    sEmail = request.form['sEmail']
    sPost = Supplier(sCompany=sCompany, sCity=sCity, sAddress=sAddress, sVAT=sVAT, sZIP=sZIP, sPhone=sPhone, sEmail=sEmail)
    db.session.add(sPost)
    db.session.commit()
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