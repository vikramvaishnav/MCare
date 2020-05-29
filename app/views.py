
# Python modules
import os, logging 
from flask_jsonpify import jsonify
import folium
# Flask modules
import datetime
from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from app.db_to_df import db_to_df
# App modules
from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm
from app.engine import LSTM_Model
from app.mapcsv_to_df import  map_to_df
from app.ep_model import  Ep_model
from app.hospitals_resource_fetch import hospitals_resource_fetch
# provide login manager with load_user callback
epm=Ep_model()
epm.data_fetch()
model_month=LSTM_Model(df=db_to_df(csv=True,dburl='postgresql://postgres:postgres@database-1.cpka5l6nyg2j.ap-south-1.rds.amazonaws.com:5432/mcare',tablename='medicineinventorymonthly',file='data/CSV/monthly.csv'),model_path="data/Models/monthly")
model_month.train()
labels,data=model_month.predict()
model_week= LSTM_Model(df=db_to_df(csv=True,dburl='postgresql://postgres:postgres@database-1.cpka5l6nyg2j.ap-south-1.rds.amazonaws.com:5432/mcare',file='data/CSV/weekly.csv',tablename="medicineinventoryweekly"),model_path="data/Models/weekly")
#model_week.train()
labels_week,data_week=model_week.predict_week()

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/register.html', form=form, msg=msg ) )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/register.html', form=form, msg=msg ) )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unkkown user"

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/login.html', form=form, msg=msg ) )

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None

    try:

        # try to match the pages defined in -> pages/<input file>
        if path == 'map.html':
            
            map() 
            print(path)  

        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path) )
    except:
        
        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/404.html' ) )

# Return sitemap 
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

#Folium map generator
def map():
    start_coords = (18.5204, 73.8567)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    hnames,latitude,longitude= map_to_df()
    for i in range(len(hnames)):
        folium.Marker([float(latitude[i]),float(longitude[i])],popup='<i>'+hnames[i]+'</i>').add_to(folium_map)
    folium_map.save('app/templates/pages/map_content.html')
#map api call   
@app.route('/map')
def mapapi():
    return render_template("pages/map_content.html")
#past inventory monthly data api
@app.route('/pastinvapi',methods=['POST'])
def invapi():
    if request.method == 'POST':
            df= db_to_df(csv=True,dburl='postgresql://postgres:postgres@database-1.cpka5l6nyg2j.ap-south-1.rds.amazonaws.com:5432/mcare',tablename='medicineinventorymonthly',file='data/CSV/monthly.csv')
            labels=list(df['datum'])[-5:]
            print(labels)
            #last 5month
            ldata = [list(df[i])[-5:] for i in df.columns if i!='datum']
            
            names=[i for i in df.columns if i!='datum']

            return jsonify({"labels":labels,"data" :ldata, 'names':names})
# predicted inventory monthly data api 
@app.route('/predictinvapi',methods=['POST'])
def predictinvapi():
    if request.method == 'POST':
            
            print(labels)
            #last 5month
            print(data)
            ldata = [list(i.values())[0] for i in data ]
            print(ldata)
            names=[str(list(i.keys())[0]) for i in data]
            #print(labels,names,ldata)
            return jsonify({"labels":labels,"data" :ldata, 'names':names})

#past inventory weekly data api
@app.route('/pastweeklyinvapi',methods=['POST'])
def invweeklyapi():
    if request.method == 'POST':
            df=db_to_df(csv=True,file='data/CSV/weekly.csv',tablename="medicineinventoryweekly")
            labels=list(df['datum'])[-5:]
            print(labels)
            labels=[str(datetime.datetime.strptime(i,'%m/%d/%Y').strftime('%Y-%m-%d')) for i in labels]
            #last 5month
            ldata = [list(df[i])[-5:] for i in df.columns if i!='datum']
            
            names=[i for i in df.columns if i!='datum']

            return jsonify({"labels":labels,"data" :ldata, 'names':names})
#predicted inventory weekly data api
@app.route('/predictweeklyinvapi',methods=['POST'])
def predictweeklyinvapi():
    if request.method == 'POST':
            
            print(labels_week)
            #last 5month
            print(data_week)
            ldata = [list(i.values())[0] for i in data_week ]
            print(ldata)
            names=[str(list(i.keys())[0]) for i in data_week]
            #print(labels,names,ldata)
            return jsonify({"labels":labels_week,"data" :ldata, 'names':names})

#table api show current inventory - next month required inventory 
@app.route('/currenttable',methods=['POST'])
def currenttableapi():
    if request.method == 'POST':
            

            df= db_to_df(csv=True)

            percentages=[]
            current_month = [list(i.values())[0][0] for i in data ]
            total_last_month=sum([list(df[i])[-2] for i in df.columns if i!='datum'])
            next_month= [list(i.values())[0][1] for i in data ]
            next_weeks=[list(i.values())[0][1:4] for i in data_week ]
            for i in range(len(current_month)):
                if current_month[i]< sum(next_weeks[i]):
                    percent= int((current_month[i]*100)/sum(next_weeks[i]))
                else:
                    percent=100
                percentages.append(str(percent))
            print(percentages)
            names=[str(list(i.keys())[0]) for i in data]
            #print(labels,names,ldata)
            return jsonify({"percentages":percentages,"nextmonth":next_month,"data" :current_month, 'names':names, 'last_month':total_last_month})

#DORM
@app.route('/dorm',methods=['POST'])
def dormapi():
    if request.method=='POST':
        print('request')
        today= [float(i) for i in epm.today_data()]
        tom=[float(i) for i in  epm.tomorrow_data()]
        outbreak={'today':today, 'tomorrow':tom}
        hospital=hospitals_resource_fetch()
        hdict={}
        hdict['beds']=float(hospital['Number of Beds'])
        hdict['emergency']= float(hospital['Number of Beds in Emergency Wards '])
        hdict['doctors']= float(hospital['Number of Doctors'])
        hdict['nurses'] = float(hospital['Number of Nurses'])
        return jsonify({'outbreak':outbreak,'hospitalinfo':hdict })


