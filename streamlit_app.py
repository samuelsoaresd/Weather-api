import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# URL base da API (ajuste conforme necessário)
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Previsão do Tempo",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Previsão do Tempo")

def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date_obj.strftime("%d/%m/%Y %H:%M")

with st.sidebar:
    st.header("Consultar Previsão")
    
    with st.form("nova_previsao"):
        cidade_input = st.text_input("Nome da Cidade", value="São Paulo")
        submit_button = st.form_submit_button("Buscar Previsão")
        
        if submit_button:
            try:
                response = requests.post(
                    f"{API_URL}/previsao/",
                    json={"cidade": cidade_input}
                )
                
                if response.status_code == 200:
                    st.success(f"Previsão para {cidade_input} registrada com sucesso!")
                else:
                    st.error(f"Erro: {response.json().get('detail', 'Erro desconhecido')}")
            except Exception as e:
                st.error(f"Erro ao comunicar com a API: {str(e)}")
    
    st.header("Filtrar Previsões")
    
    with st.form("filtrar_previsoes"):
        filter_cidade = st.text_input("Cidade", "")
        
        today = datetime.now()
        last_week = today - timedelta(days=7)
        filter_data = st.date_input(
            "Data",
            value=None,
            min_value=last_week,
            max_value=today
        )
        
        filter_button = st.form_submit_button("Filtrar")

st.header("Previsões Registradas")

params = {}
if 'filter_button' in locals() and filter_button:
    if filter_cidade:
        params['cidade'] = filter_cidade
    if filter_data:
        params['data'] = filter_data.strftime("%Y-%m-%d")

try:
    response = requests.get(f"{API_URL}/previsao/", params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if not data:
            st.info("Nenhum registro encontrado.")
        else:
            df = pd.DataFrame(data)
            
            renamed_columns = {
                'cidade': 'Cidade',
                'temperatura': 'Temperatura (°C)',
                'sensacao_termica': 'Sensação Térmica (°C)',
                'umidade': 'Umidade (%)',
                'descricao': 'Descrição',
                'velocidade_vento': 'Vel. Vento (m/s)',
                'data_consulta': 'Data da Consulta'
            }
            
            df_display = df[renamed_columns.keys()].rename(columns=renamed_columns)
            
            df_display['Data da Consulta'] = df_display['Data da Consulta'].apply(
                lambda x: format_date(x)
            )
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
            
            with st.expander("Gerenciar Registros"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    registro_id = st.number_input(
                        "ID do Registro para Excluir", 
                        min_value=1, 
                        step=1
                    )
                
                with col2:
                    if st.button("Excluir Registro"):
                        try:
                            delete_response = requests.delete(f"{API_URL}/previsao/{registro_id}")
                            
                            if delete_response.status_code == 204:
                                st.success(f"Registro {registro_id} excluído com sucesso!")
                                st.rerun()
                            else:
                                st.error("Registro não encontrado ou erro ao excluir.")
                        except Exception as e:
                            st.error(f"Erro ao comunicar com a API: {str(e)}")
                            
            if len(df) > 1:
                st.subheader("Comparação de Temperaturas")
                
                temp_by_city = df.groupby('cidade')['temperatura'].mean().reset_index()
                
                st.bar_chart(
                    temp_by_city,
                    x='cidade',
                    y='temperatura',
                    use_container_width=True
                )
                
except Exception as e:
    st.error(f"Erro ao comunicar com a API: {str(e)}")
    st.error("Verifique se o servidor da API está em execução.")

# Rodapé
st.divider()
st.caption("Desenvolvido por Samuel Soares")