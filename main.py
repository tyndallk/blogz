from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    posted = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.posted = False


# @app.route('/', methods=['POST', 'GET'])
# def index():
#      return render_template('blog.html',title="Get It Done!")




@app.route('/blog', methods = ['GET', 'POST'])
def blogs():
    blog_id = request.form['blog-id']
    blog = Blog.query.get['blog_id']
    blog.posted = True
    posted_blog = Blog.query.filter_by(posted=True).all()
    
    return render_template('blog.html',title="Build a Blog", posted_blog=posted_blog)



@app.route('/newpost', methods=['GET', 'POST'])
def add_newpost():
    if request.method == 'POST':
         post_title = request.form['title']
         db.session.add(title)
         db.session.commit()
         post_body = request.form['body']
         db.session.add(body)
         db.session.commit()

    return render_template('newpost.html', title = 'Add a Blog Entry!')



if __name__ == '__main__':
    app.run()