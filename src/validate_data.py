from sqlalchemy import text

from .connection import engine


with engine.connect() as conn:
    total = conn.execute(
        text("SELECT COUNT(*) FROM leituras_iot")
    ).scalar()

    menor_temp, maior_temp, media_temp = conn.execute(
        text("""
            SELECT
                MIN(temperatura),
                MAX(temperatura),
                AVG(temperatura)
            FROM leituras_iot
        """)
    ).fetchone()

    total_in, total_out = conn.execute(
        text("""
            SELECT
                COUNT(*) FILTER (WHERE ambiente = 'In'),
                COUNT(*) FILTER (WHERE ambiente = 'Out')
            FROM leituras_iot
        """)
    ).fetchone()

print("=== VALIDAÇÃO DO BANCO ===")
print(f"Total de registros: {total}")
print(f"Temperatura mínima: {menor_temp} °C")
print(f"Temperatura máxima: {maior_temp} °C")
print(f"Temperatura média: {media_temp:.2f} °C")
print(f"Registros IN: {total_in}")
print(f"Registros OUT: {total_out}")