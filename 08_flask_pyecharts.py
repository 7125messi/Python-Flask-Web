import json

from flask import Flask
from flask import request
from flask import render_template
from pyecharts.charts import Bar

import db
from jinja2 import Markup

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

# 增加动态数据处理
# 展现表单提交页面
@app.route("/show_add_user")
def show_add_user():
    return render_template("show_add_user.html")

# 进行提交user表单的处理
@app.route("/do_add_user",methods=["GET","POST"])
def do_add_user():
    print(request.form)

    name = request.form.get("name")
    sex = request.form.get("sex")
    age = request.form.get("age")
    email = request.form.get("email")

    # python3.6+ format字符串方法,age是数字，其他都是字符
    sql = f"""
        insert into user (name,sex,age,email) 
        values ('{name}','{sex}',{age},'{email}');
    """
    print(sql)
    db.insert_or_update_data(sql)
    return "success"

@app.route("/show_users")
def show_users():
    sql = """
    select id,name from user;
    """
    datas = db.query_data(sql)
    return render_template("show_users.html",datas=datas)

@app.route("/show_user/<user_id>")
def show_user(user_id):
    sql = f"""
        select * from user 
        where id = {user_id};
        """
    datas = db.query_data(sql)
    user = datas[0]
    return render_template("show_user.html",user=user)

@app.route("/show_echarts_3")
def show_echarts_3():
    xdatas = ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
    ydatas = [5, 20, 36, 10, 10, 20]
    return render_template("show_echarts_3.html",
                           xdatas=Markup(json.dumps(xdatas)), # Markup 不要转义
                           ydatas=json.dumps(ydatas))

@app.route("/show_pyecharts")
def show_pyecharts():
    bar = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    )
    return render_template("show_pyecharts.html",
                           bar_options = bar.dump_options())

if __name__ == '__main__':
    app.run()
