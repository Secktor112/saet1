from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from models import Article, User
from flask import render_template, flash, url_for
from flask import redirect
from flask import request
from app import app
from app import db


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/catalog')
def catalog():
    return render_template("catalog.html")


@app.route('/service')
def service():
    return render_template("service.html")


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    login = request.form.get('login')
    password = request.form.get('psw')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page)
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('auth.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    login = request.form.get('login')
    password = request.form.get('psw')
    password2 = request.form.get('psw2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        elif not (password or password2):
            flash('Please, fill all fields!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect('/auth')

    return render_template('register.html')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = Article.query.get_or_404(id)
    article.delete()
    if article.success:
        return redirect('/posts')
    return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.update(
            request.form['title'],
            request.form['intro'],
            request.form['text']
        )

        if article.success:
            return redirect('/posts')
        return "При редактировании статьи произошла ошибка"

    else:
        return render_template("post-update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
@login_required
def create_article():
    if request.method == "POST":
        article = Article(
            title=request.form['title'],
            intro=request.form['intro'],
            text=request.form['text']
        )

        article.create()

        if article.success:
            return redirect('/posts')
        return "При добавлении статьи произошла ошибка"

    else:
        return render_template("create-article.html")


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('auth') + '?next=' + request.url)

    return response