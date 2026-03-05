import streamlit as st
import pandas as pd
from datetime import datetime
from database import run_query  # Importa a função que criamos no outro arquivo

st.set_page_config(page_title="Motor de Cálculo", page_icon="📊", layout="wide")


def format_currency(value):
    if pd.isna(value):
        return "R$ 0,00"
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# --- INTERFACE: BARRA LATERAL ---
st.sidebar.header("Filtros do Relatório")

filter_start = st.sidebar.date_input("Data Inicial", datetime(2023, 1, 1))
filter_end = st.sidebar.date_input("Data Término", datetime.today())

opcoes_status = ['Ativo', 'Finalizado']
filter_status = st.sidebar.multiselect(
    "Status do Contrato",
    options=opcoes_status,
    default=opcoes_status
)

gerar_relatorio = st.sidebar.button("Gerar Relatório")

# --- ÁREA PRINCIPAL ---
st.title("📊 Motor de Cálculo de Contratos")
st.markdown("Calcule o faturamento proporcional dos contratos filtrados.")
st.divider()

if gerar_relatorio:
    if filter_start > filter_end:
        st.error("A Data Inicial não pode ser maior que a Data de Término.")
    elif not filter_status:
        st.error("Por favor, selecione pelo menos um Status.")
    else:
        with st.spinner("Consultando banco de dados..."):
            try:
                query = """
                SELECT 
                    c.razao_social, c.setor, cc.status,
                    cc.data_inicio, COALESCE(cc.data_termino, '2026-12-31') AS data_termino, 
                    cc.valor_global
                FROM contrato_cliente cc
                LEFT JOIN cliente c ON cc.cliente = c.id
                WHERE cc.status IN %(status_list)s
                  AND cc.data_inicio <= %(fim)s 
                  AND (cc.data_termino >= %(inicio)s OR cc.data_termino IS NULL)
                """

                params = {
                    'inicio': filter_start,
                    'fim': filter_end,
                    'status_list': tuple(filter_status)
                }

                # Usando nossa nova função do database.py
                df_contratos = run_query(query, params=params)
                qtd_contratos = len(df_contratos)

                if qtd_contratos > 0:
                    # Lógica de Cálculo
                    def calcular_faturamento(row):
                        start_date = pd.to_datetime(row['data_inicio']).date()
                        end_date = pd.to_datetime(row['data_termino']).date()

                        calc_start = max(start_date, filter_start)
                        calc_end = min(end_date, filter_end)

                        days_in_period = (calc_end - calc_start).days + 1 if calc_start <= calc_end else 0
                        total_contract_days = (end_date - start_date).days + 1

                        valor_global = row['valor_global'] if pd.notnull(row['valor_global']) else 0
                        daily_value = valor_global / total_contract_days if total_contract_days > 0 else 0

                        return days_in_period * daily_value


                    df_contratos['faturado_no_periodo'] = df_contratos.apply(calcular_faturamento, axis=1)

                    # 1. Calcula o total por setor
                    df_contratos['total_do_setor'] = df_contratos.groupby('setor')['faturado_no_periodo'].transform(
                        'sum')

                    # 2. NOVO: Conta a quantidade de contratos agrupada por setor
                    df_contratos['qtd_contratos_setor'] = df_contratos.groupby('setor')['razao_social'].transform(
                        'count')

                    # 3. NOVO: Calcula a divisão (média por contrato do setor)
                    df_contratos['media_por_contrato_setor'] = df_contratos['total_do_setor'] / df_contratos[
                        'qtd_contratos_setor']

                    valor_total_painel = df_contratos['faturado_no_periodo'].sum()
                    qtd_ativos = len(df_contratos[df_contratos['status'] == 'Ativo'])
                    qtd_finalizados = len(df_contratos[df_contratos['status'] == 'Finalizado'])

                    # DASHBOARD
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("📄 Total Contratos", qtd_contratos)
                    col2.metric("🟢 Ativos", qtd_ativos)
                    col3.metric("🔴 Finalizados", qtd_finalizados)
                    col4.metric("💰 Faturado no Período", format_currency(valor_total_painel))

                    st.divider()

                    # Preparando DataFrame Visual
                    df_visual = df_contratos.rename(columns={
                        'razao_social': 'Razão Social', 'setor': 'Setor', 'status': 'Status',
                        'data_inicio': 'Início', 'data_termino': 'Término', 'valor_global': 'Valor Global',
                        'faturado_no_periodo': 'Faturado no Período', 'total_do_setor': 'Total do Setor',
                        'media_por_contrato_setor': 'Média por Contrato (Setor)'  # <--- NOVO NOME DA COLUNA
                    }).copy()

                    # Removemos a coluna que foi usada apenas para contagem para não poluir a tabela
                    df_visual = df_visual.drop(columns=['qtd_contratos_setor'])

                    df_visual['Início'] = pd.to_datetime(df_visual['Início']).dt.strftime('%d/%m/%Y')
                    df_visual['Término'] = pd.to_datetime(df_visual['Término']).dt.strftime('%d/%m/%Y')

                    # Adicionamos a nova coluna para ser formatada como Moeda (R$)
                    for col in ['Valor Global', 'Faturado no Período', 'Total do Setor', 'Média por Contrato (Setor)']:
                        df_visual[col] = df_visual[col].apply(format_currency)

                    # Exibição
                    st.dataframe(df_visual.sort_values(by=['Setor', 'Razão Social']), use_container_width=True,
                                 hide_index=True)

                else:
                    st.warning("Nenhum contrato encontrado.")
            except Exception as e:
                st.error("Erro de Conexão com o Banco de Dados.")
                st.code(f"Detalhes: {e}")