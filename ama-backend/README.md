# CSN Server

En FastAPI-basert server for CSN (Consciousness Synchronization Network) med integrerte moduler for MCP-protokoll, Firestore AMA-operasjoner, agent-koordinering og biofelt-validering.

## Funksjoner

- **MCP Endpoints**: Implementasjon av Model Context Protocol for AI-agent kommunikasjon
- **AMA Integration**: Firestore-basert Advanced Medical Analytics operasjoner
- **Agent Coordination**: Agent-til-agent kommunikasjon med WebSocket-støtte
- **Biofield Validation**: HRV-basert validering av biofelt-data
- **Docker Support**: Komplett containerisering med docker-compose
- **Structured Logging**: Omfattende logging med structlog
- **Health Checks**: Kubernetes-vennlige health endpoints
- **Configuration Management**: Miljøvariabel-basert konfigurasjon

## Prosjektstruktur

```
csn_server/
├── csn_server/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Konfigurasjonshåndtering
│   └── routers/
│       ├── __init__.py
│       ├── health.py           # Health check endpoints
│       ├── mcp_endpoints.py    # MCP protocol endpoints
│       ├── ama_integration.py  # Firestore AMA operations
│       ├── agent_coordination.py # Agent communication
│       └── biofelt_validation.py # HRV-based validation
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container
├── docker-compose.yml          # Local development setup
├── env.example                 # Environment variables template
└── README.md                   # This file
```

## Installasjon og Oppsett

### Forutsetninger

- Python 3.11+
- Docker og Docker Compose (for containerisert kjøring)
- Redis (for agent coordination)
- Google Cloud Project (for Firestore AMA integration)

### Lokal Utvikling

1. **Klon repositoriet**
   ```bash
   git clone <repository-url>
   cd csn_server
   ```

2. **Opprett virtuelt miljø**
   ```bash
   python -m venv venv
   source venv/bin/activate  # På Windows: venv\Scripts\activate
   ```

3. **Installer dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurer miljøvariabler**
   ```bash
   cp env.example .env
   # Rediger .env med dine spesifikke verdier
   ```

5. **Start serveren**
   ```bash
   python -m csn_server.main
   ```

### Docker Setup

1. **Bygg og start med Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Kjør i bakgrunnen**
   ```bash
   docker-compose up -d
   ```

3. **Se logger**
   ```bash
   docker-compose logs -f csn_server
   ```

## Konfigurasjon

### Miljøvariabler

Kopier `env.example` til `.env` og konfigurer følgende:

#### Grunnleggende Konfigurasjon
```bash
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key-here
```

#### Server Konfigurasjon
```bash
HOST=0.0.0.0
PORT=8000
WORKERS=1
```

#### Database
```bash
DATABASE_URL=sqlite:///./csn_server.db
REDIS_URL=redis://localhost:6379/0
```

#### Google Cloud / Firestore
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
FIRESTORE_COLLECTION_PREFIX=csn
```

#### MCP Konfigurasjon
```bash
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=3000
MCP_CLIENT_ID=csn_server
MCP_CLIENT_SECRET=your-mcp-client-secret
```

#### Agent Koordinering
```bash
AGENT_COORDINATION_ENABLED=true
AGENT_BROKER_URL=redis://localhost:6379/1
AGENT_QUEUE_PREFIX=csn_agent
WEBSOCKET_ENABLED=true
WEBSOCKET_PORT=8001
```

#### Biofelt Validering
```bash
HRV_VALIDATION_ENABLED=true
HRV_SAMPLE_RATE=1000
HRV_MIN_SEGMENT_LENGTH=300
HRV_MAX_SEGMENT_LENGTH=3000
```

## API Endpoints

### Health Checks
- `GET /health/` - Grunnleggende health check
- `GET /health/ready` - Readiness check for Kubernetes
- `GET /health/live` - Liveness check for Kubernetes
- `GET /health/info` - Service informasjon

### MCP Endpoints
- `POST /mcp/connect` - Etabler MCP tilkobling
- `POST /mcp/disconnect` - Avslutt MCP tilkobling
- `POST /mcp/call` - Utfør MCP metodekall
- `GET /mcp/connections` - List MCP tilkoblinger
- `GET /mcp/status` - MCP service status

### AMA Integration
- `POST /ama/data` - Opprett AMA data
- `POST /ama/batch` - Batch AMA operasjoner
- `POST /ama/query` - Spør AMA data
- `POST /ama/sync` - Synkroniser AMA data
- `GET /ama/collections` - List AMA collections
- `GET /ama/status` - AMA service status

### Agent Coordination
- `POST /agents/register` - Registrer agent
- `POST /agents/unregister` - Avregistrer agent
- `POST /agents/message` - Send agent melding
- `POST /agents/broadcast` - Broadcast melding
- `GET /agents/agents` - List registrerte agenter
- `GET /agents/agents/{agent_id}` - Hent agent informasjon
- `GET /agents/messages` - Hent meldingshistorikk
- `GET /agents/status` - Agent koordinering status
- `WS /agents/ws/{agent_id}` - WebSocket for real-time kommunikasjon

### Biofield Validation
- `POST /biofield/validate` - Valider biofelt data
- `POST /biofield/analyze` - Utfør HRV analyse
- `GET /biofield/metrics` - Hent HRV metrics
- `GET /biofield/config` - Hent HRV konfigurasjon
- `GET /biofield/status` - Biofelt validering status

## Utvikling

### Testing

```bash
# Kjør tester
pytest

# Kjør tester med coverage
pytest --cov=csn_server

# Kjør spesifikke tester
pytest tests/test_mcp_endpoints.py
```

### Linting og Formatting

```bash
# Format kode
black csn_server/

# Sort imports
isort csn_server/

# Lint kode
flake8 csn_server/

# Type checking
mypy csn_server/
```

## Docker

### Bygg Image

```bash
docker build -t csn_server .
```

### Kjør Container

```bash
docker run -p 8000:8000 --env-file .env csn_server
```

### Docker Compose Services

- **csn_server**: Hovedapplikasjonen
- **redis**: Cache og message broker
- **firestore_emulator**: Lokal Firestore for utvikling

## Monitoring

### Health Checks

Serveren eksponerer flere health check endpoints:

- `/health/` - Grunnleggende status
- `/health/ready` - Readiness for Kubernetes
- `/health/live` - Liveness for Kubernetes

### Logging

Strukturerte logger med structlog:

```python
import structlog

logger = structlog.get_logger()
logger.info("Event", key="value", another_key=123)
```

### Metrics

Prometheus metrics er tilgjengelige på `/metrics` (hvis aktivert).

## Sikkerhet

### Autentisering

- JWT-basert autentisering for API endpoints
- MCP token validering
- CORS konfigurasjon

### Miljøvariabler

- Aldri commit `.env` filer
- Bruk `env.example` som template
- Roter secrets regelmessig

## Deployment

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: csn-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: csn-server
  template:
    metadata:
      labels:
        app: csn-server
    spec:
      containers:
      - name: csn-server
        image: csn_server:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
```

### Environment Variables for Production

```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
SECRET_KEY=<strong-secret-key>
ALLOWED_HOSTS=your-domain.com,api.your-domain.com
```

## Bidrag

1. Fork prosjektet
2. Opprett feature branch (`git checkout -b feature/amazing-feature`)
3. Commit endringer (`git commit -m 'Add amazing feature'`)
4. Push til branch (`git push origin feature/amazing-feature`)
5. Opprett Pull Request

## Lisens

Dette prosjektet er lisensiert under MIT License.

## Support

For spørsmål og support:

- Opprett en Issue på GitHub
- Kontakt utviklingsteamet
- Sjekk dokumentasjonen på `/docs` endpoint 