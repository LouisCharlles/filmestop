
from pathlib import Path
from decouple import config, Csv
import environ

# BASE_DIR define o caminho base do projeto. É usado para definir outros caminhos no projeto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações rápidas para o desenvolvimento - Não são adequadas para produção.
# Para mais detalhes, veja: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# A chave secreta usada para criptografia e segurança do Django.
# Ela deve ser mantida em segredo em produção.
SECRET_KEY = config('SECRET_KEY')

# Define se o projeto está em modo de depuração (DEBUG) ou não. Nunca habilite o DEBUG em produção.
DEBUG = config('DEBUG')

# Define quais hosts podem acessar o projeto. Utiliza uma lista de hosts fornecida no arquivo de ambiente.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Definição dos aplicativos instalados no Django.
# Esses são os módulos e pacotes que fazem parte do projeto ou que o Django utiliza.
INSTALLED_APPS = [
    'django.contrib.admin',  # Interface de administração do Django
    'django.contrib.auth',  # Sistema de autenticação do Django
    'django.contrib.contenttypes',  # Suporte a tipos de conteúdo
    'django.contrib.sessions',  # Gerenciamento de sessões
    'django.contrib.messages',  # Sistema de mensagens
    'django.contrib.staticfiles',  # Gerenciamento de arquivos estáticos (CSS, JS, etc.)
    'filmestop.apps.FilmestopConfig',  # Aplicativo específico do projeto "FilmesTop"
]

# Lista de middleware. Middleware são componentes que processam solicitações e respostas no Django.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Melhora a segurança do site
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gerencia as sessões entre as requisições
    'django.middleware.common.CommonMiddleware',  # Middleware comum que adiciona cabeçalhos e faz redirecionamentos
    'django.middleware.csrf.CsrfViewMiddleware',  # Protege contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autentica o usuário para cada requisição
    'django.contrib.messages.middleware.MessageMiddleware',  # Gerencia o sistema de mensagens
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protege contra ataques de clickjacking
]

# Especifica o arquivo de configuração de URLs principal do projeto.
ROOT_URLCONF = 'setup.urls'

# Configuração dos templates HTML do Django.
# Define onde e como o Django encontrará e processará os templates HTML.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Backend padrão de templates do Django
        'DIRS': [],  # Diretórios de templates personalizados
        'APP_DIRS': True,  # Se verdadeiro, o Django buscará templates nas pastas dos apps
        'OPTIONS': {
            'context_processors': [  # Funções que injetam dados no contexto dos templates
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração da aplicação WSGI, usada para deploy do projeto em servidores.
WSGI_APPLICATION = 'setup.wsgi.application'

# Configurações do banco de dados.
# Utiliza o pacote `environ` para carregar as variáveis do ambiente a partir do arquivo `.env`.
env = environ.Env()
environ.Env.read_env(env_file='./.env')  # Carrega as variáveis de ambiente do arquivo .env

# Configuração para o uso do banco de dados PostgreSQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Usa o backend do PostgreSQL
        'NAME': env('DB_NAME'),  # Nome do banco de dados
        'USER': env('DB_USER'),  # Usuário do banco de dados
        'PASSWORD': env('DB_PASSWORD'),  # Senha do banco de dados
        'HOST': env('DB_HOST'),  # Endereço do servidor do banco de dados
        'PORT': env('DB_PORT'),  # Porta do servidor do banco de dados
    }
}

# Validação de senhas. Essas configurações definem as políticas de segurança das senhas de usuários.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Verifica se a senha é similar ao nome de usuário
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Verifica se a senha possui o tamanho mínimo
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Verifica se a senha é comum (fraca)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Verifica se a senha é inteiramente numérica
    },
]

# Configurações de internacionalização.
# Define o idioma padrão do site e o fuso horário.
LANGUAGE_CODE = 'pt-br'  # Idioma padrão do site
TIME_ZONE = 'America/Fortaleza'  # Fuso horário padrão do site

# Ativa a tradução do Django (internationalization).
USE_I18N = True

# Ativa o suporte para fuso horário.
USE_TZ = True

# Configuração de arquivos estáticos.
# Define a URL e o diretório onde os arquivos estáticos (CSS, JS, etc.) serão servidos.
STATIC_URL = 'static/'

# Define o tipo de campo de chave primária padrão para modelos que não especificam uma chave primária.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


