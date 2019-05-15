from flask import *
import MySQLdb
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key="abc"
con=MySQLdb.Connect(host='localhost',user='root',passwd='',port=3306,db="dev")
cmd=con.cursor()
path1="C:\\Users\\Amrutha\\PycharmProjects\\project\\SHOPPING\\static\\image"
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/registerhere')
def registerhere():
    return render_template('ShopRegistration.html')

@app.route('/log',methods=['get','post'])
def log():
    name=request.form['textfield']
    password=request.form['textfield2']
    cmd.execute("select * from tb_login where Username='"+name+"' and password='"+password+"'")
    q=cmd.fetchone()
    print(q[3])
    if q[3]=='admin':
        return render_template("Admin_profile.html")
    elif q[3]=='shopowner':
        session['liid'] = q[0]
        session['liiid']=q[0]
        session['lid'] = q[0]
        return render_template("shopownerprofile.html")
    else:
        return '''<script>alert('invalid');window.location='/login'</script>'''


@app.route('/shome')
def shome():
    return render_template("shopownerprofile.html")

@app.route('/select')
def select():
    return render_template('select.html')
@app.route('/existing_shop')
def existing_shop():
    cmd.execute("select tb_shop.* from tb_shop join tb_login on tb_shop.shop_id = tb_login.uid  where tb_login.usertype='shopowner'")
    p=cmd.fetchall()
    print(p)
    return render_template("existing_shop.html",val=p)
@app.route('/viewshopownerprofile')
def viewshopownerprofile():
    cmd.execute("select tb_shop.* from tb_shop join tb_login on tb_shop.shop_id = tb_login.uid  where tb_login.usertype='pending'")
    o = cmd.fetchall()
    print(o)
    return render_template("view_shopownerprofile.html",val=o)
@app.route('/viewshopmore')
def viewshopmore():
    id=request.args.get('id')
    session['idd']=id
    print(id)
    cmd.execute("select tb_shop.* from tb_shop join tb_login on tb_shop.shop_id = tb_login.uid  where tb_login.usertype='pending' and tb_shop.shop_id='"+str(id)+"'")
    m = cmd.fetchone()
    print(m)
    return render_template("viewshopmore.html",val=m)
@app.route('/choose',methods={'post','get'})
def choose():
    id = session['idd']
    print(id)
    button=request.form['Submit']
    if button=='Approve':
        cmd.execute("update tb_login set usertype='shopowner' where uid='"+str(id)+"'")
        con.commit();
        return '''<script>alert('approved');window.location='/viewshopownerprofile'</script>'''
    else:
        cmd.execute("delete from tb_login where uid="+str(id)+"")
        con.commit();
        return render_template("select.html")


@app.route('/shopregister',methods={'post','get'})
def shopregister():
    shopname = request.form['textfield']
    shoptype= request.form['select']
    ownername=request.form['textfield2']
    licenceno=request.form['textfield3']
    email=request.form['textfield4']
    mobilnumber=request.form['textfield5']
    landlinenumber=request.form['textfield6']
    yearofestablishment=request.form['select2']
    shopno=request.form['textfield7']
    street=request.form['textfield8']
    city=request.form['textfield9']
    country=request.form['textfield10']
    pin = request.form['textfield11']
    enterpassword = request.form['textfield13']
    confirmpassword = request.form['textfield14']
    if enterpassword==confirmpassword:
        cmd.execute("insert into tb_login values (null,'"+shopname+"','"+enterpassword+"','pending')")
        id=con.insert_id()
        cmd.execute("insert into tb_shop values('"+str(id)+"','"+shopname+"','"+shoptype+"','"+ownername+"','"+licenceno+"','"+email+"','"+mobilnumber+"','"+landlinenumber+"','"+yearofestablishment+"','"+shopno+"','"+street+"','"+city+"','"+country+"','"+pin+"','"+enterpassword+"','"+confirmpassword+"')")
        con.commit()
        return '''<script>alert('successfully registred');window.location='/'</script>'''
    else:
        return '''<script>alert('password are not matched');window.location='/'</script>'''
@app.route('/prdtmngt')
def prdtmngt():
    return render_template('prdtmngt.html')

@app.route('/addproducts')
def addproducts():
    return render_template('addproducts.html')
@app.route('/addproduct',methods={'post','get'})
def addproduct():
    llid=session['lid']
    productname =request.form['textfield']
    producttype=request.form['select']
    brand=request.form['select2']
    madeby=request.form['select4']
    dateofmanufacture=request.form['textfield2']
    expirydate=request.form['textfield3']
    price=request.form['textfield4']
    rating=request.form['select3']
    licenceno=request.form['textfield5']
    photo=request.files['file']
    img=secure_filename(photo.filename)
    photo.save(os.path.join(path1,img))
    size=request.form['select5']
    color=request.form['select6']
    descriptions=request.form['textarea']
    cmd.execute("insert into tb_product values(null,'"+productname+"','"+producttype+"','"+brand+"','"+madeby+"','"+dateofmanufacture+"','"+expirydate+"','"+price+"','"+rating+"','"+licenceno+"','"+img+"','"+str(llid)+"','"+size+"','"+color+"','"+descriptions+"')")
    con.commit()
    return '''<script>alert('Product added');window.location='/log'</script>'''

@app.route('/viewproduct')
def viewproduct():
    liiid=session['lid']
    cmd.execute("select * from tb_product where lid='"+str(liiid)+"'")
    m = cmd.fetchall()
    print(m)
    return render_template("viewproducts.html", val=m)
@app.route('/delete',methods=['post','get'])
def delete():
    id=request.args.get('id')
    cmd.execute("delete from tb_product where product_id="+str(id)+"")
    con.commit()
    return '''<script>alert("successfully deleted");window.location='/log'</script>'''
@app.route('/update',methods=['post','get'])
def update():
    id = request.args.get('id')
    print(id,"hiiiiii")
    session['idd']=id
    cmd.execute("select * from tb_product where product_id=" + str(id) +"")
    s=cmd.fetchone()
    print(s)
    return render_template("update.html",val=s )
@app.route('/updated',methods=['post','get'])
def updated():
    id=session['idd']
    print(id)
    productname=request.form['textfield']
    producttype=request.form['select']
    brand=request.form['select2']
    madeby=request.form['select4']
    dateofmanufacture=request.form['textfield2']
    expirydate=request.form['textfield3']
    price=request.form['textfield4']
    rating=request.form['select3']
    licenceno=request.form['textfield5']
    size = request.form['select5']
    color = request.form['select6']
    descriptions = request.form['textarea']
    cmd.execute("update tb_product set productname='"+productname+"',producttype='"+producttype+"',brand='"+brand+"',madeby='"+madeby+"',dateofmanufacture='"+dateofmanufacture+"',expirydate='"+expirydate+"',price='"+price+"',rating='"+rating+"',licenceno='"+licenceno+"',size='"+size+"',color='"+color+"',descriptions='"+descriptions+"' where product_id='"+str(id)+"'")
    con.commit()
    return '''<script>alert("successfully updated");window.location='/log'</script>'''

@app.route('/noti')
def noti():
    liiid = session['lid']
    cmd.execute("select * from tb_product where lid='"+str(liiid)+"'")
    m = cmd.fetchall()
    print(m)
    return render_template('prdtntfn.html',val=m)

@app.route('/prdtntfn',methods=['post','get'])
def prdtntfn():
    productname = request.form['select4']
    offer = request.form['textarea']
    discount = request.form['textarea2']
    cmd.execute("insert into tb_notification values(null,'" +productname+ "','" +offer + "','" + discount + "')")
    con.commit()
    return '''<script>alert('Notification uploaded');window.location='/shome'</script>'''



@app.route('/viewfdbk')
def viewfdbk():
    id=session['lid']
    cmd.execute("select tb_fdbk.* from tb_fdbk join tb_shop on tb_fdbk.shopid=tb_shop.shop_id where tb_fdbk.shopid ='"+str(id)+"'")
    m = cmd.fetchall()
    print(m)
    return render_template("viewfdbk.html",val=m)



@app.route('/items')
def items():
    liiid = session['lid']
    cmd.execute("select * from tb_order where lid='" + str(liiid) + "' and orderstatus='pending'")
    m = cmd.fetchall()
    print(m)
    return render_template('vieworderditem.html', val=m)

@app.route('/viewordereditem',methods={'get','post'})
def viewordereditem():
    cmd.execute("select * from tb_order  where orderstatus='pending'")
    m = cmd.fetchall()
    session['cid']=m[0][0]
    print("hoiiiiiiiiiiiiiiiiii")
    print(m)
    return render_template("vieworderditem.html", val=m)
@app.route('/bill')
def bill():
    id=request.args.get('id')
    print(id)
    cmd.execute("select tb_orderdetails.* from tb_orderdetails join tb_order on tb_orderdetails.o_id=tb_order.o_id where tb_order.o_id='"+str(id)+"'")
    m = cmd.fetchall()
    session['oid']=m[0][1]
    print("mmmm",m)
    total=0
    for ss in m:
        total=total+float(ss[3])*float(ss[4])
    print(total)
    return render_template("bill.html", val=m,tt=total)

@app.route('/to',methods={'get','post'})
def to():
    id=session['oid']
    print('')
    button = request.form['submit']
    if button == 'Send to customer':
        cmd.execute("update tb_order set orderstatus='ok' where o_id='"+str(id)+"'")
        con.commit();
        return '''<script>alert('sended');window.location='/viewordereditem'</script>'''
    else:
        return redirect('agent')
@app.route('/agent' )
def agent():
    cmd.execute("select d_id,Name from tb_deliveryagents")
    c=cmd.fetchall()
    print(c)
    return render_template('agent.html',val=c)
@app.route('/selected',methods={'get','post'})
def selected():
    idd=session['oid']
    id = request.form['select']
    print(idd)
    print("hiiiiii")
    print(id)
    cmd.execute("update tb_order set d_id='"+str(id)+"' where o_id='"+str(idd)+"'")
    con.commit();
    return '''<script>alert('sended');window.location='/agent'</script>'''




@app.route('/viewmyprofile')
def viewmyprofile():
    diid=session['liid']
    print(diid)
    cmd.execute("select * from tb_shop where shop_id='"+str(diid)+"'")
    c = cmd.fetchone()
    print(c)
    print("hiiiiiiiiiiiiiiiiiii")
    return render_template('viewmyprofile.html',val=c)
@app.route('/asd',methods={'post','get'})
def asd():
    id = session['liid']
    print(id)
    shopname = request.form['textfield']
    shoptype = request.form['select']
    ownername = request.form['textfield2']
    licenceno = request.form['textfield3']
    email = request.form['textfield4']
    mobilnumber = request.form['textfield5']
    landlinenumber = request.form['textfield6']
    yearofestablishment = request.form['textfield13']
    shopno = request.form['textfield7']
    street = request.form['textfield8']
    city = request.form['textfield9']
    country = request.form['textfield10']
    pin = request.form['textfield12']
    cmd.execute("update tb_shop set shopname='"+shopname+"',shoptype='"+shoptype+"',ownername='"+ownername+"',licencenumber='"+licenceno+"',email='"+email+"',mobilenumber='"+mobilnumber+"',landlinenumber='"+landlinenumber+"',yearofestablishment='"+yearofestablishment+"',shopno='"+shopno+"',street='"+street+"',city='"+city+"',country='"+country+"',pin='"+pin+"' where shop_id='"+str(id)+"'")
    con.commit();
    return '''<script>alert('updated');window.location='/shome'</script>'''


@app.route('/login2')
def login2():
    return render_template('changepassword.html')
@app.route('/change',methods=['get','post'])
def change():
    lid=session['lid']
    newpassword=request.form['textfield2']
    confirmpassword=request.form['textfield3']
    currentpassword=request.form['textfield']
    if newpassword==confirmpassword:
        cmd.execute("update tb_login set password='"+newpassword+"' where uid='"+str(lid)+"'")
        con.commit();
        return '''<script>alert('password changed');window.location='/shome'</script>'''
    else:
        return '''<script>alert('password are not matched');window.location='/login2'</script>'''


@app.route('/shoplogout')
def shoplogout():
    return render_template('home.html')




@app.route('/viewcustomerprofile')
def viewcustomerprofile():
    cmd.execute("select tb_customer.* from tb_customer join tb_login on tb_customer.c_id = tb_login.uid  where tb_login.usertype='custpendi'")
    a = cmd.fetchall()
    print(a)
    return render_template('view_customerprofile.html',val = a)
@app.route('/viewmorecustomer')
def viewmorecustomer():
    id=request.args.get('id')
    session['idd'] = id
    print(id)
    cmd.execute("select tb_customer.* from tb_customer join tb_login on tb_customer.c_id = tb_login.uid  where tb_login.usertype='custpendi' and tb_customer.c_id='"+str(id)+"'")
    c = cmd.fetchone()
    print(c)
    return render_template('viewcustomermore.html',val=c)
@app.route('/choosed',methods={'post','get'})
def choosed():
    id = session['idd']
    print(id)
    button=request.form['Submit']
    if button=='Approve':
        cmd.execute("update tb_login set usertype='customer' where uid='"+str(id)+"'")
        con.commit();
        return '''<script>alert('approved');window.location='/viewshopownerprofile'</script>'''
    else:
        return render_template("view_customerprofile.html")





@app.route('/selectda')
def selectda():
    return render_template('selectde_agents.html')
@app.route('/existingda')
def existingda():
    cmd.execute("select tb_deliveryagents.* from tb_deliveryagents join tb_login on tb_deliveryagents.d_id = tb_login.uid  where tb_login.usertype='agent'")
    p = cmd.fetchall()
    print(p)
    return render_template("existing da.html", val=p)
@app.route('/deleted')
def deleted():
        id = request.args.get('id')
        cmd.execute("delete from tb_deliveryagents where d_id=" + str(id) + "")
        con.commit()
        return '''<script>alert("successfully deleted");window.location='/existingda'</script>'''


@app.route('/viewdeliveryagentsprofile')
def viewdeliveryagentsprofile():
    cmd.execute("select tb_deliveryagents.* from tb_deliveryagents join tb_login on tb_deliveryagents.d_id = tb_login.uid  where tb_login.usertype='agentpendi'")
    b = cmd.fetchall()
    print(b)
    return render_template('view_deliveryagentsprofile.html',val= b)
@app.route('/viewdamore')
def viewdamore():
    id = request.args.get('id')
    session['idd'] = id
    print(id)
    cmd.execute("select tb_deliveryagents.* from tb_deliveryagents join tb_login on tb_deliveryagents.d_id = tb_login.uid  where tb_login.usertype='agentpendi' and tb_deliveryagents.d_id='"+str(id)+"'")
    s=cmd.fetchone()
    print(s)
    return render_template('viewdamore.html',val = s)
@app.route('/choice',methods={'post','get'})
def choice():
    id = session['idd']
    print(id)
    button=request.form['Submit']
    if button=='Approve':
        cmd.execute("update tb_login set usertype='agent' where uid='"+str(id)+"'")
        con.commit();
        return '''<script>alert('approved');window.location='/selectda'</script>'''
    else:
        cmd.execute("delete from tb_login where uid="+str(id)+"")
        con.commit();
        return render_template("selectde_agents.html")



@app.route('/viewdeliveryreports',methods={'post','get'})
def viewdeliveryreports():
     return render_template('view_deliveryreports.html')
@app.route('/viewdeliveryreportss',methods=['get','post'])
def viewdeliveryreportss():
    date = request.form['textfield']
    cmd.execute("select * from tb_dailyreport where date='" + date + "'")
    s=cmd.fetchall()
    return render_template('view_deliveryreports.html',val=s)


@app.route('/viewcomplaints')
def viewcomplaints():
    cmd.execute("select * from tb_complaintreply where reply='pending'")
    y = cmd.fetchall()
    print(y)
    return render_template('view_complaints.html',val=y)
@app.route('/complaint')
def complaint():
    id=request.args.get('id')
    session['idd'] = id
    cmd.execute("select * from tb_complaintreply where complaint_id='"+str(id)+"'")
    y = cmd.fetchone()
    print(y)
    return render_template('complaint.html',val=y)
@app.route('/sendreplay',methods={'post','get'})
def sendreplay():
        id = session['idd']
        reply=request.form['textarea']
        cmd.execute("update tb_complaintreply set reply='"+reply+"' where complaint_id='" + str(id) + "'")
        con.commit();
        return '''<script>alert('sended');window.location='/viewcomplaints'</script>'''



@app.route('/logout')
def logout():
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)
