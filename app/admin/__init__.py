from flask import Blueprint,render_template,request,url_for,redirect
from app.model import Post
from app.form import PostForm
from flask.ext.login import login_required
import nanotime
from app.config import  *
admin = Blueprint("admin",__name__,static_folder="../static",template_folder="../templates",url_prefix="/admin")

@admin.route("/")
@login_required
def index():
    post = {}
    count = 0
    for i in Post.objects():
        post[str(count)] = {
            "id": i.postid,
            "time": i.time ,
            "title": i.title ,
            "content": i.content ,
            "tag": i.tag ,
        }
        count = count + 1
    pages = [ post[page]  for page in post]
    return render_template("admin/admin.html",pages=pages)


@admin.route("/editpassage")
@admin.route("/editpassage/<string:postid>/")
@login_required
def editpassage(postid=None):
    form = PostForm()

    if postid == None:
        return render_template("admin/edit.html",form=form,tags=TAG)
    post = {}

    info = Post.objects(postid=postid).first()

    post = {
        "id":info.postid,
        "time": info.time ,
        "title": info.title ,
        "content": info.content ,
        "tag": info.tag ,
    }


    return render_template("admin/edit.html",page=post,tags=TAG,form=form)



@admin.route("/changePost",methods=["POST"])
@login_required
def changePost():
    try:
        content = request.form.get('content')
        title   = request.form.get('title')
        tag     = request.form.get('tag')
        status  = request.form.get('status')
        count = Post.objects().count()
        count = str(count+1)
        time = str(nanotime.now())
        time = time[:10]


        if request.form.get('pid'):
            pid = request.form.get('pid')
            Post.objects(postid=str(pid)).update_one(set__title=title)
            Post.objects(postid=str(pid)).update_one(set__content=content)
            Post.objects(postid=str(pid)).update_one(set__status=status)
            Post.objects(postid=str(pid)).update_one(set__tag=tag)
            return redirect("/admin")

        else:
            page = Post.objects.create()
            Post.objects(id=page.id).update_one(
                postid=count ,
                title=title ,
                content=content ,
                tag=tag ,
                time=time ,
                status=status ,
            )
            return redirect("/admin")
    except Exception,e:
        return str(e)




@admin.route("/deletepassage/<string:postid>/")
@login_required
def deletepassage(postid):
    Post.objects(postid=postid).delete()
    return redirect("/admin")




