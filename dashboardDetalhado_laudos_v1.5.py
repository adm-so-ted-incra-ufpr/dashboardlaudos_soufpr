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
def filter_options(selected_filter, column_name, df):
    options = ['Todos'] + sorted(list(df[column_name].unique()))
    if selected_filter != "Todos":
        options = [selected_filter] + [x for x in options if x != selected_filter]
    return options

# Filtros laterais
with st.sidebar:
    # Ordenar opções de pesquisa
    tecnicos = filter_options("Todos", 'Técnico', df)
    assentamentos = filter_options("Todos", 'Assentamento', df)
    tipos_de_laudo = filter_options("Todos", 'Tipo de Laudo', df)
    municipios = filter_options("Todos", 'Município', df)
    modalidade = filter_options("Todos", 'Modalidade', df)
    
    # Data inicial padrão: 01/01/2022
    start_date = st.date_input("Data inicial:", datetime(2022, 1, 1))

    # Data final padrão: dia atual
    end_date = st.date_input("Data final:", datetime.now())

    selected_tecnico = st.selectbox("Selecione um técnico:", tecnicos)
    selected_municipio = st.selectbox("Selecione um município:", municipios)
    selected_assentamento = st.selectbox("Selecione um assentamento:", assentamentos)
    selected_tipo_laudo = st.selectbox("Selecione um tipo de laudo:", tipos_de_laudo)
    selected_modalidade = st.selectbox("Selecione uma modalidade:", modalidade)

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
