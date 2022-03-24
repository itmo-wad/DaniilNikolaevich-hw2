import hashlib
import os
import random
import uuid

from flask import Flask, render_template, redirect, make_response, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User

engine = create_engine('postgresql+psycopg2://wad-adm:StrongPassw0rd@127.0.0.1:55437/wad_db')
Session = sessionmaker(bind=engine)
session = Session()  # type: sqlalchemy.orm.Session

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def root():
    token = request.cookies.get('token')
    result = session.query(User).where(User.token == token).all()
    if not result:
        return redirect("/login")
    return redirect("/profile")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/profile")
def profile():
    token = request.cookies.get('token')
    result = session.query(User).where(User.token == token).all()
    if not result:
        return redirect("/login")
    avatar = 'default.jpg' if not result[0].avatar_uuid else result[0].avatar_uuid
    return render_template("profile.html", name=result[0].name, surname=result[0].surname, avatar=avatar,
                           year=random.randint(0, 5))


@app.route("/register", methods=['GET'])
def register():
    return render_template("register.html")


@app.route("/register/new", methods=['POST'])
def register_new():
    data = request.form
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    surname = data.get("surname")
    password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()

    result = session.query(User).where(User.email == email).all()
    if result:
        return render_template("error.html", error="You can't use this email, choose another one")

    if 'file' in request.files:
        avatar = request.files['file']
        if avatar:
            filename = f"{str(uuid.uuid4())}.jpg"
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = "default.jpg"
    else:
        filename = "default.jpg"

    if not any([email, password, name, surname]):
        return render_template("error.html", error="Data for registration is not full")

    token = str(uuid.uuid4())
    new_user = User(name=name, surname=surname, password=password_hash, email=email, token=token, avatar_uuid=filename)
    session.add(new_user)
    session.commit()

    resp = make_response(redirect("/profile"))
    resp.set_cookie("token", token)
    return resp


@app.route("/auth", methods=['POST'])
def auth():
    data = request.form
    email = data.get("email")
    password = data.get("password")
    password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
    if not email or not password:
        return render_template("error.html", error="Email or Password is absent")

    result = session.query(User).where(User.email == email, User.password == password_hash).all()

    if not result:
        return render_template("error.html", error="Invalid Email or Password")
    else:
        resp = make_response(redirect("/profile"))
        resp.set_cookie("token", result[0].token)
        return resp


@app.route("/logout")
def logout():
    resp = make_response(redirect("/login"))
    resp.set_cookie("token", "")
    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
