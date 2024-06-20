import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Carregar os dados do Excel
file_path = "laudos_SO_sharepoint_20062024.xlsx"
df = pd.read_excel(file_path)

# Definir título do aplicativo
st.title("(SO - TED INCRA/UFPR) - Laudos de Supervisão Ocupacional ")

# Definir título da tabela com informações gerais sobre os laudos
st.subheader("Relação de laudos")

# Função para filtrar opções com base na seleção de um filtro específico
def filter_options(selected_filter, column_name):
    options = ['Todos'] + sorted(list(df[column_name].unique()))
    if selected_filter != "Todos":
        options = [selected_filter] + [x for x in options if x != selected_filter]
    return options

# Ordenar opções de pesquisa
tecnicos = filter_options(st.sidebar.selectbox("Selecione um técnico:", ['Todos'] + sorted(list(df['Técnico'].unique()))), 'Técnico')
assentamentos = filter_options(st.sidebar.selectbox("Selecione um assentamento:", ['Todos'] + sorted(list(df['Assentamento'].unique()))), 'Assentamento')
tipos_de_laudo = filter_options(st.sidebar.selectbox("Selecione um tipo de laudo:", ['Todos'] + sorted(list(df['Tipo de Laudo'].unique()))), 'Tipo de Laudo')
municipios = filter_options(st.sidebar.selectbox("Selecione um município:", ['Todos'] + sorted(list(df['Município'].unique()))), 'Município')
modalidade = filter_options(st.sidebar.selectbox("Selecione uma modalidade:", ['Todos'] + sorted(list(df['Modalidade'].unique()))), 'Modalidade')

# Data inicial padrão: 01/01/2022
start_date = datetime(2022, 1, 1).date()

# Data final padrão: dia atual
end_date = datetime.now().date()

# Filtros laterais
selected_tecnico = st.sidebar.selectbox("Selecione um técnico:", tecnicos)
selected_municipio = st.sidebar.selectbox("Selecione um município:", municipios)
selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos)
selected_tipo_laudo = st.sidebar.selectbox("Selecione um tipo de laudo:", tipos_de_laudo)
selected_modalidade = st.sidebar.selectbox("Selecione uma modalidade:", modalidade)

# Filtrar por técnico
if selected_tecnico != "Todos":
    df = df[df['Técnico'] == selected_tecnico]

# Filtrar por município
if selected_municipio != "Todos":
    df = df[df['Município'] == selected_municipio]

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
start_date = st.sidebar.date_input("Data inicial:", start_date)
end_date = st.sidebar.date_input("Data final:", end_date)
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date
df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]

# Atualizar opções dos filtros com base no DataFrame filtrado
tecnicos = filter_options(selected_tecnico, 'Técnico')
municipios = filter_options(selected_municipio, 'Município')
assentamentos = filter_options(selected_assentamento, 'Assentamento')
tipos_de_laudo = filter_options(selected_tipo_laudo, 'Tipo de Laudo')
modalidade = filter_options(selected_modalidade, 'Modalidade')

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
