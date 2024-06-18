import streamlit as st
import pandas as pd
import base64
from io import BytesIO

def pagina_qapter():
    st.write("<h1><center>Generate Qapter</center></h1>", unsafe_allow_html=True)

    st.title('Excel File Import')

    # Instruções para o usuário
    st.write('Please import 3 Excel files (.xlsx)')

    # Upload de arquivos individuais
    file1 = st.file_uploader("Choose the first file", type=["xlsx"], key="file1")
    file2 = st.file_uploader("Choose the second file", type=["xlsx"], key="file2")
    file3 = st.file_uploader("Choose the third file", type=["xlsx"], key="file3")

    uploaded_files = [file1, file2, file3]

    # Verifica se todos os arquivos foram carregados
    if all(uploaded_files):
        st.success('All files were uploaded successfully!')
        
        # Adicionar um botão para iniciar o processamento
        if st.button('Start Processing'):
            # Adicionar uma barra de progresso
            progress_bar = st.progress(0)
            
            try:
                dfs = []
                progress_bar.progress(10)  # Atualizar para 10%

                for i, uploaded_file in enumerate(uploaded_files):
                    # Lê cada arquivo Excel em um DataFrame
                    df = pd.read_excel(uploaded_file)
                    # Adiciona o DataFrame à lista
                    dfs.append(df)
                    progress_bar.progress(10 + (i + 1) * 20)  # Atualizar para 30%, 50%, 70%

                # Concatena os DataFrames da lista em um único DataFrame
                df_final = pd.concat(dfs, ignore_index=True)
                progress_bar.progress(80)  # Atualizar para 80%

                # Selecionar as colunas desejadas
                colunas_desejadas = ['AX-CODE', 'VEICULO', 'cod_submod', 'submodel', 'cod_carroc', 'desc_carroc', 'cod_motor', 'desc_motor', 'cod_trans', 'desc_trAns', 'opcao_ano', 'opcionaisextra', 'mes_fab', 'ano_fab', 'desc_fab', 'ano_mod', 'code', 'tipo', 'valor', 'MANUFAC_CODE_N', 'MANUFAC_DESCRIP', 'tmo']

                # Criar um novo DataFrame com as colunas desejadas
                novo_df = df_final[colunas_desejadas].copy()

                # Extrair os últimos dois caracteres da coluna 'AX-CODE' e atribuir a uma nova coluna
                novo_df['AX-CODE'] = df_final['AX-CODE'].apply(lambda x: x[-2:])

                # Renomear as colunas no novo DataFrame
                novo_df = novo_df.rename(columns={
                    'AX-CODE': 'cod_familia',
                    'VEICULO': 'VEICULO',
                    'cod_submod': 'submodelo',
                    'submodel': 'desc_submod',
                    'cod_carroc': 'cod_carroc',
                    'desc_carroc': 'desc_carroc',
                    'cod_motor': 'cod_motor',
                    'desc_motor': 'desc_motor',
                    'cod_trans': 'cod_trans',
                    'desc_trAns': 'desc_trAns',
                    'opcao_ano': 'opcao_ano',
                    'opcionaisextra': 'opcionaisextra',
                    'mes_fab': 'mes_fab',
                    'ano_fab': 'ano_fab',
                    'desc_fab': 'desc_fab',
                    'ano_mod': 'ano_mod',
                    'code': 'cod_fipe',
                    'tipo': 'tipo',
                    'valor': 'valor',
                    'MANUFAC_CODE_N': 'cod_fabricante',
                    'MANUFAC_DESCRIP': 'Campo3',
                    'tmo': 'tmo'
                })

                # Substituir os pontos solitários por "none" em todo o DataFrame
                novo_df = novo_df.applymap(lambda x: 'none' if x == '.' else x)

                # Substituir os valores vazios por "NA" em todo o DataFrame
                novo_df = novo_df.applymap(lambda x: 'NA' if x == '' else x)

                # Converter a coluna 'submodelo' para numérica, mantendo os valores não numéricos
                novo_df['submodelo'] = pd.to_numeric(novo_df['submodelo'], errors='coerce')

                # Formatar os números de 1 a 9 com dois caracteres (começando com zero)
                novo_df['submodelo'] = novo_df['submodelo'].apply(lambda x: f'{x:02d}' if 0 < x < 10 else x)

                # Converter a coluna 'mes_fab' para numérica, mantendo os valores não numéricos
                novo_df['mes_fab'] = pd.to_numeric(novo_df['mes_fab'], errors='coerce')

                # Formatar os números de 1 a 9 com dois caracteres (começando com zero)
                novo_df['mes_fab'] = novo_df['mes_fab'].apply(lambda x: f'{x:02d}' if 0 < x < 10 else x)

                progress_bar.progress(100)  # Atualizar para 100%

                # Exibir uma amostra do DataFrame final
                st.write('Final DataFrame Sample:')
                st.dataframe(novo_df.head(100))  # Exibir apenas as primeiras 100 linhas

                # Opção para salvar o DataFrame em um arquivo Excel
                st.markdown(download_link(novo_df, 'search_tree.xlsx', 'Download do Excel'), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
    else:
        st.warning('Please import all 3 Excel files.')

def download_link(data, filename, text):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'

pagina_qapter()
