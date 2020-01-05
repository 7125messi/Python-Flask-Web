import os
import pandas as pd
import dill as pickle
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def apicall():
	"""API Call
	
	Pandas dataframe 从API Call
	"""
	try:
		test_json = request.get_json()
		test = pd.read_json(test_json, orient='records')

		#To resolve the issue of TypeError: Cannot compare types 'ndarray(dtype=int64)' and 'str'
		test['Dependents'] = [str(x) for x in list(test['Dependents'])]

		loan_ids = test['Loan_ID']

	except Exception as e:
		raise e
	
	clf = 'model_v2.pk'
	
	if test.empty:
		return(bad_request())
	else:
		# 加载训练好的模型
		print("Loading the model...")
		loaded_model = None
		with open('./models/'+clf,'rb') as f:
			loaded_model = pickle.load(f)

		print("模型已经加载完毕，开始预测......")
		predictions = loaded_model.predict(test) # 模型预测结果

		# 将预测结果与测试集做比较
		prediction_series = list(pd.Series(predictions))
		final_predictions = pd.DataFrame(list(zip(loan_ids, prediction_series)))

		responses = jsonify(predictions=final_predictions.to_json(orient="records"))
		responses.status_code = 200

		return (responses)


@app.errorhandler(400)
def bad_request(error=None):
	message = {
			'status': 400,
			'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
	}
	resp = jsonify(message)
	resp.status_code = 400

	return resp

if __name__ == '__main__':
	app.run()
