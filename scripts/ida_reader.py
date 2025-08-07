import pandas as pd
import os
from unidecode import unidecode


FILE_PATH = "./files"

def read_ods(file_path, sheet=0, skiprows=8):
    try:
        # Lê o arquivo .ods pulando as primeiras linhas (metadados)
        df = pd.read_excel(file_path, engine="odf", sheet_name=sheet, skiprows=skiprows)

        # Filtra somente as linhas onde a variável é o IDA
        df = df[df["VARIÁVEL"].str.contains("IDA", na=False)]

        # Converte colunas mensais em linhas (wide → long format)
        df_melted = df.melt(
            id_vars=["GRUPO ECONÔMICO", "VARIÁVEL"],  # Mantém essas colunas fixas
            var_name="MES",                           # Nova coluna com os nomes das colunas originais
            value_name="IDA"                          # Nova coluna com os valores
        )

        # Identifica o tipo de serviço com base no nome do arquivo
        nome_arquivo = os.path.basename(file_path)
        if nome_arquivo.startswith("SMP"):
            df_melted["SERVICO"] = "Telefonia Celular"
        elif nome_arquivo.startswith("STFC"):
            df_melted["SERVICO"] = "Telefonia Fixa"
        elif nome_arquivo.startswith("SCM"):
            df_melted["SERVICO"] = "Banda Larga Fixa"
        else:
            df_melted["SERVICO"] = "Desconhecido"

        return df_melted

    except Exception as e:
        # Em caso de erro, exibe o erro e retorna um DataFrame vazio
        print(f"{file_path}: {e}")
        return pd.DataFrame()

def read_all_ods(folder):
    # Filtra arquivos .ods
    files = [f for f in os.listdir(folder) if f.endswith(".ods")]
    df_list = []

    for file in files:
        path = os.path.join(folder, file)       # Caminho completo do arquivo
        df = read_ods(path)                     # Lê e transforma o arquivo
        if not df.empty:                        # Verifica se a leitura foi bem-sucedida
            df.columns = [unidecode(col.strip().lower().replace(" ", "_")) for col in df.columns]
            df_list.append(df)                  # Adiciona à lista de DataFrames

    # Retorna um único DataFrame com todos os dados unidos
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()
