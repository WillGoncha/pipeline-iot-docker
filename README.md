# Pipeline de Dados com IoT e Docker

Projeto acadêmico desenvolvido para demonstrar um pipeline de dados utilizando Python, PostgreSQL, Docker e Streamlit.

O projeto utiliza um arquivo CSV com dados de temperatura, armazena essas informações em um banco de dados PostgreSQL e apresenta os dados por meio de um dashboard.

## Tecnologias utilizadas

- Python
- Pandas
- PostgreSQL
- Docker
- SQLAlchemy
- Streamlit
- Plotly

## Estrutura do projeto

```text
Project IOT/
├── dashboard/
│   └── dashboard.py
├── data/
│   └── IOT-temp.csv
├── docs/
│   └── screenshots/
├── sql/
│   └── views.sql
├── src/
│   ├── connection.py
│   ├── create_tables.py
│   ├── import_csv.py
│   ├── models.py
│   └── validate_data.py
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## Banco de dados

O banco PostgreSQL é executado utilizando Docker.

A tabela principal utilizada no projeto é:

```text
leituras_iot
```

Ela armazena os dados de temperatura presentes no arquivo CSV.

## Análise dos dados

Foram criadas algumas consultas SQL para facilitar a análise dos dados:

- Temperatura média por ambiente;
- Quantidade de leituras por hora;
- Temperatura mínima, máxima e média por dia.

## Dashboard

O dashboard foi desenvolvido utilizando Streamlit e Plotly.

Ele apresenta informações como:

- Quantidade de registros;
- Temperatura mínima, máxima e média;
- Temperatura média por ambiente;
- Quantidade de leituras por hora;
- Temperaturas por dia.

As imagens do dashboard estão disponíveis em:

```text
docs/screenshots/
```

## Como executar

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Inicie o banco de dados:

```powershell
docker compose up -d
```

Crie as tabelas:

```powershell
python -m src.create_tables
```

Importe os dados:

```powershell
python -m src.import_csv
```

Crie as views:

```powershell
Get-Content .\sql\views.sql | docker exec -i postgres-iot psql -U iot_user -d iot_database
```

Valide os dados:

```powershell
python -m src.validate_data
```

Execute o dashboard:

```powershell
python -m streamlit run dashboard/dashboard.py
```

## Objetivo

Demonstrar, de forma prática, o funcionamento de um pipeline de dados utilizando conceitos de IoT, banco de dados, Docker e visualização de dados.