# Usa imagem Python
FROM python:3.11.12-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY . .

# Instala dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Comando padrão (pode ser alterado se quiser rodar outro script)
CMD ["python", "scripts/postgres_load.py"]
