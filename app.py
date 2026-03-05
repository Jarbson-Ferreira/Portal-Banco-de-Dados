import streamlit as st

st.set_page_config(
    page_title="Portal de Conexão Banco de Dados - Vintech",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Portal de Conexão Banco de Dados - Vintech")
st.markdown("Bem-vindo ao sistema integrado de gestão e inteligência comercial.")
st.divider()

st.markdown("""
### O que você pode fazer aqui:
👈 **Use o menu lateral para navegar entre os módulos:**

* **📊 Faturamento:** Motor de cálculo e projeção financeira dos contratos ativos.
* **🎯 Licitações:** Radar de oportunidades e match de softwares com editais do PNCP.
* **⏳ Gestão de Atas:** Controle de vigência e saldo de Atas de Registro de Preço.
* **📚 Catálogo:** Base de conhecimento técnica dos nossos produtos.
""")

st.info("💡 Selecione um módulo no menu à esquerda para começar.")