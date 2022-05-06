import os
import pandas as pd
import pickle
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann

#loading model
model = pickle.load(open('/home/pietro/Documents/MyJourneyDS/ComunidadeDS/DSemProducao/my-codes/model/model_rossmann.pkl', 'rb'))

#inicialize API
app = Flask(__name__)

@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()
    
    if test_json: #there is data
        if isinstance(test_json, dict): #Unique example
            test_raw = pd.DataFrame(test_json, index= [0])
        
        else: #Multiple example
            test_raw = pd.DataFrame(test_json, columns= test_json[0].keys())
            
        #Instantiate Rossmann Class
        pipeline = Rossmann()
        
        #data cleaning
        dataframe = pipeline.data_cleaning(test_raw)
        
        #feature engineering
        dataframe_2 = pipeline.feature_engineering(dataframe)
        
        #data_preparation
        dataframe_3 = pipeline.data_preparation(dataframe_2)
        
        #prediction
        df_response = pipeline.get_prediction(model, test_raw, dataframe_3)
        
        
        return df_response
        
    else:
        return Response('{}', status= 200, mimetype= 'application/json')

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port= port)
