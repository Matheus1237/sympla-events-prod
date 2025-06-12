# Sympla Events Integration

Este projeto é uma aplicação Django que integra com a API do Sympla para importar e gerenciar eventos. Ele oferece uma API REST para consulta dos eventos importados e mantém um histórico de importações.

## 📸 Screenshots

### Dashboard de Eventos
![Dashboard de Eventos](docs/assets/image.png)

### Detalhes do Evento
![Detalhes do Evento](docs/assets/image02.png)

### Logs de Importação
![Logs de Importação](docs/assets/image03.png)

## 🚀 Tecnologias

- Python 3.11
- Django 5.2
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker & Docker Compose

## 🌟 Funcionalidades

- ✅ Integração com a API do Sympla
- ✅ Importação automática de eventos
- ✅ API REST para consulta de eventos
- ✅ Histórico de importações
- ✅ Tratamento de erros e logging
- ✅ Suporte a paginação
- ✅ Containerização com Docker

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Git

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone git@github.com:Matheus1237/sympla-events-prod.git
cd sympla-events-prod
```

2. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```

3. Configure as variáveis de ambiente no arquivo `.env`:
```env
# Django settings
DJANGO_SECRET_KEY=sua_chave_secreta_aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
POSTGRES_NAME=sympla_events
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Sympla API settings
SYMPLA_API_KEY=seu_token_da_api_do_sympla
```

4. Inicie os containers:
```bash
docker-compose up -d
```

5. Execute as migrações:
```bash
docker-compose exec web python manage.py migrate
```

6. Importe os eventos do Sympla:
```bash
docker-compose exec web python manage.py import_events
```

## 🌐 Acessando a Aplicação

Após a instalação, você pode acessar:

- API de Eventos: http://localhost:8000/events/
- API de Logs de Importação: http://localhost:8000/import-logs/

## 📝 Estrutura do Projeto

```
sympla-events-prod/
├── events/                    # Aplicação principal
│   ├── management/           # Comandos personalizados
│   ├── migrations/           # Migrações do banco de dados
│   ├── services/            # Serviços de integração
│   ├── models.py            # Modelos do Django
│   ├── serializers.py       # Serializers da API
│   ├── views.py             # Views da API
│   └── urls.py              # URLs da API
├── sympla_events/           # Configurações do projeto
├── docker-compose.yml       # Configuração do Docker Compose
├── Dockerfile              # Configuração do container
└── requirements.txt        # Dependências Python
```

## 🔑 Obtendo Token da API do Sympla

1. Faça login na sua conta do Sympla
2. Acesse o menu "Minha Conta"
3. Navegue até a aba "Integrações"
4. Clique em "Criar chave de acesso"
5. Copie o token gerado e adicione ao seu arquivo `.env`

## 📊 Modelos de Dados

### Event
- `sympla_id`: ID do evento no Sympla
- `name`: Nome do evento
- `start_date`: Data e hora de início (formato: DD/MM/YYYY HH:MM)
- `venue`: Local do evento (relacionamento)
- `category`: Categoria do evento (relacionamento)
- `raw_data`: Dados brutos do evento
- `import_version`: Versão da importação
- `created_at`: Data de criação do registro
- `updated_at`: Data da última atualização

### Venue
- `sympla_id`: ID do local no Sympla
- `name`: Nome do local
- `address`: Endereço completo
- `city`: Cidade
- `state`: Estado
- `country`: País

### Category
- `name`: Nome da categoria
- `created_at`: Data de criação

### ImportLog
- `version`: Versão da importação
- `status`: Status da importação (SUCCESS, ERROR)
- `imported_count`: Quantidade de eventos importados
- `error_message`: Mensagem de erro (se houver)
- `created_at`: Data da importação
- `duration`: Duração da importação em segundos

## 🔄 API Endpoints

### Events
- `GET /events/`: Lista todos os eventos
  - Suporta paginação (page_size=10 por padrão)
  - Formato de data: DD/MM/YYYY HH:MM
  - Inclui informações do local e categoria
  - Filtros disponíveis:
    - `?name=`: Filtra por nome do evento
    - `?category=`: Filtra por categoria
    - `?start_date_after=`: Eventos após data
    - `?start_date_before=`: Eventos antes da data

### Import Logs
- `GET /import-logs/`: Lista todos os logs de importação
  - Ordenado por data de criação (mais recente primeiro)
  - Mostra status e quantidade de eventos importados
  - Filtros disponíveis:
    - `?status=`: Filtra por status (SUCCESS/ERROR)
    - `?date=`: Filtra por data da importação

## 🐳 Comandos Docker Úteis

```bash
# Visualizar logs
docker-compose logs -f web

# Executar migrations
docker-compose exec web python manage.py migrate

# Importar eventos
docker-compose exec web python manage.py import_events

# Reiniciar serviços
docker-compose restart

# Parar todos os serviços
docker-compose down

# Limpar volumes (cuidado: apaga dados do banco)
docker-compose down -v
```