"""
模型部署

现在我们已经设置好了环境，也训练了深度学习模型，接下来可以使用 Flask 来生产 Keras 模型。
用于模型预测的完整代码如下所示。代码的整体结构与前面的代码示例相同，

但主要区别在于定义预测函数之前先加载模型，并在预测函数中使用模型。
要想重新加载模型，我们需要使用 custom_objects 参数将自定义度量函数作为输入参数传递给 load_model。

使用 tf.get_default_graph（）为 TensorFlow 计算图设置一个引用同样必要。
如果忽略了这一步，在预测步骤期间可能会发生异常。
条件 with graph.as_default（）用于在进行预测时获取计算图的线程安全引用。
在预测函数中，请求参数被转换为 DataFrame，然后传递给 Keras 模型以进行预测。
可以通过运行 python3 Flask_Deploy.py 来部署 Flask 应用程序。
也可以像前面一样连接到应用程序，但是需要指定属性 G1 到 G10 的值。这里使用浏览器测试端点，会得到以下结果：

# 浏览器
http://127.0.0.1:5000/predict?g1=1&g2=0&g3=0&g4=0&g5=0&g6=0&g7=0&g8=0&g9=0&g10=0
# 响应
{
 "prediction":"0.04930059",
 "success":true}
}
"""

# 加载库
import flask
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model

# 实例化 flask
app = flask.Flask(__name__)

# 我们需要重新定义我们的度量函数，
# 从而在加载模型时使用它
def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    keras.backend.get_session().run(tf.local_variables_initializer())
    return auc

# 加载模型，传入自定义度量函数
global graph
graph = tf.get_default_graph()
model = load_model('games.h5', custom_objects={'auc': auc})

# 将预测函数定义为一个端点
@app.route("/predict", methods=["GET","POST"])
def predict():

    data = {"success": False}

    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # 若发现参数，则返回预测值
    if (params != None):
        x=pd.DataFrame.from_dict(params, orient='index').transpose()
        with graph.as_default():
            data["prediction"] = str(model.predict(x)[0][0])
            data["success"] = True

    # 返回Jason格式的响应
    return flask.jsonify(data)

if __name__ == '__main__':
    # 启动Flask应用程序，允许远程连接
    app.run()
