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

- **Django 5.2.6** - Framework web
- **Django REST Framework 3.16** - API REST
- **drf-spectacular** - Documentação OpenAPI/Swagger
- **django-filter** - Filtros avançados
- **PostgreSQL** - Banco de dados


## 🚀 Instalação e Configuração

### 1. Clone o Repositório

```bash
git clone https://github.com/Kovokar/Sistema-de-Gest-o-de-Materiais-Did-ticos.git
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2.1 Usando UV

```bash
# Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Baixar Dependências
uv sync

# Rodar Server 
uv run python manage.py runserver
```


### 3. Instale as Dependências (pule se estiver usando UV)

```bash
pip install -r requirements.txt
```


### 5. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
DB_HOST=HOST-EX
DB_PORT=PORT-EX
DB_NAME=NAME-EX
DB_USER=USER-EX
DB_PASSWORD=PWD-EX
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

### 9. Execute o Servidor de Desenvolvimento

```bash
python manage.py runserver
# ou ocm uv
uv run python manage.py runserver
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


## 📚 Recursos Adicionais

### Documentação
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [Django Filters](https://django-filter.readthedocs.io/)

### Ferramentas Úteis
- **Postman**: Para teste de APIs
- **Insomnia**: Alternativa ao Postman  
- **DBeaver**: Cliente de banco de dados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

<!-- ## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes. -->

<!-- ## 📞 Suporte

- **Email**: pkovokar
- **Documentação**: http://localhost:8000/api/docs/
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/material-didatico-api/issues)

--- -->

**Desenvolvido com ❤️ pela Equipe de TI da Secretaria de Educação**