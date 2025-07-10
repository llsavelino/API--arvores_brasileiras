# Configuração da API Árvores Brasileiras v2.0.0

## Configuração Rápida

### 1. Variáveis de Ambiente (Recomendado)

**Linux/Mac:**
```bash
export SQL_SERVER=localhost
export SQL_DATABASE=ArvoresBrasileiras
export SQL_USERNAME=api_user
export SQL_PASSWORD=MinhaSenh@123
export SQL_DRIVER="ODBC Driver 17 for SQL Server"
export FLASK_ENV=development
```

**Windows (CMD):**
```cmd
set SQL_SERVER=localhost
set SQL_DATABASE=ArvoresBrasileiras
set SQL_USERNAME=api_user
set SQL_PASSWORD=MinhaSenh@123
set SQL_DRIVER=ODBC Driver 17 for SQL Server
set FLASK_ENV=development
```

**Windows (PowerShell):**
```powershell
$env:SQL_SERVER="localhost"
$env:SQL_DATABASE="ArvoresBrasileiras"
$env:SQL_USERNAME="api_user"
$env:SQL_PASSWORD="MinhaSenh@123"
$env:SQL_DRIVER="ODBC Driver 17 for SQL Server"
$env:FLASK_ENV="development"
```

### 2. Arquivo .env (Alternativo)

Crie um arquivo `.env` na raiz do projeto:

```env
SQL_SERVER=localhost
SQL_DATABASE=ArvoresBrasileiras
SQL_USERNAME=api_user
SQL_PASSWORD=MinhaSenh@123
SQL_DRIVER=ODBC Driver 17 for SQL Server
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-aqui
```

## Configurações por Ambiente

### Desenvolvimento
```bash
export FLASK_ENV=development
export SQL_SERVER=localhost
export SQL_DATABASE=ArvoresBrasileiras
```

### Produção
```bash
export FLASK_ENV=production
export SQL_SERVER=servidor-producao.empresa.com
export SQL_DATABASE=ArvoresBrasileiras
export SQL_USERNAME=api_prod_user
export SQL_PASSWORD=SenhaSeguraProducao123!
```

### Teste
```bash
export FLASK_ENV=testing
export SQL_DATABASE=ArvoresBrasileiras_Test
```

## Configuração do SQL Server

### 1. Criar Usuário Específico para a API

```sql
-- Conectar como administrador (sa)
USE master;
GO

-- Criar login
CREATE LOGIN api_user WITH PASSWORD = 'MinhaSenh@123';
GO

-- Usar o banco de dados
USE ArvoresBrasileiras;
GO

-- Criar usuário no banco
CREATE USER api_user FOR LOGIN api_user;
GO

-- Conceder permissões (desenvolvimento)
ALTER ROLE db_owner ADD MEMBER api_user;
GO

-- OU para produção (permissões mais restritivas)
-- ALTER ROLE db_datareader ADD MEMBER api_user;
-- ALTER ROLE db_datawriter ADD MEMBER api_user;
-- GO
```

### 2. Verificar Drivers ODBC Instalados

**Windows:**
```cmd
# Listar drivers disponíveis
odbcad32.exe
```

**Linux:**
```bash
# Verificar drivers instalados
odbcinst -q -d

# Instalar driver se necessário (Ubuntu/Debian)
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

### 3. Testar Conexão Manual

**Python:**
```python
import pyodbc

# String de conexão
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=ArvoresBrasileiras;"
    "UID=api_user;"
    "PWD=MinhaSenh@123;"
    "TrustServerCertificate=yes;"
    "Encrypt=no;"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print("Conexão bem-sucedida:", result[0])
    conn.close()
except Exception as e:
    print("Erro na conexão:", e)
```

## Configuração de Rede

### Habilitar TCP/IP no SQL Server

1. Abra **SQL Server Configuration Manager**
2. Vá para **SQL Server Network Configuration** > **Protocols for MSSQLSERVER**
3. Habilite **TCP/IP**
4. Clique duas vezes em **TCP/IP** > **IP Addresses**
5. Na seção **IPAll**, configure:
   - **TCP Dynamic Ports**: (deixe vazio)
   - **TCP Port**: 1433
6. Reinicie o serviço SQL Server

### Firewall (se necessário)

**Windows:**
```cmd
# Abrir porta 1433
netsh advfirewall firewall add rule name="SQL Server" dir=in action=allow protocol=TCP localport=1433
```

**Linux:**
```bash
# UFW
sudo ufw allow 1433/tcp

# iptables
sudo iptables -A INPUT -p tcp --dport 1433 -j ACCEPT
```

## Solução de Problemas Comuns

### Erro: "Driver not found"
- Instale o ODBC Driver 17 for SQL Server
- Verifique o nome exato do driver: `odbcinst -q -d`

### Erro: "Login failed"
- Verifique usuário e senha
- Confirme se o usuário tem permissões no banco
- Teste conexão manual

### Erro: "Server not found"
- Verifique se SQL Server está rodando
- Confirme nome/IP do servidor
- Teste conectividade de rede: `telnet servidor 1433`

### Erro: "Database not found"
- Confirme se o banco `ArvoresBrasileiras` existe
- Verifique se o usuário tem acesso ao banco

## Configuração para Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc \
    unixodbc-dev

# Instalar ODBC Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copiar aplicação
WORKDIR /app
COPY . .

# Instalar dependências Python
RUN pip install -r requirements.txt

# Configurar variáveis de ambiente
ENV SQL_DRIVER="ODBC Driver 17 for SQL Server"

EXPOSE 5000
CMD ["python", "src/main.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SQL_SERVER=sqlserver
      - SQL_DATABASE=ArvoresBrasileiras
      - SQL_USERNAME=sa
      - SQL_PASSWORD=MinhaSenh@123
      - FLASK_ENV=development
    depends_on:
      - sqlserver

  sqlserver:
    image: mcr.microsoft.com/mssql/server:2019-latest
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=MinhaSenh@123
    ports:
      - "1433:1433"
    volumes:
      - sqldata:/var/opt/mssql

volumes:
  sqldata:
```

## Configuração de Produção

### Segurança
- Use senhas fortes
- Configure SSL/TLS
- Restrinja permissões do usuário da API
- Use variáveis de ambiente para credenciais

### Performance
- Configure pool de conexões
- Otimize queries
- Monitore logs
- Configure backup automático

### Monitoramento
```bash
# Health check
curl http://localhost:5000/api/health

# Teste de banco
curl http://localhost:5000/api/database/test

# Informações da API
curl http://localhost:5000/api/info
```

