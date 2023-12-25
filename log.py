from flask import Flask, request, render_template, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Login.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    # Define a Flask-WTF form class
class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=3)])
    password = PasswordField('Password', [validators.Length(min=3)])

class RegistrationForm(FlaskForm):
    dusername = StringField('DUsername', [validators.Length(min=4)])
    dpassword = PasswordField('DPassword', [validators.Length(min=4)])
    email = StringField('EmailUser', [validators.Email()])

@app.route('/loggedIn')
def logged_in():
    return render_template("loggedIn.html")

@app.route("/")
def homepage():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    return render_template("index.html", login_form=login_form, registration_form=registration_form)

@app.route("/login", methods=["POST"])
def check_login():
    print("Login Request Data:", request.form)
    UN = request.form['Username']
    entered_password = request.form['Password']

    user = User.query.filter_by(username=UN).first()

    if user and check_password_hash(user.password, entered_password):
        # Redirect to the 'loggedIn' route if login is successful
        print("Login successful. Redirecting to '/loggedIn'")
        return redirect("/loggedIn")
    else:
        print("Login failed. Redirecting to '/'")
        return redirect("/")


@app.route('/', methods=['GET', 'POST'])
def register_page():
    try:
        if request.method == "POST":
            dUN = request.form['DUsername']
            dPW = generate_password_hash(request.form['DPassword'], method='pbkdf2:sha256')
            Uemail = request.form['EmailUser']

            new_user = User(username=dUN, password=dPW, email=Uemail)
            db.session.add(new_user)
            db.session.commit()

            return redirect("/")

        return render_template("index.html")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return "Internal Server Error", 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run()
