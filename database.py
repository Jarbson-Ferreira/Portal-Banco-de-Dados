import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()


@st.cache_resource  # Faz cache da engine para não reconectar a todo momento
def init_connection():
    db_user = os.getenv("DATABASE_USER_NAME")
    db_pass = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_port = os.getenv("DATABASE_PORT")
    db_name = os.getenv("DATABASE_NAME")

    string_conexao = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return create_engine(string_conexao)


@st.cache_data(ttl=600)  # Faz cache dos dados da query por 10 minutos (600 seg)
def run_query(query, params=None):
    engine = init_connection()
    return pd.read_sql(query, engine, params=params)