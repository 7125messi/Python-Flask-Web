import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

def read_pvuv_data():
    """
    read pv uv data
    :return:list,ele = (date,pv,uv)
    """
    data = []
    with open('./data/pvuv.txt') as fo:
        linenum = 0
        for row in fo:
            if linenum == 0:
                linenum += 1
                continue
            date, pv, uv = row.strip().split("\t")
            data.append((date, pv, uv))
    return data

@app.route('/getjson')
def getjson():
    # read file
    data = read_pvuv_data()

    # return json
    return json.dumps(data)

if __name__ == '__main__':
    app.run()
