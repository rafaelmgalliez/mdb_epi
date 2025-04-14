import streamlit as st
import subprocess
import pandas as pd
import os

# Função para extrair tabelas usando mdb-tables
def get_tables_from_mdb(mdb_path):
    result = subprocess.run(['mdb-tables', '-1', mdb_path], capture_output=True, text=True)
    tables = result.stdout.strip().split('\n')
    tables = [t for t in tables if t.strip() != '']
    return tables

# Função para obter dados de uma tabela
def get_table_data_from_mdb(mdb_path, table_name):
    try:
        result = subprocess.run(['mdb-export', mdb_path, table_name], capture_output=True, text=True)
        data = result.stdout
        if data.strip() == "":
            return None
        from io import StringIO
        df = pd.read_csv(StringIO(data))
        return df
    except Exception as e:
        print(f"Erro ao ler tabela {table_name}: {e}")
        return None

# Verifica quais tabelas têm dados e quais estão vazias
def get_non_empty_tables(mdb_path, tables):
    non_empty = []
    empty = []
    for table in tables:
        try:
            df = get_table_data_from_mdb(mdb_path, table)
            if df is not None and not df.empty:
                non_empty.append(table)
            else:
                empty.append(table)
        except Exception as e:
            print(f"Erro ao processar tabela {table}: {e}")
            empty.append(table)
    return non_empty, empty

def main():
    st.set_page_config(page_title="Visualizador MDB (Epi Info)", layout="wide")
    st.title("📊 Leitor de Arquivos MDB (Epi Info)")

    uploaded_file = st.file_uploader("📁 Faça upload de um arquivo .mdb", type=["mdb"])

    if uploaded_file is not None:
        with open("uploaded_file.mdb", "wb") as f:
            f.write(uploaded_file.read())

        tables = get_tables_from_mdb("uploaded_file.mdb")

        if not tables:
            st.warning("⚠️ Nenhuma tabela encontrada no arquivo.")
            return

        try:
            with st.spinner("🔍 Verificando conteúdo das tabelas..."):
                tabelas_com_dados, tabelas_vazias = get_non_empty_tables("uploaded_file.mdb", tables)
        except Exception as e:
            st.error(f"Erro ao verificar tabelas: {e}")
            return

        st.success(f"✅ Tabelas com dados: {len(tabelas_com_dados)} | 🗃️ Vazias: {len(tabelas_vazias)}")

        if tabelas_com_dados:
            selected_table = st.selectbox("📌 Selecione uma tabela com dados", tabelas_com_dados)
            table_data = get_table_data_from_mdb("uploaded_file.mdb", selected_table)

            if table_data is not None:
                st.markdown(f"### 🧾 Conteúdo da Tabela: `{selected_table}`")
                st.dataframe(table_data, use_container_width=True)
            else:
                st.warning(f"A tabela `{selected_table}` não possui dados.")
        else:
            st.info("Nenhuma tabela com dados foi encontrada no arquivo.")

        with st.expander("🗂️ Ver tabelas vazias"):
            st.write(tabelas_vazias)

if __name__ == "__main__":
    main()

