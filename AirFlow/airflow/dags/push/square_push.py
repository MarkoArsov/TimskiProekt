import pandas as pd
import requests
import numpy as np

def push_square(**kwargs):
    ti = kwargs['ti']
    cleaned_data = ti.xcom_pull(task_ids='clean_square', key='cleaned_data')

    df = pd.DataFrame.from_dict(cleaned_data)
    df = df.replace({np.nan: None})

    api_url = 'http://flask-api:5000/api/property'

    data_to_send = df.to_dict(orient='records')
   
    try:
        response = requests.post(api_url, json=data_to_send)
       
        if response.status_code == 201:
            print("Successfully sent all property data.")
        else:
            print(f"Failed to send data. Status Code: {response.status_code}, Response: {response.text}")
            
    except Exception as e:
        print(f"Error occurred while sending data: {e}")



