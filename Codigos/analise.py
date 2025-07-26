import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
from matplotlib import cm
import seaborn as sns
import time
from matplotlib.patches import Patch
import math
os.system("cls")
#ANALISES
# 
#print(df.describe())

#EVASÃO 
def fazer_grafico_evasao(dados: pd.DataFrame):
    labels = {True:"True",False:"False"}
    counter:Counter = Counter(dados["Churn"].map(labels))
    print(df.columns)



    total = sum(counter.values())
    labels = list(counter.keys())
    valores = list(counter.values())


    plt.figure(figsize=(6, 5))
    #Distribuição de evasão de Clientes
    plt.title("Customer churn distribution")
    plt.bar(labels, valores, color=["deepskyblue","red"])
    plt.ylabel("Number of Customers")
    plt.xlabel("Churn")

    # Adiciona o valor e a porcentagem acima das barras
    for i, (label, valor) in enumerate(zip(labels, valores)):
        porcentagem = f"{(valor / total) * 100:.1f}%"
        plt.text(i,  valor * 0.5, f"{porcentagem}", ha='center', va='center', fontsize=15)
        plt.text(i,  valor + total * 0.02, f"({valor})", ha='center', va='center', fontsize=10)


    plt.tight_layout()
    outputplots = "OUTPUT/PLOTS"
    os.makedirs(outputplots,exist_ok=True)
    plt.savefig(f"{outputplots}/evasao_distribuicao.png")

# 28% cancelam o contrato

#Antes de fazer as comparações de evasão com categorias, vou ver a correlação entre as tabelas
def converter_para_dataframe_numerico(dados: pd.DataFrame):
    dados = dados.drop(columns=["customerID"])
    df_numerico: pd.DataFrame = pd.get_dummies(dados) # Converter tudo para valores numerico/booleanos. para calcular a correlação
    # drop_first=True é para boa pratica k-1. mas já removi o id
    df_numerico.to_csv("OUTPUT/dados_apenas_numeros.csv",sep=",",decimal=".",index=False)
    from dython.nominal import associations
    dic=associations(dados,figsize=(20,20),mark_columns=True,title="Matriz de Correlação",plot=False)
    ax = dic["ax"]
    

    fig = ax.get_figure()
    os.makedirs("OUTPUT/PLOTS",exist_ok=True)
    fig.savefig("OUTPUT/PLOTS/correlacao_dython.png", dpi=100, bbox_inches="tight")
    plt.close()
    corr = dic["corr"]

    corr.to_csv("OUTPUT/dython_corr_matrix.csv",sep=",",decimal=".",index=False)

def calcular_correlação(df_num: pd.DataFrame, limite: float =  0.3) -> list[str]:
    df_corr = df_num.corr(numeric_only=True)["Churn"].sort_values(ascending=False)
    df_corr = df_corr[abs(df_corr) > 0.1] # Filtrar 
    df_corr = df_corr[1:]
    
    plt.figure(figsize=(15, 10))
    ax = sns.barplot(x=df_corr.values, y=df_corr.index,  hue=df_corr.values, palette="vlag")
    plt.title("Correlação com a Evasão (Churn)")
    plt.ylabel("")
    plt.xlabel("Nivel de Correlação")

    for i, p in enumerate(ax.patches):
        width = p.get_width()
        if abs(width) != 0: 
            ax.text((width *0.5), p.get_y() + p.get_height() / 2,
                        f"{width:.2f}", va="center")
    legenda = [
        Patch(color="#a35455", label="Correlação positiva: mais chance de evasão"),
        Patch(color="#4d76ac", label="Correlação negativa: menos chance de evasão") 
    ]
    plt.legend(handles=legenda, loc="lower right")
    plt.tight_layout()
    #plt.show()
    plt.savefig("OUTPUT/PLOTS/correlacao_evasao")
    plt.close()
    correlacao_postiva = df_corr[df_corr > limite].index.tolist()
    colunas_fortes = df_corr[abs(df_corr) > limite].index.tolist()

    return correlacao_postiva,colunas_fortes

def graficos_categorias(dados: pd.DataFrame,colunas_categorias: list[str], coluna_target: str="Churn",filename: str = "categories_"):
    colunas_categorias
    output ="OUTPUT/PLOTS/CATEGORIAS/"
    n = len(colunas_categorias)
    rows = math.ceil(n / 3)
    
    plt.figure(figsize=(25, 5 * rows))
    for i,categoria in enumerate(colunas_categorias):
        plt.subplot((rows),3,i+1)
        contador = Counter(dados[categoria])
    
        #print(f"{categoria}: {contador.values()},{contador.keys()}")
        
        ax = sns.countplot(data = dados, 
                        x = categoria, 
                        hue = coluna_target,
                        palette = {"deepskyblue", "red"}
                        )

  
        ax.set_title(f"Churn per {categoria}") 
        ax.set_ylabel('Clientes') 
        ax.set_xlabel(f"Groups of {categoria}") 
        

        total = dados[categoria].count()
        

   


        for p in ax.patches:
            
            if abs(p.get_x()) !=0:
                height = p.get_height()
                width = p.get_width()

                ax.text(p.get_x()+width/2.0, height * 0.5, s=f"{height:.1f}\n{(height/total)*100:.1f}%",  ha='center')



   

    plt.tight_layout()

    os.makedirs(output,exist_ok=True)
    plt.savefig(f"{output}{filename}.png")
    plt.close()

def graficos_boxplot(dados: pd.DataFrame):
    colunas_numericas=["account_Charges_Monthly","account_Charges_Total","account_Charges_Daily","customer_tenure"] # Numericos

    plt.figure(figsize=(10,10))
    for i,coluna in enumerate(colunas_numericas):
        plt.subplot(2,2,i+1)
        ax = sns.boxplot(data=dados,x="Churn",y=coluna,legend=False,hue="Churn", palette = {'deepskyblue', 'red'})

        ax.set_title(f"Churn per {coluna}")
        ax.set_xlabel("Churn state")
    plt.tight_layout()
    os.makedirs("OUTPUT/PLOTS/",exist_ok=True)
    plt.savefig("OUTPUT/PLOTS/box_plot.png")
    plt.close()

def tempo_contrato_evasao(dados: pd.DataFrame):
 
    ax =sns.displot(data=dados, x="customer_tenure", col="Churn",hue="Churn",palette = {'deepskyblue', 'red'},aspect=1.5)
    ax.set_ylabels("Clients")
    ax.set_xlabels("Service Time (Month's)")
    #ax.set_titles("Distribution of Service Time by Churn")
     
    counter:Counter = Counter(dados["Churn"])
    total = sum(counter.values())
    for ax in ax.axes.ravel():
    

        for c in ax.containers:

  
            labels = [f'{w:0.1f}%' if (w := v.get_height()/total*100) > 0 else '' for v in c]

            ax.bar_label(c, labels=labels, label_type='edge', padding=2)
        ax.margins(y=0.2)
    #plt.title("Distribution of Service Time by Churn")
    outputplot = "OUTPUT/"
    os.makedirs(outputplot,exist_ok=True)
    plt.savefig(f"{outputplot}/evasao_distribuicao_tempo_contrato.png")
    plt.close()

if __name__ == "__main__":

    start_time = time.time()
    df = pd.read_csv("./OUTPUT/dados_limpos.csv",sep=",",decimal=".",index_col=False)
    converter_para_dataframe_numerico(df)
    df_numerico = pd.read_csv("./OUTPUT/dados_apenas_numeros.csv",sep=",",decimal=".",index_col=False)

    
    correlacao_fraca=['account_Contract_Month-to-month', 'internet_InternetService_Fiber optic', 'account_PaymentMethod_Electronic check', 'internet_InternetService_No', 'internet_DeviceProtection', 'internet_OnlineBackup', 'account_Contract_Two year', 'internet_TechSupport', 'internet_OnlineSecurity']
    correlacao_fraca2=['account_PaymentMethod','internet_InternetService','account_PaymentMethod','internet_OnlineSecurity','internet_StreamingMovies','phone_MultipleLines']
    colunas_a= ['customer_gender', 'customer_SeniorCitizen',     
        'customer_Partner', 'customer_Dependents',
        'phone_PhoneService', 'phone_MultipleLines', 'internet_InternetService',
        'internet_OnlineSecurity', 'internet_OnlineBackup',
        'internet_DeviceProtection', 'internet_TechSupport',
        'internet_StreamingTV', 'internet_StreamingMovies', 'account_Contract', 
        'account_PaperlessBilling', 'account_PaymentMethod']
    
    if False:

        correlacao_postiva,colunas_fortes = calcular_correlação(df_numerico,0.2)


        graficos_categorias(df_numerico,correlacao_postiva,filename="correlacao_postiva")
        graficos_categorias(df_numerico,colunas_fortes,filename="colunas_fortes")


        graficos_boxplot(df)
        tempo_contrato_evasao(df)


    fazer_grafico_evasao(df)