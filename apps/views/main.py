from flask import Blueprint,render_template,flash,redirect,url_for
from apps.models import Posts
from apps.forms import PostsForm
from flask_login import login_required,current_user
from apps.exts import db
main = Blueprint("main",__name__)



@main.route('/',methods=['GET','POST'])
# @login_required
def index():
    form = PostsForm()
    if form.validate():
        #判断是否登录了
        if current_user.is_authenticated:
            #获取当前登录的用户
            u = current_user._get_current_object()
            p = Posts(content=form.content.data,author=u)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('登录以后才可以发表')
            return redirect(url_for('users.login'))

    #读取所有的博客
    posts = Posts.query.filter_by(rid=0).all()
    return render_template('main/index.html',form=form,posts=posts)