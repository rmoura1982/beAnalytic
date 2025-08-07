from connections import postgres_conn
from ida_reader import read_all_ods

if __name__ == "__main__":
    engine = postgres_conn()
    folder = "./files"

    df_final = read_all_ods(folder)

    try:
        df_final.to_sql(
            "ida", 
            con=engine, 
            schema="raw", 
            if_exists='append', 
            index=False
        )
        print("Inseriu no banco normalmente!")
    except Exception as e:
        print("Erro ao inserir no banco:", e)
