import streamlit as st
import pandas as pd
import plotly.express as px

# Título do aplicativo
st.set_page_config(layout="wide")
st.title(" Dashboard de Matrículas Escolares")

# Carregar dataset
@st.cache_data
def carregar_dados(name):
    df = pd.read_csv(name)
    return df

df = carregar_dados("dados_matriculas.csv")

# Sidebar para filtros globais
st.sidebar.header(" Filtros Globais")

ano_selecionado = st.sidebar.multiselect(
    "Selecionar Ano de Matrícula",
    options=df["Ano_Matricula"].unique(),
    default=df["Ano_Matricula"].unique()
)

regiao_selecionada = st.sidebar.multiselect(
    "Selecionar Região",
    options=df["Regiao"].unique(),
    default=df["Regiao"].unique()
)

# Aplicar filtros globais
df_filtrado_global = df[
    (df["Ano_Matricula"].isin(ano_selecionado)) &
    (df["Regiao"].isin(regiao_selecionada))
]

st.subheader(" Visão Geral dos Dados")
st.dataframe(df_filtrado_global.head())

# 1. Visualização de matrículas por região geográfica
st.markdown("### 1. Visualização de Matrículas por Região Geográfica")
matriculas_por_regiao = df_filtrado_global.groupby("Regiao")["Numero_Matriculas"].sum().reset_index()
fig_regiao = px.bar(
    matriculas_por_regiao,
    x="Regiao",
    y="Numero_Matriculas",
    title="Total de Matrículas por Região",
    labels={"Regiao": "Região", "Numero_Matriculas": "Número de Matrículas"},
    color="Regiao"
)
st.plotly_chart(fig_regiao, use_container_width=True)

# 2. Análise detalhada de matrículas por unidade escolar
st.markdown("### 2. Análise Detalhada de Matrículas por Unidade Escolar")

# Filtros para esta seção
tipo_unidade_selecionado = st.multiselect(
    "Filtrar por Tipo de Unidade Escolar",
    options=df_filtrado_global["Tipo_Unidade_Escolar"].unique(),
    default=df_filtrado_global["Tipo_Unidade_Escolar"].unique()
)

df_filtrado_unidade = df_filtrado_global[
    df_filtrado_global["Tipo_Unidade_Escolar"].isin(tipo_unidade_selecionado)
]

matriculas_por_unidade = df_filtrado_unidade.groupby(["Nome_Unidade_Escolar", "Tipo_Unidade_Escolar"])["Numero_Matriculas"].sum().reset_index()
matriculas_por_unidade = matriculas_por_unidade.sort_values(by="Numero_Matriculas", ascending=False)

# Exibir as top N escolas
num_escolas = st.slider("Número de Escolas para Exibir", min_value=5, max_value=50, value=10)
fig_unidade = px.bar(
    matriculas_por_unidade.head(num_escolas),
    x="Nome_Unidade_Escolar",
    y="Numero_Matriculas",
    color="Tipo_Unidade_Escolar",
    title=f"Top {num_escolas} Unidades Escolares por Número de Matrículas",
    labels={"Nome_Unidade_Escolar": "Unidade Escolar", "Numero_Matriculas": "Número de Matrículas"},
    hover_data=["Tipo_Unidade_Escolar"]
)
st.plotly_chart(fig_unidade, use_container_width=True)

# 3. Visão agregada por superintendências regionais
st.markdown("### 3. Visão Agregada por Superintendências Regionais")

# Filtros para esta seção
superintendencia_selecionada = st.multiselect(
    "Filtrar por Superintendência",
    options=df_filtrado_global["Superintendencia"].unique(),
    default=df_filtrado_global["Superintendencia"].unique()
)

df_filtrado_super = df_filtrado_global[
    df_filtrado_global["Superintendencia"].isin(superintendencia_selecionada)
]

matriculas_por_super = df_filtrado_super.groupby(["Superintendencia", "Regiao"])["Numero_Matriculas"].sum().reset_index()
fig_super = px.bar(
    matriculas_por_super,
    x="Superintendencia",
    y="Numero_Matriculas",
    color="Regiao",
    title="Total de Matrículas por Superintendência Regional",
    labels={"Superintendencia": "Superintendência Regional", "Numero_Matriculas": "Número de Matrículas"},
    hover_data=["Regiao"]
)
st.plotly_chart(fig_super, use_container_width=True)

# Adicionando um mapa (exemplo simples com dados fictícios)
st.markdown("### Matrículas por Estado (Exemplo de Mapa)")
matriculas_por_estado = df_filtrado_global.groupby("Estado")["Numero_Matriculas"].sum().reset_index()

# Para um mapa, precisaríamos de coordenadas geográficas reais para os estados.
# Como os dados são fictícios, este é um exemplo conceitual.
# Para um mapa real, usaríamos um shapefile ou dados geojson.
# Por simplicidade, vamos apenas mostrar um gráfico de barras por estado.
fig_estado = px.bar(
    matriculas_por_estado,
    x="Estado",
    y="Numero_Matriculas",
    title="Total de Matrículas por Estado",
    labels={"Estado": "Estado", "Numero_Matriculas": "Número de Matrículas"},
    color="Estado"
)
st.plotly_chart(fig_estado, use_container_width=True)