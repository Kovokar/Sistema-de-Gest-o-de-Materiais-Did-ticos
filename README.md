# Sistema de Gestão de Material Didático API

Uma API RESTful desenvolvida em Django REST Framework para gerenciamento de envios de material didático educacional.

## 🚀 Funcionalidades

- **👥 Gestão de Usuários**: Cadastro e controle de usuários com diferentes perfis
- **🎓 Gestão Acadêmica**: Controle de etapas escolares e disciplinas
- **📚 Controle de Material**: Registro e acompanhamento de envios de material didático
- **📊 Relatórios**: Estatísticas e relatórios detalhados
- **🔍 Busca Avançada**: Filtros e buscas em todos os endpoints
- **📖 Documentação**: API totalmente documentada com Swagger/OpenAPI

## 🛠️ Tecnologias

- **Django 4.2** - Framework web
- **Django REST Framework 3.14** - API REST
- **drf-spectacular** - Documentação OpenAPI/Swagger
- **django-filter** - Filtros avançados
- **PostgreSQL/MySQL** - Banco de dados
- **Redis** - Cache e sessões
- **Celery** - Tarefas assíncronas

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- PostgreSQL ou MySQL (opcional, SQLite incluído por padrão)
- Redis (opcional, para cache e Celery)

## 🚀 Instalação e Configuração

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/material-didatico-api.git
cd material-didatico-api
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Banco de Dados

#### Opção 1: SQLite (padrão - não requer configuração)
O projeto já está configurado para usar SQLite por padrão.

#### Opção 2: PostgreSQL
```bash
# Instale o PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Crie o banco de dados
sudo -u postgres createdb material_didatico_db
sudo -u postgres createuser --interactive
```

#### Opção 3: MySQL
```bash
# Instale o MySQL
sudo apt-get install mysql-server

# Crie o banco de dados
mysql -u root -p
CREATE DATABASE material_didatico_db;
CREATE USER 'api_user'@'localhost' IDENTIFIED BY 'sua_senha';
GRANT ALL PRIVILEGES ON material_didatico_db.* TO 'api_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (ajuste conforme sua configuração)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=material_didatico_db
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

# Redis (opcional)
REDIS_URL=redis://localhost:6379/0

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_app
```

### 6. Execute as Migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crie um Superusuário

```bash
python manage.py createsuperuser
```

### 8. Carregue Dados Iniciais (Opcional)

```bash
# Crie alguns dados iniciais para teste
python manage.py loaddata initial_data.json
```

### 9. Execute o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

## 📚 Acesso à API

### URLs Principais

- **API Root**: http://localhost:8000/api/
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Admin Panel**: http://localhost:8000/admin/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Endpoints Disponíveis

| Endpoint | Métodos | Descrição |
|----------|---------|-----------|
| `/api/perfis/` | GET, POST, PUT, DELETE | Gestão de perfis |
| `/api/usuarios/` | GET, POST, PUT, DELETE | Gestão de usuários |
| `/api/etapas-escolares/` | GET, POST, PUT, DELETE | Gestão de etapas escolares |
| `/api/disciplinas/` | GET, POST, PUT, DELETE | Gestão de disciplinas |
| `/api/status-envio/` | GET, POST, PUT, DELETE | Gestão de status |
| `/api/envios-material/` | GET, POST, PUT, DELETE | Gestão de envios |

### Endpoints Customizados

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/usuarios/by_perfil/` | GET | Usuários por perfil |
| `/api/envios-material/by_user/` | GET | Envios por usuário |
| `/api/envios-material/by_period/` | GET | Envios por período |
| `/api/envios-material/pending/` | GET | Envios pendentes |
| `/api/envios-material/stats/` | GET | Estatísticas de envios |
| `/api/envios-material/overdue/` | GET | Envios em atraso |

## 📖 Exemplos de Uso

### 1. Criar um Usuário

```bash
curl -X POST http://localhost:8000/api/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{
    "id_perfil": 1,
    "nome_usuario": "João Silva",
    "matricula": "MAT2024001",
    "cpf": "123.456.789-00",
    "senha": "senha123",
    "telefone": "(85) 99999-9999"
  }'
```

### 2. Listar Usuários com Filtro

```bash
# Por perfil
curl "http://localhost:8000/api/usuarios/?id_perfil=1"

# Busca por nome
curl "http://localhost:8000/api/usuarios/?search=João"

# Ordenação
curl "http://localhost:8000/api/usuarios/?ordering=nome_usuario"
```

### 3. Criar um Envio de Material

```bash
curl -X POST http://localhost:8000/api/envios-material/ \
  -H "Content-Type: application/json" \
  -d '{
    "id_etapa": 1,
    "id_disciplina": 1,
    "id_usuario": 1,
    "id_status": 1,
    "mes_referencia": 3,
    "ano_referencia": 2024,
    "observacoes_gerencia": "Material aprovado",
    "data_limite_envio": "2024-03-15"
  }'
```

### 4. Filtros Avançados para Envios

```bash
# Por período
curl "http://localhost:8000/api/envios-material/?ano_referencia=2024&mes_referencia=3"

# Por faixa de datas
curl "http://localhost:8000/api/envios-material/?data_envio_escola_gte=2024-01-01&data_envio_escola_lte=2024-03-31"

# Múltiplos filtros
curl "http://localhost:8000/api/envios-material/?id_disciplina=1&id_status=1&ordering=-data_envio_escola"
```

### 5. Usar Endpoints Customizados

```bash
# Estatísticas por período
curl "http://localhost:8000/api/envios-material/stats/?mes=3&ano=2024"

# Envios por usuário
curl "http://localhost:8000/api/envios-material/by_user/?user_id=1"

# Envios pendentes
curl "http://localhost:8000/api/envios-material/pending/"
```

## 🔧 Configuração de Produção

### 1. Variáveis de Ambiente para Produção

```bash
# .env.production
SECRET_KEY=sua_chave_super_secreta_de_producao
DEBUG=False
ALLOWED_HOSTS=api.educacao.gov.br,localhost

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=material_didatico_prod
DB_USER=api_user
DB_PASSWORD=senha_forte_producao
DB_HOST=db.educacao.gov.br
DB_PORT=5432

# Redis
REDIS_URL=redis://redis.educacao.gov.br:6379/0

# Email
EMAIL_HOST=smtp.educacao.gov.br
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=sistema@educacao.gov.br
EMAIL_HOST_PASSWORD=senha_email
```

### 2. Configuração com Docker

Crie um `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DEBUG=False
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=material_didatico_db
      - POSTGRES_USER=api_user
      - POSTGRES_PASSWORD=senha123
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 3. Configuração do Nginx

```nginx
# nginx.conf
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name api.educacao.gov.br;

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test material_didatico.tests.test_models

# Com coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML
```

### Testes da API com pytest

```bash
# Instalar pytest
pip install pytest pytest-django

# Executar testes
pytest

# Com verbose
pytest -v

# Teste específico
pytest tests/test_api.py::TestUsuarioAPI::test_create_user
```

## 📊 Monitoramento e Logs

### 1. Configuração de Logs

Os logs são configurados automaticamente e salvos em:
- Console (desenvolvimento)
- Arquivo `api.log` (produção)

### 2. Monitoramento com Sentry

```bash
pip install sentry-sdk

# Adicione ao settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="sua_dsn_do_sentry",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### 3. Health Check

```bash
# Verificar saúde da API
curl http://localhost:8000/health/

# Com detalhes
curl http://localhost:8000/health/?format=json
```

## 🔐 Autenticação e Segurança

### 1. Configurar JWT Authentication

```bash
pip install djangorestframework-simplejwt

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### 2. Endpoints de Autenticação

```bash
# Obter token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "senha"}'

# Usar token
curl -H "Authorization: Bearer seu_token_aqui" \
  http://localhost:8000/api/usuarios/
```

### 3. Rate Limiting

```bash
pip install django-ratelimit

# Aplicar rate limiting nos views
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/m', method='POST')
def create_user(request):
    # view logic
```

## 🚀 Deploy

### 1. Deploy com Heroku

```bash
# Instalar Heroku CLI
# Criar Procfile
echo "web: gunicorn projeto.wsgi --log-file -" > Procfile

# Deploy
heroku create material-didatico-api
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=sua_chave_secreta
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 2. Deploy com AWS

```bash
# Usar AWS Elastic Beanstalk
pip install awsebcli
eb init
eb create production
eb deploy
```

## 📚 Recursos Adicionais

### Documentação
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [Django Filters](https://django-filter.readthedocs.io/)

### Ferramentas Úteis
- **Postman**: Para teste de APIs
- **Insomnia**: Alternativa ao Postman  
- **DBeaver**: Cliente de banco de dados
- **Redis Commander**: Interface web para Redis

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

- **Email**: dev@educacao.gov.br
- **Documentação**: http://localhost:8000/api/docs/
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/material-didatico-api/issues)

---

**Desenvolvido com ❤️ pela Equipe de TI da Secretaria de Educação**