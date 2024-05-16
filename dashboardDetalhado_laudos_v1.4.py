import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Carregar os dados do Excel
file_path = "laudos_SO_sharepoint_16052024.xlsx"
df = pd.read_excel(file_path)

# Definir título do aplicativo
st.title("(SO - TED INCRA/UFPR) - Laudos de Supervisão Ocupacional ")

# Definir título da tabela com informações gerais sobre os laudos
st.subheader("Relação de laudos (pesquisar nomes com underline)")

# Lista de todos os técnicos, assentamentos, tipos de laudo e municípios
tecnicos = ['Todos'] + list(df['Técnico'].unique())
assentamentos = ['Todos'] + list(df['Assentamento'].unique())
tipos_de_laudo = ['Todos'] + list(df['Tipo de Laudo'].unique())
municipios = ['Todos'] + list(df['Município'].unique())
modalidade = ['Todos'] + list(df['Modalidade'].unique())

# Data inicial padrão: 01/01/2022
start_date = datetime(2022, 1, 1).date()

# Data final padrão: dia atual
end_date = datetime.now().date()

# Filtrar por técnico
selected_tecnico = st.sidebar.selectbox("Selecione um técnico:", tecnicos)
if selected_tecnico != "Todos":
    df = df[df['Técnico'] == selected_tecnico]

# Filtrar por município
selected_municipio = st.sidebar.selectbox("Selecione um município:", municipios)
if selected_municipio != "Todos":
    df = df[df['Município'] == selected_municipio]

# Filtrar por assentamento
selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos)
if selected_assentamento != "Todos":
    df = df[df['Assentamento'] == selected_assentamento]

# Filtrar por tipo de laudo
selected_tipo_laudo = st.sidebar.selectbox("Selecione um tipo de laudo:", tipos_de_laudo)
if selected_tipo_laudo != "Todos":
    df = df[df['Tipo de Laudo'] == selected_tipo_laudo]

# Filtrar por modalidade
selected_modalidade = st.sidebar.selectbox("Selecione uma modalidade:", modalidade)
if selected_modalidade != "Todos":
    df = df[df['Modalidade'] == selected_modalidade]

# Filtrar por data
start_date = st.sidebar.date_input("Data inicial:", start_date)
end_date = st.sidebar.date_input("Data final:", end_date)
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date
df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]

# Exibir tabela interativa
st.write(df)

# Exibir gráfico interativo
st.subheader("Gráfico de barras - tipo de laudo")
chart_data = df['Tipo de Laudo'].value_counts()
st.bar_chart(chart_data)

# Gráfico de pizza
st.subheader("Gráfico de pizza - tipo de laudo")
pie_chart_data = df['Tipo de Laudo'].value_counts()
fig = px.pie(names=pie_chart_data.index, values=pie_chart_data.values, title='Distribuição dos Laudos')
st.plotly_chart(fig)

# Calcular o total de laudos para cada tipo de laudo
total_por_tipo_laudo = df['Tipo de Laudo'].value_counts()

# Calcular o total de laudos
total_de_laudos = total_por_tipo_laudo.sum()

# Adicionar o total de laudos ao DataFrame
total_por_tipo_laudo = total_por_tipo_laudo.reset_index()
total_por_tipo_laudo.columns = ['Tipo de Laudo', 'Quantidade de Laudos']
total_por_tipo_laudo.loc[len(total_por_tipo_laudo)] = ['Total', total_de_laudos]

# Exibir quadro com os totais
st.subheader("Quantidade de laudos por tipo")
st.write(total_por_tipo_laudo)
