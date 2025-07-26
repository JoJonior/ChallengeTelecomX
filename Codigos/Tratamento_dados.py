import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.system("cls")
# Extracão

# os dois funcionam, porem baixar o json é mais rapido
url_data = "TelecomX_Data.json" 
#url_data = "https://raw.githubusercontent.com/ingridcristh/challenge2-data-science/refs/heads/main/TelecomX_Data.json"

df_json = pd.read_json(url_data)
# 🔧 Transformação
# NORMALIZAR 
df_normalizado = pd.json_normalize(
    df_json.to_dict(orient='records'),  
    sep='_',                            
)

# Str para float
df_normalizado["account_Charges_Total"] = (
    df_normalizado["account_Charges_Total"]
    .astype(str)                 
    .str.strip()                
    .replace("", 0.0)        
    .astype(float)              
)


# Str para boolean

bolean_colums = ['Churn','customer_Partner','customer_Dependents','phone_PhoneService','phone_MultipleLines','internet_OnlineSecurity','internet_OnlineBackup','internet_DeviceProtection','internet_TechSupport','internet_StreamingTV','internet_StreamingMovies','account_PaperlessBilling']

for coluna in bolean_colums:
    df_normalizado[coluna] = (df_normalizado[coluna].astype(str).str.strip().str.lower().map({"yes": True, "no": False})).astype(np.bool)
    #1 ou 0, prefiro trabalhar com booleans, e Counter

df_normalizado["account_Charges_Daily"] =  df_normalizado["account_Charges_Monthly"] / 30

#print(df_normalizado.loc[df_normalizado["Churn"] == True].T)

#CONTAR NULOS
#print(df_normalizado.isna().sum())
os.makedirs("OUTPUT",exist_ok=True)
df_normalizado.to_csv("OUTPUT/dados_limpos.csv",sep=",",decimal=".",index=False)
