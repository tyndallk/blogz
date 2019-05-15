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

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/newpost', methods=['GET', 'POST'])
def add_newpost():
    if request.method == 'POST':
         title = request.form['title']
         body = request.form['body']
         new_blog = Blog(title, body)
         db.session.add(new_blog)
         db.session.commit()
         new_blog = new_blog.id
         #return redirect ('/blog?id=new_blog')
    

    return render_template('newpost.html', title = 'Add a Blog Entry!')


@app.route('/blog', methods = ['GET', 'POST'])
def blogs():
    new_blog = new_blog.id
    return render_template('blog.html',title="Build a Blog", new_blog=new_blog)




if __name__ == '__main__':
    app.run()