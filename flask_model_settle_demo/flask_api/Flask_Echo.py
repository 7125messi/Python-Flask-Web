"""
为了帮大家熟悉 Flask，我们会设置一个简单的函数来回显传入的参数。
下面的代码片段首先实例化 Flask 应用程序，定义函数，然后启动应用程序。
在 Flask 中，app.route 注释用于指定在 Web 上使用函数的位置以及允许的方法。
使用下面的代码，就可以在 5000 / predict 这个位置使用函数。
该函数会检查 request.json 和 request.args 对象的输入参数，
根据函数的调用方式（例如浏览器获取 vs cURL POST）使用这些参数。
如果已将 msg 参数传递给函数，则将其回显到函数返回的 JSON 响应中。

可以用 Web 浏览器或 cURL 调用该函数。
这里在 Windows 环境中使用 cURL，也可以使用 -d '{"msg":"Hello World"}' 。
两种方法的结果相同，来自客户端的 JSON 响应会重复传入的 msg 参数。

# 浏览器
http://127.0.0.1:5000/predict?msg=HelloWorld

# cURL
>curl -X POST -H "Content-Type: application/json" -d "{ \"msg\":
\"Hello World\" }" http://127.0.0.1:5000/predict

# 响应
{
  "response": "HelloWorld",
  "success": true
}

我们现在能够将 Python 函数设置为 Web 端点，下一步是让函数调用训练好的深层网络。
"""

import flask

app = flask.Flask(__name__)

# 将一个预测函数定义为一个端点
@app.route("/predict", methods=["GET","POST"])
def predict():

    data = {"success": False}

    # 获取请求参数
    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # 若获得参数，则回显msg 参数
    if (params != None):
        data["response"] = params.get("msg")
        data["success"] = True

    # 返回一个 json 格式的响应
    return flask.jsonify(data)

if __name__ == '__main__':
    # 开启Flask应用程序，运行远程连接
    app.run()
