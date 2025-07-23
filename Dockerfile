# Use uma imagem base Python oficial que seja leve e estável
# 'slim-buster' é uma boa escolha para ambientes de produção.
# Certifique-se que a versão (3.x) é compatível com o seu projeto Django.
FROM python:3.9-slim-buster

# Define variáveis de ambiente para Python
# PYTHONDONTWRITEBYTECODE: Evita a criação de arquivos .pyc
# PYTHONUNBUFFERED: Garante que os logs do Python sejam enviados diretamente para o console do contêiner
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do contêiner
# É para onde o código da sua aplicação será copiado
WORKDIR /app

# Instala as dependências do sistema operacional necessárias (se houver, por exemplo, para drivers de banco de dados)
# Requer um pacote 'build-dep' para compilar 'mysqlclient' ou 'psycopg2' (se usar MySQL/PostgreSQL)
# e 'default-libmysqlclient-dev' ou 'libpq-dev' para as bibliotecas do cliente de BD.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos e instala as dependências Python
# Esta etapa é feita separadamente para aproveitar o cache do Docker.
# Se o requirements.txt não mudar, esta etapa não será reconstruída.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o diretório de trabalho do contêiner
COPY . /app/

# Coleta arquivos estáticos do Django (CSS, JS, imagens do app)
# --noinput evita perguntas interativas
RUN python manage.py collectstatic --noinput

# Expõe a porta que o Gunicorn vai usar dentro do contêiner
EXPOSE 8000

# Comando principal para iniciar o Gunicorn quando o contêiner for executado
# 'guia_servidor_web.wsgi:application' aponta para o seu arquivo WSGI do Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "guia_servidor_web.wsgi:application"]