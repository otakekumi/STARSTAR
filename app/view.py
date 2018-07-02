from app import app
from flask import render_template,request,redirect,url_for
from flask.ext.cache import Cache
from form import LoginForm
import mistune
from model import User,Post,Admin,CommentForm
from flask.ext.login import LoginManager,login_required,login_user,logout_user
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension



cache = Cache()
config = {
    "CACHE_TYPE":"redis",
    "CACHE_REDIS_HOST":"127.0.0.1",
    "CACHE_REDIS_PORT":"6379",
    "CACHE_REDIS_DB":"",
    "CACHE_REDIS_PASSWORD":""
}



DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION   = ".md"
app.config.from_object(__name__)

# cache.init_app(app)

# Login Manager

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Unauthorized User.Please Login First!"
login_manager.login_message_category = "info"

#session["login"] = False

exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']
# Home page
@app.route("/")
# @cache.cached(timeout=60)
def index():
    post = {}
    count = 0
    try:

        cc = Post.objects(status="post")
        for i in cc:
            post[str(count)] = {
                "id": i.postid ,
                "time": i.time ,
                "title": i.title ,
                "content": i.content ,
                "tag": i.tag ,
            }
            count = count + 1
        pages = [post[page] for page in post]
        return render_template("Home.html" , pages=pages)
    except Exception,e:
        return str(e)

# Get the passage content
@app.route("/archive/<string:postid>/")
def archive(postid):
    info = Post.objects(postid=postid).first()
    page = {
        "id": postid,
        "title": info.title,
        "time": info.time,
        "content": markdown.markdown(info.content,exts),
        "tag": info.tag
    }
    form = CommentForm()
    return render_template("archive.html" , page=page,form=form)



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tags/<string:tag>")
def tags(tag):
    try:
        if tag != "all":

            count = 0
            post = {}
            page = Post.objects(tag=tag)
            for i in page:
                post[str(count)] = {
                    "id": i.postid ,
                    "time": i.time ,
                    "title": i.title ,
                    "content": i.content ,
                    "tag": i.tag ,
                }
                count = count + 1
            pages = [post[page] for page in post]

            return render_template("tag.html" , pages=pages)
        elif tag == "all":
            tags = app.config["TAG"]
            return render_template("tag.html" , tags=tags)
    except Exception,e:
        return str(e)

@app.route("/login")
def login():
    try:
        form = LoginForm()
        return render_template("login.html" , form=form)
    except Exception,e:
        return str(e)

@app.route("/auth",methods=['GET','POST'])
def auth():
    form = LoginForm()
    error = ""
    if request.method == "POST":
        username,password = request.form.get("name"),request.form.get("password")
        if username and password and verify(username,password):
            login_user(User(username))
            return redirect("/admin")

        else:
            error = "Username Or Password Is Invalid."

    return render_template("login.html",form=form,error=error)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@login_manager.user_loader
def load_user(id):
    return User(id)


def verify(username,password):
    passDB = Admin.objects(username=username).first().password
    if password == passDB:
        return True
    else:
        return False

