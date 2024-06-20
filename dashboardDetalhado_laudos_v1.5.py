import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import unicodedata

# Carregar os dados do Excel
file_path = "laudos_SO_sharepoint_20062024.xlsx"
df = pd.read_excel(file_path)

# Definir título do aplicativo
st.title("(SO - TED INCRA/UFPR) - Laudos de Supervisão Ocupacional ")

# Definir título da tabela com informações gerais sobre os laudos
st.subheader("Relação de laudos")

# Função para remover caracteres especiais e normalizar texto
def remove_special_chars(text):
    return ''.join(ch for ch in unicodedata.normalize('NFKD', text) if not unicodedata.combining(ch))

# Ordenar opções de pesquisa
tecnicos = ['Todos'] + sorted(list(df['Técnico'].unique()))
assentamentos = ['Todos'] + sorted(list(df['Assentamento'].unique()))
tipos_de_laudo = ['Todos'] + sorted(list(df['Tipo de Laudo'].unique()))
municipios = ['Todos'] + sorted(list(df['Município'].apply(remove_special_chars).unique()))
modalidade = ['Todos'] + sorted(list(df['Modalidade'].unique()))

# Data inicial padrão: 01/01/2022
start_date = datetime(2022, 1, 1).date()

# Data final padrão: dia atual
end_date = datetime.now().date()

# Filtros laterais
selected_tecnico = st.sidebar.selectbox("Selecione um técnico:", tecnicos, key="tecnico")
selected_municipio = st.sidebar.selectbox("Selecione um município:", municipios, key="municipio")
selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento")
selected_tipo_laudo = st.sidebar.selectbox("Selecione um tipo de laudo:", tipos_de_laudo, key="tipo_laudo")
selected_modalidade = st.sidebar.selectbox("Selecione uma modalidade:", modalidade, key="modalidade")

# Filtrar por técnico
if selected_tecnico != "Todos":
    df = df[df['Técnico'] == selected_tecnico]

# Filtrar por município
if selected_municipio != "Todos":
    df = df[df['Município'].apply(remove_special_chars) == remove_special_chars(selected_municipio)]

# Filtrar por assentamento
if selected_assentamento != "Todos":
    df = df[df['Assentamento'] == selected_assentamento]

# Filtrar por tipo de laudo
if selected_tipo_laudo != "Todos":
    df = df[df['Tipo de Laudo'] == selected_tipo_laudo]

# Filtrar por modalidade
if selected_modalidade != "Todos":
    df = df[df['Modalidade'] == selected_modalidade]

# Filtrar por data
start_date = st.sidebar.date_input("Data inicial:", start_date, key="start_date")
end_date = st.sidebar.date_input("Data final:", end_date, key="end_date")
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date
df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]

# Atualizar opções dos filtros com base no DataFrame filtrado
tecnicos = ['Todos'] + sorted(list(df['Técnico'].unique()))
municipios = ['Todos'] + sorted(list(df['Município'].apply(remove_special_chars).unique()))
assentamentos = ['Todos'] + sorted(list(df['Assentamento'].unique()))
tipos_de_laudo = ['Todos'] + sorted(list(df['Tipo de Laudo'].unique()))
modalidade = ['Todos'] + sorted(list(df['Modalidade'].unique()))

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
