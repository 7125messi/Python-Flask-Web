"""
模型训练

我们使用简单的网络结构创建一个二元分类器。
模型的输入是特征数组，描述了用户先前玩过哪些游戏，模型的输出是玩家将来玩特定游戏的概率。
关于模型训练的信息这里暂且不表我们的重点是部署模型。

上述代码片段定义了自定义度量函数，该函数用于训练模型对 ROC AUC 指标进行优化。
此代码的主要附加功能是最后一步，它将模型序列化为 H5 格式。
我们稍后可以在 Flask 应用程序中加载此模型以提供模型预测。
可以通过运行生成 games.h5 的 python3 Flask_Train.py 来训练模型。
"""

# 导入panda，keras 和tensorflow
import pandas as pd
import tensorflow as tf
import keras
from keras import models, layers

# 加载样本数据集，划分为x和y DataFrame
df = pd.read_csv("https://github.com/bgweber/Twitch/raw/master/Recommendations/games-expand.csv")
x = df.drop(['label'], axis=1)
y = df['label']

# 定义Keras模型
model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10,)))
model.add(layers.Dropout(0.1))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.1))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

# 使用自定义度量函数
def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    keras.backend.get_session().run(tf.local_variables_initializer())
    return auc

# 编译并拟合模型
model.compile(
    optimizer='rmsprop',
    loss='binary_crossentropy',
    metrics=[auc]
)

history = model.fit(
    x,
    y,
    epochs=100,
    batch_size=100,
    validation_split = .2,
    verbose=0
)

# 以H5格式保存模型
model.save("games.h5")
