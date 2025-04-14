# 🧬 Visualizador de Arquivos MDB (Epi Info)

Este é um aplicativo em Python com Streamlit que permite visualizar o conteúdo de arquivos `.mdb` gerados pelo Epi Info (formato Microsoft Access).

## 🛠️ Requisitos

- Python 3.8+
- `mdbtools` instalado no sistema:
  - Ubuntu: `sudo apt install mdbtools`
  - macOS: `brew install mdbtools`

## 🚀 Como rodar localmente

```bash
git clone https://github.com/seuusuario/visualizador-mdb.git
cd visualizador-mdb
pip install -r requirements.txt
streamlit run app.py
