# 🏢 Portal de Inteligência de Contratos e Licitações

Este projeto é uma aplicação web interativa desenvolvida em **Python** e **Streamlit**. O objetivo central do sistema é atuar como uma plataforma B2G (Business to Government) para gestão de contratos, projeção de faturamento financeiro, inteligência de licitações (PNCP), gestão de Atas de Registro de Preços e catálogo técnico de produtos de software.

---

## ✨ Funcionalidades (Módulos)

A aplicação foi estruturada em múltiplas páginas (Multipage App) para garantir escalabilidade e organização. Os módulos atuais incluem:

* **📊 Motor de Cálculo (Faturamento):** Calcula o faturamento proporcional dos contratos ativos e finalizados em um determinado período de tempo, gerando médias financeiras por setor e permitindo a exportação de dados.
* **🎯 Radar de Licitações (Em breve):** Painel de inteligência de mercado para mapeamento de editais públicos, cruzando o portfólio da empresa (Match Score) com oportunidades do PNCP.
* **⏳ Gestão de Atas (Em breve):** Monitoramento de vigência, saldo e vencimento de Atas de Registro de Preços (ARP).
* **📚 Catálogo de Produtos:** Base de conhecimento técnica para as equipes de pré-vendas e desenvolvimento, detalhando a stack, objetivos e funções de cada módulo dos softwares da empresa.

---

## 🛠️ Tecnologias Utilizadas

* **[Streamlit](https://streamlit.io/):** Framework para construção rápida da interface web e dashboards interativos.
* **[Pandas](https://pandas.pydata.org/):** Manipulação, limpeza e análise de dados (DataFrames).
* **[SQLAlchemy](https://www.sqlalchemy.org/):** ORM e motor de conexão nativa com o banco de dados.
* **[Psycopg2](https://pypi.org/project/psycopg2/):** Driver de adaptação do banco de dados PostgreSQL para Python.
* **[Python-dotenv](https://pypi.org/project/python-dotenv/):** Gerenciamento de variáveis de ambiente e credenciais de segurança.
* **Banco de Dados:** PostgreSQL.

---

## 📁 Estrutura do Projeto

```text
/meu_projeto_streamlit
│
├── .env                       # Variáveis de ambiente e senhas (Não comitar!)
├── .gitignore                 # Arquivos ignorados pelo Git
├── requirements.txt           # Lista de bibliotecas e dependências
├── database.py                # Módulo central de conexão e cache com o banco
├── app.py                     # Página Home / Dashboard principal
│
└── pages/                     # Páginas do Menu Lateral
    ├── 1_📊_Faturamento.py    # Módulo de cálculo financeiro