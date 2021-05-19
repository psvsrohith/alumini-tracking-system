from flask import *
import pymongo,os,smtplib,imghdr,re
from email.message import EmailMessage
from werkzeug.utils import secure_filename

UPLOAD_FOLDER=r'D:\Abhi\alumni\static\profile'
ALLOWED_EXTENSIONS={'txt','pdf','png','jpg','jpeg','gif'}
start=Flask(__name__)
start.secret_key='abhi'

client=pymongo.MongoClient("mongodb://localhost:27017")

start.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def accessStudent(roll):
	db=client['alumni']
	st=db[roll[:4]]
	return st.find_one({'id':roll})

def accessCollege(roll):
	db=client['alumni']
	st=db['college']
	return st.find_one({'id':roll})
#a
@start.route('/login/<int:num>/')
def accPass(num):
    return render_template('accounts.html',type=num)


#b


#c
@start.route('/cform/')
def c_signup():
    return render_template('collegeSignup.html')

@start.route('/collegeGroup/<string:name>')
def collegeGroup(name):
	return render_template('collegeGroup.html',type=2,roll=name)


@start.route('/collegeProfiles/<string:name>',methods=['GET','POST'])
def editCollegeProfiles(name):
	db=client['alumni']
	st=db['college']
	res=request.form
	new={'$set':{'director':res['director'],'contact':res['contact'],'website':res['website'],'email':res['email'],'address':res['address'],'accredition':res['accredition']}}
	st.update_one({'id':name},new)
	return redirect(url_for('collegeProfile',name=name))

@start.route('/collegeProfile/<string:name>')
def collegeProfile(name):
	db=client['alumni']
	x=accessCollege(name)
	st=db[name+'_post']
	y=st.find()
	li=[]
	for u in y:
		st=db['posts']
		li.append(st.find_one({"_id":u['id']}))
	li.reverse()
	return render_template('collegeProfile.html',type=2,roll=name,req=x,req2=li)

@start.route('/collegeRequests/<string:name_c>/<string:type1>/<string:name_s>')
def collegeRequests(name_c,name_s,type1):
	db=client['alumni']
	requests=db['requests']
	
	if type1=='1':
		x=requests.find_one({'id':name_s})
		acc={'id':x['id'],'password':x['password']}
		perm=db[name_c]
		perm.insert_one({'year':name_s[0:2]})
		perm=db[name_s[0:4]]
		perm.insert_one(x)
		perm=db['accounts']
		perm.insert_one(acc)

	requests.remove({'id':name_s})
	return redirect(url_for('collegeRequest',name=name_c))

@start.route('/collegeRequest/<string:name>')
def collegeRequest(name):
	db=client['alumni']
	requests=db['requests']
	x=requests.find({'college':name})
	return render_template('collegeRequest.html',type=2,req=x,roll=name)

#d


#e
@start.route('/<int:num>/event/<string:name>')
def event(num,name):
	if num==1:
		return render_template('event.html',type=num,roll=name)
	elif num==2:
		return render_template('event.html',type=num,roll=name)
	else:
		return render_template('event.html',type=num,roll='Directorate')


@start.route('/editCollegeProfile/<string:name>')
def editCollegeProfile(name):
	x=accessCollege(name)
	return render_template('editCollegeProfile.html',roll=name,req=x)


@start.route('/editStudentProfile/<string:name>')
def editStudentProfile(name):
	x=accessStudent(name)
	return render_template('editStudentProfile.html',req=x)



#f
@start.route('/forget/',methods=['GET','POST'])
def forget():
		res=request.form.get('fp')
		global name_in_page	
		msg = EmailMessage()
		msg['Subject'] = 'Check out Bronx as a puppy!'
		msg['From'] = 'yaswanthmogili543@gmail.com'
		msg['To'] = res
		msg.set_content('This is a plain text email')
		msg.add_alternative("""\
			<!DOCTYPE html>
			<html>
			<body>
			<h1 style="color:SlateGray;">This is an HTML Email!</h1>
			</body>
			</html>
			""", subtype='html')
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login('yaswanthmogili543@gmail.com', '******')
			smtp.send_message(msg)
		return redirect(url_for('login'))

@start.route('/login/<int:num>/forgot.html')
def forgot(num): 	
 	return render_template('forgot.html')


#g


#h
@start.route('/home/<int:num>/<string:name>')
def home(num,name):
	db=client['alumni']
	posts=db['posts']
	x=posts.find()
	li=[]
	for u in x:
		li.append(u)
	li.reverse()
	return render_template('home.html',type=num,roll=name,req=li)


#i


#j


#k


#l
@start.route('/login/')
def login():
    return render_template('login.html')

@start.route('/logged/<int:num>',methods=['GET','POST'])
def logged(num):
	try:
		res=request.form
		db=client["alumni"]
		if num==1:
			alumni=db['accounts']
			existing_user=alumni.find_one({'id':res['account']})
			if existing_user is None:
				flash("Wrong Credentials")
				return redirect(request.referrer)
			else:
				if existing_user['password']==res['pass']:
					return redirect(url_for('home',num=1,name=existing_user['id']))
				else:
					flash("Wrong Credentials")
					return redirect(request.referrer)
		elif num==2:
			college=db['college']
			existing_college=college.find_one({'short':res['account']})
			if existing_college is None:
				flash("Wrong Credentials")
				return redirect(request.referrer)
			else:
				if existing_college['pass']==res['pass']:
					return redirect(url_for('home',num=2,name=existing_college['id']))
				else:
					flash("Wrong Credentials")
					return redirect(request.referrer)
		else:
			directorate=db['directorate']
			passw=directorate.find_one({'pass':res['pass']})
			if  passw is None:
				flash("Wrong Credentials")
				return redirect(request.referrer)
			else:
				return redirect(url_for('home',num=3,name='Directorate'))
	except:
		flash("Wrong Credentials")
		return redirect(request.referrer)

@start.route('/login.html/')
def logout():
	return render_template('accounts.html',type=1)


#m


#n
@start.route('/newPost/<int:num>/<string:name>')
def newPost(name,num):
	return render_template('newPostCreation.html',type=num,roll=name)


#o


#p
@start.route('/<int:num>/<string:name>/post',methods=['GET','POST'])
def post(num,name):
	db=client['alumni']

	if num==1:
		y=accessStudent(name)
		y=y['first']+' '+y['last']
	else:
		y=accessCollege(name)
		y=y['account']

	posts=db['posts']
	res=request.form
	x=res['description']
	x=posts.insert_one({'post':x,'person_id':y})
	posts=db[name+'_post']
	posts.insert_one({'id':x.inserted_id})
	return redirect(url_for('home',num=num,name=name))


#q


#r
@start.route('/recieved_file/<string:filename>')
def recieved_file(filename):
	x=accessStudent(filename)
	head,tail=os.path.split('static/profile/'+x['profile'])
	return send_from_directory(head,tail)

#s
@start.route('/')
def startFirst():
	return render_template('start.html')

@start.route('/login/signup/')
def signup():
    return render_template('studentSignup.html')

@start.route('/<name>/signupSuccess.html',methods=['POST','GET'])
def signupSuccess(name):
	res=request.form
	db=client['alumni']
	alumni=db['requests']
	existing_user=alumni.find_one({'id':res['roll']})
	if existing_user is None:
		x=res['roll']
		y=alumni.insert_one({'email':res['account'],'profile':'','password':res['pass'],'id':x,'first':res['first'],
			'last':res['last'],'phone':res['phone'],'aadhar':res['aadhar'],'gender':res['radios'],'college':x[2:4]})
		return render_template('signupSuccess.html')
	else:
		return render_template('alreadyAccount.html')

@start.route('/studentChat/<string:name>')
def studentChat(name):
	return render_template('studentChat.html',type=1,roll=name)

@start.route('/studentGroup/<string:name>')
def studentGroup(name):
	return render_template('studentGroup.html',type=1,roll=name)

@start.route('/studentProfileImg/<string:name>',methods=['GET','POST'])
def studentProfileImg(name):
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(url_for('studentProfile',name=name))
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(url_for('studentProfile',name=name))
		elif file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(start.config['UPLOAD_FOLDER'], filename))
	
	db=client['alumni']
	st=db[name[:4]]
	new={'$set':{'profile':filename}}
	st.update_one({'id':name},new)
	return redirect(url_for('studentProfile',name=name))

@start.route('/studentProfiles/<string:name>',methods=['GET','POST'])
def studentProfiles(name):
	res=request.form
	db=client['alumni']
	st=db[name[:4]]
	new={'$set':{'first':res['first'],'last':res['last'],'phone':res['phone'],'education':res['education'],'job':res['job'],'works':res['works'],'mar':res['radios'],'email':res['email'],'social':res['social'],'address':res['address']}}
	st.update_one({'id':name},new)
	return redirect(url_for('studentProfile',name=name))

@start.route('/studentProfile/<string:name>')
def studentProfile(name):
	db=client['alumni']
	x=accessStudent(name)
	y=[]
	st=db[name+'_post']
	y=st.find()
	li=[]
	for u in y:
		st=db['posts']
		li.append(st.find_one({"_id":u['id']}))
	li.reverse()
	return render_template('studentProfile.html',type=1,req=x,roll=name,req2=li)

#t


#u


#v


if __name__=='__main__':
    start.run(debug=True)
