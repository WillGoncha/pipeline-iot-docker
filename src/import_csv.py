import pandas as pd
from sqlalchemy import insert

from .connection import engine
from .models import LeituraCSV


ARQUIVO = "data/IOT-temp.csv"


print("Lendo CSV...")

df = pd.read_csv(ARQUIVO)

df["noted_date"] = pd.to_datetime(
    df["noted_date"],
    format="%d-%m-%Y %H:%M"
)

df = df.rename(columns={
    "room_id/id": "room_id",
    "noted_date": "data_hora",
    "temp": "temperatura",
    "out/in": "ambiente"
})

df = df[
    [
        "id",
        "room_id",
        "data_hora",
        "temperatura",
        "ambiente"
    ]
]

duplicados = df["id"].duplicated().sum()

print(f"IDs duplicados encontrados: {duplicados}")

df = df.drop_duplicates(subset=["id"], keep="first")

print(f"Registros após limpeza: {len(df)}")

print(f"Registros encontrados: {len(df)}")
print("Iniciando importação...")

dados = df.to_dict(orient="records")

with engine.begin() as conn:
    conn.execute(insert(LeituraCSV), dados)

print("IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
print(f"Total importado: {len(dados)}")