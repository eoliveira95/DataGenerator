import streamlit as st
import pandas as pd
import base64
from io import BytesIO

def pagina_novaslinhas():
    st.write("<h1><center>New Lines</center></h1>", unsafe_allow_html=True)

    # Interface para importar o primeiro arquivo Excel
    uploaded_file1 = st.file_uploader("Upload Old TBL", type=["xls", "xlsx"], key="uploader1")
    
    # Interface para importar o segundo arquivo Excel
    uploaded_file2 = st.file_uploader("Upload the new TBL", type=["xls", "xlsx"], key="uploader2")

    completion_date = None

    # Verificar se ambos os arquivos foram carregados
    if uploaded_file1 is not None and uploaded_file2 is not None:
        # Solicitar a data de conclusão ao usuário
        completion_date = st.date_input("Completion date of the new TBL:")

        # Adicionar um botão para processar os arquivos
        if st.button('Process Files'):
            if completion_date:
                try:
                    progress_bar = st.progress(0)

                    # Carregar o primeiro arquivo Excel
                    df1 = pd.read_excel(uploaded_file1)
                    progress_bar.progress(20)  # Atualizar para 20%

                    # Carregar o segundo arquivo Excel
                    df2 = pd.read_excel(uploaded_file2)
                    progress_bar.progress(40)  # Atualizar para 40%

                    # Formatar a coluna 'submodelo'
                    df1['submodelo'] = df1['submodelo'].apply(lambda x: f'{int(x):02d}' if (str(x).isdigit() or x == '0') else x)
                    df2['submodelo'] = df2['submodelo'].apply(lambda x: f'{int(x):02d}' if (str(x).isdigit() or x == '0') else x)
                    progress_bar.progress(50)  # Atualizar para 50%

                    # Formatar a coluna 'mes_fab'
                    df1['mes_fab'] = df1['mes_fab'].apply(lambda x: f'{int(x):02d}' if (str(x).isdigit() or x == '0') else x)
                    df2['mes_fab'] = df2['mes_fab'].apply(lambda x: f'{int(x):02d}' if (str(x).isdigit() or x == '0') else x)
                    progress_bar.progress(60)  # Atualizar para 60%

                    # Formatar a coluna 'cod_motor'
                    df1['cod_motor'].fillna("NA", inplace=True)
                    df2['cod_motor'].fillna("NA", inplace=True)
                    progress_bar.progress(70)  # Atualizar para 70%

                    # Criar a coluna "Chave_Primária" em ambos os DataFrames
                    df1['Chave_Primária'] = df1['cod_familia'].astype(str) + df1['submodelo'].astype(str) + df1['cod_carroc'].astype(str) + df1['cod_motor'].astype(str) + df1['cod_trans'].astype(str) + df1['opcao_ano'].astype(str)
                    df2['Chave_Primária'] = df2['cod_familia'].astype(str) + df2['submodelo'].astype(str) + df2['cod_carroc'].astype(str) + df2['cod_motor'].astype(str) + df2['cod_trans'].astype(str) + df2['opcao_ano'].astype(str)
                    progress_bar.progress(80)  # Atualizar para 80%

                    # Identificar as chaves primárias distintas que estão em df2, mas não em df1
                    novas_linhas = df2[~df2['Chave_Primária'].isin(df1['Chave_Primária'].unique())]

                    # Adicionar a nova coluna "PRCODE"
                    novas_linhas['PRCODE'] = novas_linhas['cod_fabricante'].astype(str) + novas_linhas['cod_familia'].astype(str)
                    
                    # Adicionar a nova coluna "Completion" com a data fornecida pelo usuário
                    completion_date_str = completion_date.strftime("%d/%m/%Y")
                    novas_linhas['Completion'] = completion_date_str
                    progress_bar.progress(100)  # Atualizar para 100%

                    # Exibir novo dataframe
                    st.subheader("DataFrame Resultante:")
                    st.dataframe(novas_linhas)

                    # Adicionar um botão para fazer o download do DataFrame em formato XLSX
                    st.markdown(download_dataframe(novas_linhas, "novas_linhas"), unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")
            else:
                st.error("Please enter the completion date.")
        else:
            st.error("Please upload both files before processing.")

def download_dataframe(df, filename):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">Download {filename} Excel file</a>'
    return href

pagina_novaslinhas()
