from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newtest.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cCompany = db.Column(db.String(50))
    cAddress = db.Column(db.String(50))
    cCity = db.Column(db.String(50))
    cZIP = db.Column(db.String(50))
    cVAT = db.Column(db.String(50))
    cPhone = db.Column(db.String(15))
    cEmail = db.Column(db.String(50))

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cinvoiceCompany = db.Column(db.String(50))
    cinvoiceIssue = db.Column(db.String(50))
    cinvoiceDue = db.Column(db.String(50))
    cinvoiceText = db.Column(db.String(50))
    cinvoiceAmount = db.Column(db.Integer)

    
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sCompany = db.Column(db.String(50))
    sAddress = db.Column(db.String(50))
    sCity = db.Column(db.String(50))
    sZIP = db.Column(db.String(50))
    sVAT = db.Column(db.String(50))
    sPhone = db.Column(db.String(15))
    sEmail = db.Column(db.String(50))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carrier = db.Column(db.String(50))
    dloading = db.Column(db.String(50))
    ddelivery = db.Column(db.String(50))
    aloading = db.Column(db.String(50))
    adelivery = db.Column(db.String(50))
    goods = db.Column(db.String(50))
    note = db.Column(db.String(50))


@app.route("/")
def main():
    return render_template('mainpage.html')


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

@app.route('/listcustomers', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/listcustomers/<int:page>', methods=['GET', 'POST'])
def listcustomers(page):
    page = page
    pages = 5
    #employees = Employees.query.filter().all()
    #employees = Employees.query.paginate(page,pages,error_out=False)
    customers = Customer.query.order_by(Customer.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       customers = Customer.query.filter(Customer.cCompany.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
       #employees = Employees.query.filter(Employees.fullname == 'Tiger Nixon').paginate(per_page=pages, error_out=True) # equals: query.filter(User.name == 'ednalan')    
       #employees = Employees.query.filter(Employees.fullname.in_(['rai', 'kenshin', 'Ednalan'])).paginate(per_page=pages, error_out=True) # IN: query.filter(User.name.in_(['rai', 'kenshin', 'Ednalan']))  
       #employees = Employees.query.filter(Employees.fullname == 'Tiger Nixon', Employees.position == 'System Architect').paginate(per_page=pages, error_out=True) # AND: query.filter(User.name == 'ednalan', User.fullname == 'clyde ednalan')    
       #employees = Employees.query.filter(or_(Employees.fullname == 'Tiger Nixon', Employees.fullname == 'Ednalan')).paginate(per_page=pages, error_out=True) # OR: from sqlalchemy import or_  filter(or_(User.name == 'ednalan', User.name == 'caite'))
       return render_template('listcustomers.html', customers=customers, tag=tag)
    return render_template('listcustomers.html', customers=customers)



@app.route("/invoice")
def invoice():
      return render_template('newinvoice.html')

@app.route("/newinvoice",methods=['POST'])
def newinvoice():
    if request.method == 'POST':
        cinvoiceCompany = request.form['cinvoiceCompany']
        cinvoiceIssue = request.form['cinvoiceIssue']
        cinvoiceDue = request.form['cinvoiceDue']
        cinvoiceText = request.form['cinvoiceText']
        cinvoiceAmount = request.form['cinvoiceAmount']
        cinvoice = Invoice(cinvoiceCompany=cinvoiceCompany,cinvoiceIssue=cinvoiceIssue,cinvoiceDue=cinvoiceDue,cinvoiceText=cinvoiceText,cinvoiceAmount=cinvoiceAmount)
        db.session.add(cinvoice)
        db.session.commit()
    return render_template('newinvoice.html')


@app.route('/listinvoices', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/listinvoices/<int:page>', methods=['GET', 'POST'])
def listinvoices(page):
    page = page
    pages = 5
    invoices = Invoice.query.order_by(Invoice.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       invoices = Invoice.query.filter(Invoice.cinvoiceCompany.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
       return render_template('listinvoices.html', invoices=invoices, tag=tag)
    return render_template('listinvoices.html', invoices=invoices)

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
      return redirect(url_for('main'))
    return render_template('newsupplier.html')

@app.route('/listsuppliers', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/listsuppliers/<int:page>', methods=['GET', 'POST'])
def listsuppliers(page):
    page = page
    pages = 5
    suppliers = Supplier.query.order_by(Supplier.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       suppliers = Supplier.query.filter(Supplier.sCompany.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
       return render_template('listsuppliers.html', suppliers=suppliers, tag=tag)
    return render_template('listsuppliers.html', suppliers=suppliers)







@app.route("/suppliers")
def suppliers():
    return render_template('author.html')

@app.route("/sinvoice")
def sinvoice():
      return render_template('sinvoice.html')

@app.route("/orders")
def orders():
    return render_template('order.html')

@app.route("/neworder", methods=['POST'])
def neworder():
    if request.method == 'POST':
        carrier = request.form['carrier']
        dloading = request.form['dloading']
        ddelivery = request.form['ddelivery']
        aloading = request.form['aloading']
        adelivery = request.form['adelivery']
        goods = request.form['goods']
        note = request.form['note']
        orderpost = Order(carrier=carrier, dloading=dloading, ddelivery=ddelivery, aloading=aloading,
                          adelivery=adelivery, goods=goods, note=note)
        db.session.add(orderpost)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('neworder.html')    

@app.route('/listorders', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/listorders/<int:page>', methods=['GET', 'POST'])
def listorders(page):
    page = page
    pages = 5
    #employees = Employees.query.filter().all()
    #employees = Employees.query.paginate(page,pages,error_out=False)
    orders = Order.query.order_by(Order.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        orders = Order.query.filter(Order.id.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
        return render_template('listorders.html', orders=orders, tag=tag)
    return render_template('listorders.html', orders=orders)

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