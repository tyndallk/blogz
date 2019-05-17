from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']   
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()

        username_error = ''
        password_error = ''
        verify_error = ''

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect ('/newpost')
        else:
            
            if username == '' or len(username) < 3:
                username_error = "Invalid Username."

            if existing_user:
                username_error = " User already exists."
        
            if password == '' or len(password) < 3:
                password_error = "Invalid Password."
        
            if verify == '' or verify != password or len(verify) < 3:
                verify_error = "Passwords do not match."

            return render_template('signup.html', username_error=username_error,
            password_error=password_error, verify_error = verify_error)
    
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        user_error = ''
        password_error = ''
        
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            if not user:
                user_error = 'Username does not exist'
            
            if user and not user.password == password:
                password_error = ('Invalid password')

            return render_template('login.html', user_error = user_error, password_error = password_error)
    
    return render_template('login.html')



@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')



@app.route('/newpost', methods=['GET', 'POST'])
def add_newpost():

    owner = User.query.filter_by(username=session['username']).first()


    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        title_error = ''
        body_error = ''

        if title == '' and body == '':
            title_error = "Please fill out a title"
            title = ''
            body_error = "Please fill out a body"
            body = ''
            return render_template('newpost.html', title_error=title_error,
            body_error=body_error)

        if title == '' and not body == '':
            title_error = "Please fill out the title."
            title = ''
            return render_template('newpost.html', title_error=title_error)

        if not title == '' and body == '':
            body_error = "Please fill out the body."
            body = ''
            return render_template('newpost.html', body_error=body_error)

        new_blog = Blog(title, body, owner)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = new_blog.id
        
        return redirect ("/blog?id=" + str(blog_id))

    return render_template('newpost.html', title = 'Add a Blog Entry!')
            

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    user_id = request.args.get('user')

    if blog_id:
        #show this blog
        blog = Blog.query.get(int(blog_id))
        return render_template('individual_blog.html', blog=blog)
    elif user_id:
        #show all posts for this user
        owner = User.query.get(int(user_id))
        all_blogs = Blog.query.filter_by(owner=owner).all()
        return render_template('blog.html', all_blogs=all_blogs)
    else:
        #show all blogs
        all_blogs = Blog.query.all()
        return render_template('blog.html',title="Build a Blog", all_blogs=all_blogs)

@app.route('/', methods = ['GET', 'POST'])
def index():

    if request.method == 'GET':
        all_users = User.query.all()
        return render_template('index.html', title = "Blog Users!", all_users=all_users)
    


if __name__ == '__main__':
    app.run()