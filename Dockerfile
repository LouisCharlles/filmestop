# Obter a imagem base do Python
FROM python:3.9-slim

## Instalar as bibliotecas necessárias do sistema(postgresql)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no container
WORKDIR /filmestop

# Copiar o arquivo de requisitos para o container
COPY setup/requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o container
COPY . .

# Expor a porta que a aplicação vai usar
EXPOSE 8000

# Definir o comando para iniciar a aplicação, corrigindo o caminho do wsgi
CMD ["gunicorn", "setup.wsgi:application", "--bind", "0.0.0.0:8000"]
