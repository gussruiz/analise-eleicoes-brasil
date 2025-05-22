import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análise de Votação por Seção", layout="wide")
st.title("Análise de Dados Eleitorais (Votação por Seção)")

CSV_PATH = "../data/votacao_secao_2022_SP.csv"

try:
    df = pd.read_csv(CSV_PATH, sep=";", encoding="latin-1")
    df['QT_VOTOS'] = pd.to_numeric(df['QT_VOTOS'], errors='coerce')
    st.success(f"Arquivo carregado com sucesso: {CSV_PATH}")
except FileNotFoundError:
    st.error(
        f"Arquivo '{CSV_PATH}' não encontrado. Coloque o arquivo na pasta do app.")
    st.stop()

col1, col2, col3 = st.columns(3)
with col1:
    ano = st.selectbox("Ano da eleição", sorted(df['ANO_ELEICAO'].unique()))
with col2:
    uf = st.selectbox("UF", sorted(df['SG_UF'].unique()))
with col3:
    municipio = st.selectbox("Município", sorted(df['NM_MUNICIPIO'].unique()))

df_filtrado = df[(df['ANO_ELEICAO'] == ano) & (
    df['SG_UF'] == uf) & (df['NM_MUNICIPIO'] == municipio)]

st.subheader("🥇 Top 10 Candidatos/Partidos mais Votados no Município")
top_votaveis = df_filtrado.groupby(
    'NM_VOTAVEL')['QT_VOTOS'].sum().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_votaveis.values, y=top_votaveis.index,
            ax=ax1, palette="viridis")
ax1.set_xlabel("Quantidade de Votos")
ax1.set_ylabel("Nome do Votável")
st.pyplot(fig1)

st.subheader("Votos por Cargo")
votos_cargo = df_filtrado.groupby('DS_CARGO')['QT_VOTOS'].sum().sort_values()

fig2, ax2 = plt.subplots(figsize=(10, 5))
votos_cargo.plot(kind='barh', ax=ax2, color='coral')
ax2.set_xlabel("Votos")
ax2.set_ylabel("Cargo")
st.pyplot(fig2)

st.subheader("Comparação: Válidos, Brancos, Nulos")


def classifica_voto(nome):
    if nome == "Voto em branco":
        return "Branco"
    elif nome == "Voto nulo":
        return "Nulo"
    else:
        return "Válido"


df_filtrado['TIPO_VOTO'] = df_filtrado['NM_VOTAVEL'].apply(classifica_voto)
votos_tipo = df_filtrado.groupby('TIPO_VOTO')['QT_VOTOS'].sum()

fig3, ax3 = plt.subplots()
votos_tipo.plot(kind='bar', color=['green', 'lightgray', 'red'], ax=ax3)
ax3.set_ylabel("Quantidade de Votos")
st.pyplot(fig3)

st.subheader("Mapa de Calor por Zona e Seção")
heatmap_data = df_filtrado.pivot_table(
    index='NR_ZONA', columns='NR_SECAO', values='QT_VOTOS', aggfunc='sum').fillna(0)

fig4, ax4 = plt.subplots(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax4)
st.pyplot(fig4)

st.subheader("Total de Votos por Turno")
votos_turno = df_filtrado.groupby('NR_TURNO')['QT_VOTOS'].sum()

fig5, ax5 = plt.subplots()
votos_turno.plot(kind='bar', color=['royalblue', 'darkorange'], ax=ax5)
ax5.set_xlabel("Turno")
ax5.set_ylabel("Total de Votos")
st.pyplot(fig5)
