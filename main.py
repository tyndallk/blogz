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

        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = new_blog.id
        
        return redirect ("/blog?id=" + str(blog_id))

    return render_template('newpost.html', title = 'Add a Blog Entry!')
            

@app.route('/blog', methods = ['GET', 'POST'])
def blogs():
    blog_id = request.args.get('id')
     
    if blog_id is not None:
        blog = Blog.query.get(int(blog_id))
        return render_template('individual_blog.html', blog=blog)

    all_blogs = Blog.query.all()
    return render_template('blog.html',title="Build a Blog", all_blogs=all_blogs)


if __name__ == '__main__':
    app.run()