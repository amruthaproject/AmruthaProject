from flask import *
import MySQLdb
from flask.globals import request, session
from flask.helpers import make_response
from flask.templating import render_template
from werkzeug.utils import secure_filename
import os
app=Flask(__name__)
con=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='',db='dev')
cmd=con.cursor()
app.secret_key='abcd'
pt="G:\\signlanguage detectionnew\\signlangaugedetection\\src\\static\\photos"
path="C:\\Users\\manu\\PycharmProjects\\vr shopping\\SHOPPING\\static\\da"
@app.route('/login',methods=['POST','GET'])
def login():
    uname=request.args.get('uname')
    password=request.args.get('pass')
    try:
        cmd.execute("select * from tb_login where username='"+uname+"' and password='"+password+"'")
        s=cmd.fetchone()
        id=s[0]
        return jsonify({'result':str(id)+"#"+str(s[3])})
    except Exception as e:
        print(str(e))
        return jsonify({'result':"invalid"})

@app.route('/reg',methods=['POST'])
def reg():
    print("okok")
    name = request.form['Name']
    age=request.form['age']
    print(name)
    print(age)
    gender = request.form['gender']

    dob = request.form['dateofbirth']
    print(dob)
    qualification = request.form['qualification']

    houseno= request.form['houseno']
    street = request.form['street']

    city = request.form['city']

    country = request.form['country']


    email = request.form['email']

    phoneno = request.form['phoneno']

    epswd = request.form['enterpassword']

    cpswd = request.form['confirmpassword']
    print(cpswd)

    img = request.files['files']
    fname = secure_filename(img.filename)
    print(fname)

    img.save(os.path.join(path, fname))

    cmd.execute("insert into tb_login values(null,'" +str( name) + "','" + str(cpswd) + "','agentpendi')")
    idd = con.insert_id()

    print(idd)
    cmd.execute("insert into tb_deliveryagents values('"+ str(idd) +"','" + name + "','" +age + "','"+dob+"','"+gender+"','" + qualification + "','" + houseno + "','" + street + "','" + city+ "','" + country + "','"+email+"','"+phoneno+"','"+epswd+"','"+fname+"')")


    con.commit()
    return jsonify({'result': "success"})





@app.route('/viewordereditems',methods=['GET'])
def viewordereditems():
    did = request.args.get('lid')
    print(did)
    cmd.execute("select tb_orderdetails.* from tb_orderdetails join tb_order on tb_orderdetails.o_id= tb_order.o_id where tb_order.d_id='"+str(did)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/vitems',methods=['post','get'])
def vitems():
    id=request.args.get('id')
    cmd.execute("select tb_customer.* from tb_customer join tb_order on tb_customer.c_id = tb_order.c_id where tb_order.o_id='"+str(id)+"'")
    print("select tb_customer.* from tb_customer join tb_order on tb_customer.c_id = tb_order.c_id where tb_order.o_id='"+str(id)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchone()
    if results is not None:
     json_data = []
     print()
     # for result in results:
     json_data.append(dict(zip(row_headers, results)))
     con.commit()
     print(json_data)
     return jsonify(json_data)
    else:
        return jsonify({'result': "failed"})



@app.route('/deliv_status',methods=['get','post'])
def deliv_status():
    did = request.args.get('lid')
    print("lid--",did)
    cmd.execute("select * from tb_order where d_id='"+str(did)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
     json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/ds',methods=['post','get'])
def ds():
    order_id=request.args.get('order_id')
    print(order_id)
    cmd.execute("select tb_orderdetails.price,tb_product.productname,tb_order.date,tb_customer.customername from tb_product join tb_orderdetails on tb_orderdetails.product_id=tb_product.product_id join tb_order on tb_order.o_id=tb_orderdetails.o_id join tb_customer on tb_customer.c_id=tb_order.c_id where tb_order.o_id='"+str(order_id)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/deliverystatus',methods=['post','get'])
def deliverystatus():
    date = request.args.get('date')
    o_id = request.args.get('order_id')
    ordereditem= request.args.get('orderditem')
    amount = request.args.get('amount')
    #customername = request.args.get('custname')
    deliverystatus= request.args.get('delivery')
    cmd.execute("insert into tb_dailyreport values(null,'"+str(date)+"','"+str(o_id)+"','"+str(amount)+"','"+ordereditem+"','"+deliverystatus+"')")
    con.commit()
    return jsonify({'result': "success"})


@app.route('/bi',methods=['post','get'])
def bi():
    cmd.execute("select * from tb_order")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/bs',methods=['post','get'])
def bs():
    order_id=request.args.get('order_id')
    cmd.execute("select tb_orderdetails.price,tb_product.productname,tb_order.date,tb_customer.customername,tb_customer.c_id from tb_product join tb_orderdetails on tb_orderdetails.product_id=tb_product.product_id join tb_order on tb_order.o_id=tb_orderdetails.o_id join tb_customer on tb_customer.c_id=tb_order.c_id where tb_order.o_id='"+str(order_id)+"'")
    # print("select tb_order.customer_name,tb_order.c_id,tb_orderdetails.productname,tb_orderdetails.price from tb_order inner join tb_orderdetails on tb_order.o_id=tb_orderdetails.o_id where tb_order.o_id='" + str(order_id) + "'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)


@app.route('/billstatus',methods=['post','get'])
def billstatus():
    cid = request.args.get('custid')
    ordereditem = request.args.get('orderditem')
    customername = request.args.get('custname')
    amount = request.args.get('amount')
    o_id = request.args.get('order_id')
    billstatus = request.args.get('billing')
    cmd.execute("insert into tb_bill values(null,'" + str(cid) + "','"+ordereditem+"','" + customername + "','" +str(amount) + "','" + billstatus + "','"+str(o_id)+"')")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/custviewbill',methods=['post','get'])
def custviewbill():
    id=request.args.get('id')
    print(id)
    cmd.execute("select * from tb_bill where c_id='"+str(id)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)


@app.route('/viewprofile',methods=['post','get'])
def viewprofile():
    did = request.args.get('lid')
    cmd.execute("select * from tb_deliveryagents where d_id='" + str(did) + "'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchone()
    json_data = []
    json_data.append(dict(zip(row_headers, results)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/updateprofile',methods=['post','get'])
def updateprofile():
    did = request.args.get('lid')
    Name = request.args.get('name')
    age = request.args.get('age')
    dob= request.args.get('dateofbirth')
    gender = request.args.get('gender')
    #qualification = request.args.get('qualification')
    houseno = request.args.get('houseno')
    street = request.args.get('street')
    city = request.args.get('city')
    country = request.args.get('country')
    email = request.args.get('email')
    phoneno = request.args.get('phoneno')
    cmd.execute("update tb_deliveryagents set Name='"+Name+"',age='"+age+"',dateofbirth='"+dob+"',gender='"+gender+"',houseno='"+houseno+"',street='"+street+"',city='"+city+"',country='"+country+"',email='"+email+"',phoneno='"+phoneno+"' where d_id='"+str(did)+"'")
    # print("update tb_deliveryagents set Name='"+Name+"',age='"+age+"',dateofbirth='"+dob+"',gender='"+gender+"',houseno='"+houseno+"',street='"+street+"',city='"+city+"',country='"+country+"',email='"+email+"',phoneno='"+phoneno+"' where d_id='"+str(did)+"'")
    # print(did)
    cmd.execute("update tb_login set username='" +str( Name) +"' where uid='"+str(did)+"'")
    con.commit()
    return jsonify({'result': "updated"})

@app.route('/changepassword', methods=['POST', 'GET'])
def changepassword():
    curpass =  request.args.get('curpass')
    newpass =  request.args.get('newpass')
    conpass =   request.args.get('conpass')
    lid = request.args.get('lid')
    cmd.execute("select * from tb_login where  password='" + str(curpass) + "' and uid='" + str(lid) + "'")
    print("select * from tb_login where  password='" + str(curpass) + "' and uid='" + str(lid) + "'")
    s = cmd.fetchone()
    if s is None:
        return jsonify({'result': "failed"})
    else:
        cmd.execute("update tb_login set password='" + str(newpass) + "' where uid='" + str(lid) + "'")
        con.commit()
        return jsonify({'result': "success"})

@app.route('/custreg',methods=['POST','GET'])
def custreg():
    try:
        name = request.args.get('name')
        age = request.args.get('age')
        gender = request.args.get('gender')
        houseno = request.args.get('houseno')

        street = request.args.get('street')

        city = request.args.get('city')

        pin = request.args.get('pin')
        email = request.args.get('email')
        phoneno = request.args.get('phoneno')
        cpswd= request.args.get('cpswd')
        #print("insert into tb_login values(null,'" + name + "','" + cpswd + "','customer')")
        cmd.execute("insert into tb_login values(null,'" + name + "','" + cpswd + "','custpendi')")
        idd = con.insert_id()
        cmd.execute("insert into tb_customer values('"+str(idd)+"','" + name + "','" + str(age) + "','"+gender+"','" + houseno + "','" + street + "','" + city + "','" + pin + "','" + email + "','" + phoneno + "')")
        con.commit()
        return jsonify({'result': "success"})
    except Exception as e:
        print(e)
        return jsonify({'result': "error"})

@app.route('/vwprofile',methods=['post','get'])
def vwprofile():
    did = request.args.get('lid')
    cmd.execute("select * from tb_customer where c_id='"+str(did)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/upprofile',methods=['post','get'])
def upprofile():
    lid = request.args.get('lid')
    customername= request.args.get('Name')
    age = request.args.get('age')
    gender = request.args.get('gender')
    housenumber = request.args.get('houseno')
    street = request.args.get('street')
    city = request.args.get('city')
    pin= request.args.get('pin')
    email =request.args.get('email')
    phonenumber = request.args.get('phoneno')
    cmd.execute("update tb_customer set customername='"+customername+"',age='"+age+"',gender='"+gender+"',housenumber='"+housenumber+"',street='"+street+"',city='"+city+"',pin='"+pin+"',email='"+email+"',phonenumber='"+phonenumber+"' where c_id='"+str(lid)+"'")
    con.commit()
    return jsonify({'result': "updated"})


@app.route('/cpassword', methods=['POST', 'GET'])
def cpassword():
    curpass =  request.args.get('curpass')
    newpass =  request.args.get('newpass')
    conpass =   request.args.get('conpass')
    lid = request.args.get('lid')
    cmd.execute("select * from tb_login where  password='" + str(curpass) + "' and uid='" + str(lid) + "'")
    print("select * from tb_login where  password='" + str(curpass) + "' and uid='" + str(lid) + "'")
    s = cmd.fetchone()
    if s is None:
        return jsonify({'result': "failed"})
    else:
        cmd.execute("update tb_login set password='" + str(newpass) + "' where uid='" + str(lid) + "'")
        con.commit()
        return jsonify({'result': "success"})



@app.route('/shopselect')
def shopselect():
    cmd.execute("select * from tb_shop ")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/givefdbk',methods=['get','post'])
def givefdbk():
    lid = request.args.get('lid')
    shopid= request.args.get('shops')
    print(shopid)
    feedback = request.args.get('feedback')
    print (feedback)
    cmd.execute("insert into tb_fdbk values (null,'"+str(lid)+"','"+feedback+"',curdate(),curtime(),'"+str(shopid)+"')")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/givecomplaint',methods=['get','post'])
def givecomplaint():
    id = request.args.get('lid')
    complaint=request.args.get('complaint')
    print(complaint)
    cmd.execute("insert into tb_complaintreply values (null,'"+str(id)+"','"+complaint+"','pending',curdate(),curtime())")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/complaintset',methods=['get'])
def complaintset():
    did = request.args.get('lid')
    print(did)
    cmd.execute("select complaint_id,complaint,reply from tb_complaintreply where c_id='"+str(did)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)


@app.route('/getproduct',methods=['get','post'])
def getproduct():

    cmd.execute("select * from tb_product ")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
     json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)


@app.route('/productnoti',methods=['GET','POST'])
def productnoti():
    id=request.args.get('id')
    cmd.execute("select tb_product.productname,tb_notification.* from tb_product join tb_notification on tb_product.product_id=tb_notification.productname where tb_product.product_id='"+str(id)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
     json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/ptview',methods=['get','post'])
def ptview():
    id=request.args.get('sid')
    cmd.execute("select * from tb_product where lid='"+str(id)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/ptview2',methods=['get','post'])
def ptview2():
    id=request.args.get('pid')
    cmd.execute("select * from tb_product where product_id='"+str(id)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/prdtview',methods=['get','post'])
def prdtview():
    cmd.execute("select * from tb_bill where c_id='" + str(id) + "'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/select',methods=['get','post'])
def select():
    id=request.args.get('pid')
    print(id)
    price=request.args.get('price')
    quantity=request.args.get('quantity')
    cmd.execute("select max(o_id)from tb_order")
    oid = cmd.fetchone()
    orid=oid[0]

    # print("insert into tb_orderdetails(null,'"+str(orid)+"','"+str(id)+"','"+str(quantity)+"','"+str(price)+"')")
    cmd.execute("insert into tb_orderdetails values(null,'"+str(orid)+"','"+str(id)+"','"+str(quantity)+"','"+str(price)+"')")
    print()
    con.commit()
    return jsonify({'result': "success"})


@app.route('/trackorder',methods=['get','post'])
def trackorder():
    id=request.args.get('lid')
    cmd.execute("select * from tb_order where orderstatus='ok' and c_id='"+str(id)+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/tracking',methods=['get','post'])
def tracking():
    oid=request.args.get('oid')
    did=request.args.get('did')
    cmd.execute("select * from tb_trackorder  where d_id='"+did+"' and o_id='"+oid+"'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)


@app.route('/productview',methods=['post','get'])
def productview():
    lid = request.args.get('lid')
    cmd.execute("select * from tb_product where product_id='" + str(lid) + "'")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchone()
    json_data = []
    json_data.append(dict(zip(row_headers, results)))
    con.commit()
    print(json_data)
    return jsonify(json_data)



@app.route('/pt',methods=['post','get'])
def pt():
    cmd.execute("select * from tb_shop")
    row_headers = [x[0] for x in cmd.description]
    results = cmd.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/prdt',methods=['post','get'])
def prdt():
    lid=request.args.get('shop_id')
    cmd.execute("insert into tb_order values(null,'0','0','0','0','pending','"+lid+"')")
    con.commit()
    return jsonify({'result':"success"})


@app.route('/purchase',methods=['get','post'])
def purchase():
    o_id=request.args.get('o_id')
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')
    price= request.args.get('price')
    cmd.execute("insert into tb_orderdetails values (null,'"+o_id+"','"+product_id+"','"+quantity+"','"+price+"'")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/order_conf',methods=['get','post'])
def order_conf():
    cid=request.args.get('cid')
    cmd.execute("select max(o_id)from tb_order")
    oid = cmd.fetchone()
    # oid = oid[0]
    print(str(cid),str(oid[0]))
    cmd.execute("Select * from tb_orderdetails where o_id='"+str(oid[0])+"' ")
    s=cmd.fetchall()
    print(s)
    total = 0
    for ss in s:
        total = total + float(ss[3]) * float(ss[4])
    print("total----",total)
    cmd.execute("update tb_order set c_id='"+cid+"', amount='"+str(total)+"', date=curdate() where o_id='"+str(oid[0])+"' ")
    con.commit()
    return jsonify({'result': "success"})

@app.route('/availcheack',methods=['get','post'])
def availcheack():
    pin=request.args.get('pin')
    cmd.execute("select pin from tb_pin where pin='"+str(pin)+"'")
    s=cmd.fetchone()
    if(s is None):
        return  jsonify({'result':"notavailable"})
    else:
        return jsonify({'result': "available"})



if __name__=="__main__":
    app.run(host="192.168.43.29",port=5000)



