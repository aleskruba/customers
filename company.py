from flask import Flask, render_template, redirect, url_for, request,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms import StringField,SubmitField
from wtforms.validators import ValidationError,DataRequired
from flask_wtf import FlaskForm
from sqlalchemy import or_
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aa619dbda413f99de65fde9b865605c5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newtest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sCompany = db.Column(db.String(50))
    sAddress = db.Column(db.String(50))
    sCity = db.Column(db.String(50))
    sZIP = db.Column(db.String(50))
    sVAT = db.Column(db.String(50))
    sPhone = db.Column(db.String(15))
    sEmail = db.Column(db.String(50))
    orders = db.relationship('Order',backref='supplier',lazy='dynamic')
    sinvoices = db.relationship('Sinvoice',backref='supplier',lazy='dynamic')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dloading = db.Column(db.String(50))
    ddelivery = db.Column(db.String(50))
    aloading = db.Column(db.String(50))
    adelivery = db.Column(db.String(50))
    goods = db.Column(db.String(50))
    note = db.Column(db.String(50))
    price = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer,db.ForeignKey('supplier.id'))

class Sinvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sinvoiceIssue = db.Column(db.String(50))
    sinvoiceDue = db.Column(db.String(50))
    sinvoiceText = db.Column(db.String(50))
    sinvoiceAmount = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer,db.ForeignKey('supplier.id'))

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cCompany = db.Column(db.String(50))
    cAddress = db.Column(db.String(50))
    cCity = db.Column(db.String(50))
    cZIP = db.Column(db.String(50))
    cVAT = db.Column(db.String(50),unique=True)
    cPhone = db.Column(db.String(15))
    cEmail = db.Column(db.String(50))
    invoices = db.relationship('Invoice',backref='customer',lazy='dynamic')

       

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cinvoiceIssue = db.Column(db.String(50))
    cinvoiceDue = db.Column(db.String(50))
    cinvoiceText = db.Column(db.String(50))
    cinvoiceAmount = db.Column(db.Integer)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'))

    


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
        if Customer.query.filter(Customer.cVAT == request.form['cVAT']).first():
            flash('Record was not saved !!!!! VAT alredy exists in the database','danger')
            return redirect(url_for('main'))
        else:
            db.session.add(cPost)
            db.session.commit()
            flash('Record was saved','success')
            return redirect(url_for('main'))
    return render_template('newcustomer.html',form=form)

@app.route('/listcustomers', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/listcustomers/<int:page>', methods=['GET', 'POST'])
def listcustomers(page):
    page = page
    pages = 10
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



@app.route("/editcustomer/<int:page>",methods=['GET','POST'])
def editcustomer(page):
    post = Customer.query.get_or_404(page)
    if request.method == 'POST':
        post.cCompany = request.form['cCompany']
        post.cCity = request.form['cCity']
        post.cVAT = request.form['cVAT']
        post.cAddress = request.form['cAddress']
        post.cZIP = request.form['cZIP']
        post.cPhone = request.form['cPhone']
        post.cEmail = request.form['cEmail']
        db.session.commit()
        return redirect(url_for('listcustomers'))
    return render_template('editcustomers.html', post=post)

@app.route('/invoicecustomer', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/invoicecustomer/<int:page>', methods=['GET', 'POST'])
def invoicecustomer(page):
    page = page
    pages = 10
    customers = Customer.query.order_by(Customer.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       customers = Customer.query.filter(Customer.cCompany.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
       return render_template('invoicecustomer.html', customers=customers, tag=tag)
    return render_template('invoicecustomer.html', customers=customers)

@app.route("/invoice/<int:page>", methods=['GET','POST'])
def invoice(page):
    cust = Customer.query.get_or_404(page)
    return render_template('newinvoice.html',cust=cust)

@app.route("/newinvoice/<int:page>",methods=['POST'])
def newinvoice(page):
    post = Customer.query.get_or_404(page)
    if request.method == 'POST':
        cinvoiceIssue = request.form['cinvoiceIssue']
        cinvoiceDue = request.form['cinvoiceDue']
        cinvoiceText = request.form['cinvoiceText']
        cinvoiceAmount = request.form['cinvoiceAmount']
        cinvoice = Invoice(customer=post,cinvoiceIssue=cinvoiceIssue,cinvoiceDue=cinvoiceDue,cinvoiceText=cinvoiceText,cinvoiceAmount=cinvoiceAmount)
        db.session.add(cinvoice)
        db.session.commit()
        return redirect(url_for('listinvoices'))
    return render_template('newinvoice.html')




@app.route("/editinvoice/<int:page>",methods=['GET','POST'])
def editinvoice(page):
    post = Invoice.query.get_or_404(page)
    cust = Customer.query.all()
    if request.method == 'POST':
        post.customer_id = request.form['customer']
        post.cinvoiceIssue = request.form['cinvoiceIssue']
        post.cinvoiceDue = request.form['cinvoiceDue']
        post.cinvoiceText = request.form['cinvoiceText']
        post.cinvoiceAmount = request.form['cinvoiceAmount']
        db.session.commit()
        return redirect(url_for('listinvoices'))
    return render_template('editinvoice.html', post=post,cust=cust)



@app.route('/listinvoices', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/listinvoices/<int:page>', methods=['GET', 'POST'])
def listinvoices(page):
    page = page
    pages = 10 
    invoices = Invoice.query.order_by(Invoice.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        
        invoices = Invoice.query.join(Customer).filter(Customer.cCompany.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
        return render_template('listinvoices.html', invoices=invoices, tag=tag)
    return render_template('listinvoices.html', invoices=invoices )

@app.route("/printinvoice/<int:page>",methods=['POST','GET'])
def printinvoice(page):
    
    invoices = Invoice.query.filter_by(id=page).one()
    return render_template('invoice.html',invoices=invoices)






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
      if Supplier.query.filter(Supplier.sVAT == request.form['sVAT']).first():
            flash('Record was not saved !!!!! VAT alredy exists in the database','danger')
      else: 
              
            db.session.add(sPost)
            db.session.commit()
      return redirect(url_for('main'))
    return render_template('newsupplier.html')

@app.route('/listsuppliers', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/listsuppliers/<int:page>', methods=['GET', 'POST'])
def listsuppliers(page):
    page = page
    pages = 10
    suppliers = Supplier.query.order_by(Supplier.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       suppliers = Supplier.query.filter(Supplier.sCompany.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
       return render_template('listsuppliers.html', suppliers=suppliers, tag=tag)
    return render_template('listsuppliers.html', suppliers=suppliers)


@app.route("/editsupplier/<int:page>",methods=['GET','POST'])
def editsupplier(page):
    post = Supplier.query.get_or_404(page)
    if request.method == 'POST':
        post.sCompany = request.form['sCompany']
        post.sCity = request.form['sCity']
        post.sVAT = request.form['sVAT']
        post.sAddress = request.form['sAddress']
        post.sZIP = request.form['sZIP']
        post.sPhone = request.form['sPhone']
        post.sEmail = request.form['sEmail']
        db.session.commit()
        return redirect(url_for('listsuppliers'))
    return render_template('editsuppliers.html', post=post)


@app.route('/invoicesupplier', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/invoicesupplier/<int:page>', methods=['GET', 'POST'])
def invoicesupplier(page):
    page = page
    pages = 10
    suppliers = Supplier.query.order_by(Supplier.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       suppliers = Supplier.query.filter(Supplier.sCompany.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
       return render_template('invoicesupplier.html', suppliers =suppliers , tag=tag)
    return render_template('invoicesupplier.html', suppliers = suppliers )



@app.route("/newsinvoice/<int:page>",methods=['POST'])
def newsinvoice(page):
    sup = Supplier.query.get_or_404(page)
    if request.method == 'POST':
        sinvoiceIssue = request.form['sinvoiceIssue']
        sinvoiceDue = request.form['sinvoiceDue']
        sinvoiceText = request.form['sinvoiceText']
        sinvoiceAmount = request.form['sinvoiceAmount']
        sinvoice = Sinvoice(supplier=sup,sinvoiceIssue=sinvoiceIssue,sinvoiceDue=sinvoiceDue,sinvoiceText=sinvoiceText,sinvoiceAmount=sinvoiceAmount)
        db.session.add(sinvoice)
        db.session.commit()
        return redirect(url_for('invoicesupplier'))
    return render_template('newsinvoice.html')


@app.route("/sinvoice/<int:page>", methods=['GET','POST'])
def sinvoice(page):
    sup = Supplier.query.get_or_404(page)
    return render_template('newsinvoice.html',sup=sup)

@app.route('/listsinvoices', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/listsinvoices/<int:page>', methods=['GET', 'POST'])
def listsinvoices(page):
    page = page
    pages = 10 
    sinvoices = Sinvoice.query.order_by(Sinvoice.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        
        sinvoices = Sinvoice.query.join(Supplier).filter(Supplier.sCompany.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
        return render_template('listsinvoices.html', sinvoices=sinvoices, tag=tag)
    return render_template('listsinvoices.html', sinvoices=sinvoices )


@app.route("/editsinvoice/<int:page>",methods=['GET','POST'])
def editsinvoice(page):
    post = Sinvoice.query.get_or_404(page)
    sup = Supplier.query.all()
    if request.method == 'POST':
        post.supplier_id = request.form['supplier']
        post.sinvoiceIssue = request.form['sinvoiceIssue']
        post.sinvoiceDue = request.form['sinvoiceDue']
        post.sinvoiceText = request.form['sinvoiceText']
        post.sinvoiceAmount = request.form['sinvoiceAmount']
        db.session.commit()
        return redirect(url_for('listsinvoices'))
    return render_template('editsinvoice.html', post=post,sup=sup)


@app.route('/order', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/order/<int:page>', methods=['GET', 'POST'])
def order(page):
    page = page
    pages = 10
    suppliers = Supplier.query.order_by(Supplier.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
       tag = request.form["tag"]
       search = "%{}%".format(tag)
       suppliers = Supplier.query.filter(Supplier.sCompany.like(search)).paginate(per_page=pages, error_out=False)
       return render_template('invoicesupplier.html', suppliers =suppliers , tag=tag)
    return render_template('invoicesupplier.html', suppliers = suppliers )


@app.route("/neworder/<int:page>",methods=['POST'])
def neworder(page):
    sup = Supplier.query.get_or_404(page)
    if request.method == 'POST':
        dloading = request.form['dloading']
        ddelivery = request.form['ddelivery']
        aloading = request.form['aloading']
        adelivery = request.form['adelivery']
        goods = request.form['goods']
        note = request.form['note']
        price = request.form['price']
        orderpost = Order(supplier=sup,dloading=dloading, ddelivery=ddelivery, aloading=aloading,
                          adelivery=adelivery, goods=goods, note=note,price=price)
        db.session.add(orderpost)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('neworder.html')    

@app.route('/listorders', methods=['GET', 'POST'], defaults={"page": 1}) 
@app.route('/listorders/<int:page>', methods=['GET', 'POST'])
def listorders(page):
    page = page
    pages = 5
    orders = Order.query.order_by(Order.id.asc()).paginate(page,pages,error_out=False)  #desc()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        orders = Order.query.filter(Order.id.like(search)).paginate(per_page=pages, error_out=False) # LIKE: query.filter(User.name.like('%ednalan%'))
        return render_template('listorders.html', orders=orders, tag=tag)
    return render_template('listorders.html', orders=orders)

@app.route("/sorder/<int:page>", methods=['GET','POST'])
def sorder(page):
    sup = Supplier.query.get_or_404(page)
    return render_template('order.html', sup=sup)

@app.route("/editorder/<int:page>",methods=['GET','POST'])
def editorder(page):
    post = Order.query.get_or_404(page)
    sup = Supplier.query.all()
    if request.method == 'POST':
        post.supplier_id = request.form['supplier']
        post.dloading = request.form['dloading']
        post.ddelivery = request.form['ddelivery']
        post.aloading = request.form['aloading']
        post.adelivery = request.form['adelivery']
        post.goods = request.form['goods']
        post.note = request.form['note']
        post.price = request.form['price']
        db.session.commit()
        return redirect(url_for('listorders'))
    return render_template('editorder.html', post=post,sup=sup)

@app.route("/printorder/<int:page>",methods=['POST','GET'])
def printoder(page):
    
    orders = Order.query.filter_by(id=page).one()
    return render_template('orderprint.html',orders=orders)



if __name__ == '__main__':
    app.run(debug=True,port=5001)
    
    