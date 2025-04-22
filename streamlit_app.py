import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_URL = "http://localhost:8000"

st.title("🌤️ Previsão do Tempo")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Consultar Nova Previsão")
    cidade = st.text_input("Nome da cidade")
    if st.button("Buscar Previsão"):
        if cidade:
            try:
                response = requests.post(f"{API_URL}/previsao/", json={"cidade": cidade})
                if response.status_code == 200:
                    st.success(f"Previsão para {cidade} registrada com sucesso!")
                else:
                    st.error("Erro ao buscar previsão")
            except Exception as e:
                st.error(f"Erro: {str(e)}")
        else:
            st.warning("Digite o nome da cidade")

with col2:
    st.subheader("Gerenciar Previsões")
    opcao = st.selectbox(
        "O que deseja fazer?",
        ["Ver todas as previsões", "Filtrar por cidade", "Limpar histórico"]
    )
    
    if opcao == "Filtrar por cidade":
        cidade_filtro = st.text_input("Digite a cidade para filtrar")
        if st.button("Filtrar"):
            if cidade_filtro:
                params = {"cidade": cidade_filtro}
            else:
                params = {}
        else:
            params = {}
    elif opcao == "Limpar histórico":
        cidade_limpar = st.text_input("Digite a cidade para limpar o histórico (deixe em branco para ver todas)")
        if st.button("Limpar Histórico", type="primary"):
            try:
                if cidade_limpar:
                    response = requests.delete(f"{API_URL}/previsao/cidade/{cidade_limpar}")
                else:
                    response = requests.delete(f"{API_URL}/limpar-tudo?confirmar=true")
                
                if response.status_code in [200, 204]:
                    data = response.json()
                    st.success(f"{data.get('registros_excluidos', 0)} registros excluídos com sucesso!")
                else:
                    st.error("Erro ao limpar histórico")
            except Exception as e:
                st.error(f"Erro: {str(e)}")
        params = {}
    else:
        params = {}

st.subheader("Previsões Disponíveis")

try:
    response = requests.get(f"{API_URL}/previsao/", params=params)
    if response.status_code == 200:
        data = response.json()
        if not data:
            st.info("Nenhum registro encontrado.")
        else:
            df = pd.DataFrame(data)
            
            df['data_consulta'] = pd.to_datetime(df['data_consulta']).dt.strftime('%d/%m/%Y %H:%M')
            
            for i, row in df.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{row['cidade']}**: {row['temperatura']}°C - {row['descricao']}")
                    with col2:
                        st.write(f"Data: {row['data_consulta']}")
                    with col3:
                        if st.button(f"🗑️ Excluir", key=f"del_{row['id']}"):
                            try:
                                response = requests.delete(f"{API_URL}/previsao/{row['id']}")
                                if response.status_code == 204:
                                    st.success("Registro excluído com sucesso!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao excluir registro")
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")
                    st.divider()
            
            st.subheader("Comparação de Temperaturas por Cidade")
            
            cidades_unicas = df['cidade'].unique()
            
            if len(cidades_unicas) > 1:
                temp_by_city = df.groupby('cidade')['temperatura'].mean().reset_index()
                
                st.bar_chart(
                    temp_by_city,
                    x='cidade',
                    y='temperatura',
                    use_container_width=True
                )
            else:
                if len(df) > 1:
                    st.write(f"Evolução da temperatura em {cidades_unicas[0]}")
                    
                    df['data_ordenacao'] = pd.to_datetime(df['data_consulta'], format='%d/%m/%Y %H:%M')
                    df = df.sort_values('data_ordenacao')
                    
                    chart_data = pd.DataFrame({
                        'data': df['data_consulta'],
                        'temperatura': df['temperatura']
                    })
                    
                    st.line_chart(
                        chart_data,
                        x='data',
                        y='temperatura',
                        use_container_width=True
                    )
                else:
                    st.info("Adicione mais registros para visualizar gráficos comparativos.")
            
except Exception as e:
    st.error(f"Erro ao comunicar com a API: {str(e)}")

# Rodapé
st.divider()
st.caption("Desenvolvido por Samuel Soares")