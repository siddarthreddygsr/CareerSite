from flask import Flask, jsonify, request, session, redirect,render_template, url_for
from passlib.hash import pbkdf2_sha256
import time
import smtplib, ssl
from app import db, client
import uuid


class User:

	def start_session(self, user):
		del user['password']
		session['logged_in'] = True
		session['user'] = user
		return jsonify(user), 200

	def signup(self):

		# verification_code = str(uuid.uuid4().hex)
		# Create the user object
		user = {
		"_id": uuid.uuid4().hex,
		"name": request.form.get('name'),
		"email": request.form.get('email'),
		"password": request.form.get('password'),
		"token_generation_epoch": int(time.time())
		}

		# Encrypt the password
		user['password'] = pbkdf2_sha256.encrypt(user['password'])

		# Check for existing email address
		if db.users.find_one({ "email": user['email'] }):
			return jsonify({ "error": "Email address already in use" }), 400
		else:
			print("yo")
			db.users.insert_one(user)
			return jsonify({ "error": "Account created." }), 400

	def signout(self):
		session.clear()
		return redirect('/')
	
	def sign_up(self):
		return render_template('signup.html')
	

	def login(self):

		user = db.users.find_one({
		"email": request.form.get('email')
		})

		if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
			return self.start_session(user)
		return jsonify({ "error": "Invalid login credentials" }), 401


	def search_unique_email(self):
		search = request.form.get('searchTerm')
		search = "^" + search + ".*"
		user = db.users.find(
			{
				"email" : { "$regex": search, "$options": "i" }
			}
		)
		return jsonify(list(user))
	
	def adduni(self):
		return render_template('adduni.html')

	def adduni_image(self):
		if 'uni-image' in request.files:
			uni_image = request.files['uni-image']
			client.save_file(uni_image.filename, uni_image)
			db.unapproved_universities.insert({"university": request.form.get('university'), "image": uni_image.filename})

		return 'Done!'
	

#userid
#roomi