import pandas as pd 
import numpy as np 
import plotly.express as px 
import streamlit as st

#função carregar dados
@st.cache_data
def carregar_dados():
    # importando e tratando os dados
    iByte = pd.read_csv('RECLAMEAQUI_IBYTE.csv')
    HapVida = pd.read_csv('reclameaqui_hapvida.csv')
    Nagem = pd.read_csv('reclameaqui_nagem.csv')

    #definindo a empresa
    iByte['EMPRESA'] = 'IBYTE'
    HapVida['EMPRESA'] = 'HAPVIDA'
    Nagem['EMPRESA'] = 'NAGEM'

    #concatenando a base
    df = pd.concat([iByte, HapVida, Nagem], axis = 0)
    df.reset_index(inplace=True, drop=True)

    # tratando o tempo
    df['TEMPO'] = pd.to_datetime(df['TEMPO'])

    # tratando UF
    df['UF'] = [x[1] for x in df['LOCAL'].str.split(' - ')]
    df['UF'] = df['UF'].apply(lambda x: 'PB' if x == 'P' else x)
    df['UF'] = df['UF'].apply(lambda x: 'CE' if x == 'C' else x)

    # contando as palavras
    df['QT_PALAVRA'] = [len(x) for x in df['DESCRICAO'].str.split()]
    return df

with st.container():
    df = carregar_dados()
    
    st.title('Casos do Reclame aqui')
    st.write('---')
    st.subheader('Seleciona uma empresa')
    empresa = st.selectbox(label = ' ', options=list(df['EMPRESA'].unique()))
    
    _,c,_ = st.columns(3)

    if empresa == 'HAPVIDA':
        c.image(r'./img/hapvida.png', width=300,output_format='auto')
    elif empresa == 'IBYTE':
        c.image(r'./img/IBYTE.jpg', width=300,output_format='auto')
    elif empresa == 'NAGEM':
        c.image(r'./img/nagem.webp', width=300,output_format='auto')

    box_ano = st.selectbox(label = 'ANO', options=list(df['ANO'].unique()))
    
df_filtrado = df[df['EMPRESA']==empresa]
df_filtrado = df_filtrado[df_filtrado['ANO'] == box_ano]
st.write('---')
st.write('Quantidade de reclamações por Status')

status = df_filtrado['STATUS'].unique()
if len(status) > 0:
    col = st.columns(len(status))
    for i,sta in enumerate(status):
        coluna = col[i]
        coluna.metric(label = sta, value=len(df_filtrado[df_filtrado['STATUS']==sta]))

st.write('Quantidade de reclamações por Estado')
st.bar_chart(data=df_filtrado['UF'].value_counts())

st.write('Quantidade de reclamações por Tempo')
st.line_chart(data=df_filtrado['TEMPO'].value_counts())

st.write('Quantidade de palavras por Reclamação')
st.metric(label='Méida', value=int(df_filtrado['QT_PALAVRA'].mean()))