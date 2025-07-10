# API Árvores Brasileiras v2.0.0 (pyodbc)

Uma API Flask refatorada para gerenciamento de dados sobre árvores brasileiras, utilizando **pyodbc** para conexão direta com SQL Server, sem dependência do SQLAlchemy.

## Principais Mudanças na v2.0.0

- ✅ **Removido SQLAlchemy**: Substituído por pyodbc para conexão direta com SQL Server
- ✅ **Removido SQLite**: Suporte exclusivo ao SQL Server
- ✅ **Arquitetura simplificada**: Menos dependências e maior controle sobre as consultas SQL
- ✅ **Performance otimizada**: Consultas SQL diretas e gerenciamento manual de transações
- ✅ **Mantida compatibilidade**: Todos os endpoints e funcionalidades da v1.0.0 preservados

## Características

- **CRUD Completo**: Operações GET, POST, PUT, PATCH, DELETE e HEAD para todas as tabelas
- **Modularização**: Utiliza Flask Blueprints para organização das rotas
- **Paginação**: Paginação automática em todas as consultas
- **Filtros**: Filtros dinâmicos baseados em parâmetros de query
- **Relacionamentos**: Suporte a relacionamentos opcionais entre tabelas
- **SQL Server Nativo**: Conexão direta via pyodbc sem ORM
- **CORS**: Configurado para permitir requisições de qualquer origem
- **Transações**: Gerenciamento automático de transações com rollback em caso de erro

## Estrutura do Banco de Dados

### Tabelas

1. **Especies** - Informações sobre espécies de árvores
2. **Biomas** - Dados sobre biomas brasileiros
3. **Ocorrencias** - Relaciona espécies com biomas
4. **Caracteristicas** - Características físicas das espécies
5. **Curiosidades** - Curiosidades sobre as espécies
6. **DadosArvore** - Dados técnicos das árvores

## Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- SQL Server
- ODBC Driver 17 for SQL Server (ou superior)

### Instalação

1. Extraia o projeto
2. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Configuração do Banco de Dados

#### 1. Criar o Banco de Dados no SQL Server

Execute o script SQL para criar o banco `ArvoresBrasileiras` e suas tabelas:

```sql
-- Criação do banco de dados
CREATE DATABASE ArvoresBrasileiras;
GO

USE ArvoresBrasileiras;
GO

-- [Script completo das tabelas conforme fornecido anteriormente]
```

#### 2. Configurar Variáveis de Ambiente

Configure as variáveis de ambiente para conexão com SQL Server:

```bash
export SQL_SERVER=localhost
export SQL_DATABASE=ArvoresBrasileiras
export SQL_USERNAME=seu_usuario
export SQL_PASSWORD=sua_senha
export SQL_DRIVER="ODBC Driver 17 for SQL Server"
```

**Ou no Windows:**
```cmd
set SQL_SERVER=localhost
set SQL_DATABASE=ArvoresBrasileiras
set SQL_USERNAME=seu_usuario
set SQL_PASSWORD=sua_senha
set SQL_DRIVER=ODBC Driver 17 for SQL Server
```

#### 3. Configuração Alternativa

Se preferir, você pode editar diretamente o arquivo `src/config.py` com suas configurações.

### Executando a API

```bash
python src/main.py
```

A API estará disponível em `http://localhost:5000`

## Endpoints da API

### Endpoints de Sistema

- `GET /api/health` - Verificação de saúde da API e conexão com banco
- `GET /api/info` - Informações detalhadas sobre a API
- `GET /api/database/test` - Teste específico de conexão com banco de dados

### Endpoints CRUD (Todas as Tabelas)

Cada tabela possui os seguintes endpoints padrão:

#### Especies
- `GET /api/especies` - Lista todas as espécies
- `GET /api/especies/{id}` - Obtém uma espécie específica
- `POST /api/especies` - Cria uma nova espécie
- `PUT /api/especies/{id}` - Atualiza completamente uma espécie
- `PATCH /api/especies/{id}` - Atualiza parcialmente uma espécie
- `DELETE /api/especies/{id}` - Remove uma espécie
- `HEAD /api/especies` - Retorna headers com contagem total
- `HEAD /api/especies/{id}` - Verifica se uma espécie existe

**Rotas Auxiliares:**
- `GET /api/especies/search?nome={nome}` - Busca por nome científico ou popular
- `GET /api/especies/familia/{familia}` - Lista espécies por família

#### Biomas
- `GET /api/biomas` - Lista todos os biomas
- `GET /api/biomas/{id}` - Obtém um bioma específico
- `POST /api/biomas` - Cria um novo bioma
- `PUT /api/biomas/{id}` - Atualiza completamente um bioma
- `PATCH /api/biomas/{id}` - Atualiza parcialmente um bioma
- `DELETE /api/biomas/{id}` - Remove um bioma
- `HEAD /api/biomas` - Retorna headers com contagem total
- `HEAD /api/biomas/{id}` - Verifica se um bioma existe

**Rotas Auxiliares:**
- `GET /api/biomas/regiao/{regiao}` - Lista biomas por região
- `GET /api/biomas/search?nome={nome}` - Busca biomas por nome

#### Ocorrencias
- `GET /api/ocorrencias` - Lista todas as ocorrências
- `GET /api/ocorrencias/{id}` - Obtém uma ocorrência específica
- `POST /api/ocorrencias` - Cria uma nova ocorrência
- `PUT /api/ocorrencias/{id}` - Atualiza completamente uma ocorrência
- `PATCH /api/ocorrencias/{id}` - Atualiza parcialmente uma ocorrência
- `DELETE /api/ocorrencias/{id}` - Remove uma ocorrência
- `HEAD /api/ocorrencias` - Retorna headers com contagem total
- `HEAD /api/ocorrencias/{id}` - Verifica se uma ocorrência existe

**Rotas Auxiliares:**
- `GET /api/ocorrencias/especie/{especie_id}` - Lista ocorrências por espécie
- `GET /api/ocorrencias/bioma/{bioma_id}` - Lista ocorrências por bioma
- `GET /api/ocorrencias/frequencia/{frequencia}` - Lista por frequência

#### Caracteristicas
- `GET /api/caracteristicas` - Lista todas as características
- `GET /api/caracteristicas/{id}` - Obtém uma característica específica
- `POST /api/caracteristicas` - Cria uma nova característica
- `PUT /api/caracteristicas/{id}` - Atualiza completamente uma característica
- `PATCH /api/caracteristicas/{id}` - Atualiza parcialmente uma característica
- `DELETE /api/caracteristicas/{id}` - Remove uma característica
- `HEAD /api/caracteristicas` - Retorna headers com contagem total
- `HEAD /api/caracteristicas/{id}` - Verifica se uma característica existe

**Rotas Auxiliares:**
- `GET /api/caracteristicas/especie/{especie_id}` - Lista características por espécie
- `GET /api/caracteristicas/tipo-folha/{tipo_folha}` - Lista por tipo de folha
- `GET /api/caracteristicas/altura-range?min={min}&max={max}` - Lista por faixa de altura

#### Curiosidades
- `GET /api/curiosidades` - Lista todas as curiosidades
- `GET /api/curiosidades/{id}` - Obtém uma curiosidade específica
- `POST /api/curiosidades` - Cria uma nova curiosidade
- `PUT /api/curiosidades/{id}` - Atualiza completamente uma curiosidade
- `PATCH /api/curiosidades/{id}` - Atualiza parcialmente uma curiosidade
- `DELETE /api/curiosidades/{id}` - Remove uma curiosidade
- `HEAD /api/curiosidades` - Retorna headers com contagem total
- `HEAD /api/curiosidades/{id}` - Verifica se uma curiosidade existe

**Rotas Auxiliares:**
- `GET /api/curiosidades/especie/{especie_id}` - Lista curiosidades por espécie
- `GET /api/curiosidades/search?texto={texto}` - Busca por texto
- `GET /api/curiosidades/fonte/{fonte}` - Lista por fonte

#### Dados Arvore
- `GET /api/dados-arvore` - Lista todos os dados de árvore
- `GET /api/dados-arvore/{id}` - Obtém dados específicos
- `POST /api/dados-arvore` - Cria novos dados
- `PUT /api/dados-arvore/{id}` - Atualiza completamente
- `PATCH /api/dados-arvore/{id}` - Atualiza parcialmente
- `DELETE /api/dados-arvore/{id}` - Remove dados
- `HEAD /api/dados-arvore` - Retorna headers com contagem total
- `HEAD /api/dados-arvore/{id}` - Verifica se dados existem

**Rotas Auxiliares:**
- `GET /api/dados-arvore/especie/{especie_id}` - Lista dados por espécie
- `GET /api/dados-arvore/tempo-vida-range?min={min}&max={max}` - Por tempo de vida
- `GET /api/dados-arvore/crescimento-range?min={min}&max={max}` - Por crescimento
- `GET /api/dados-arvore/densidade-range?min={min}&max={max}` - Por densidade

## Parâmetros de Query

### Paginação
- `page` - Número da página (padrão: 1)
- `per_page` - Itens por página (padrão: 100, máximo: 1000)

### Relacionamentos
- `include_relationships=true` - Inclui dados relacionados na resposta

### Filtros Dinâmicos
Qualquer campo do modelo pode ser usado como filtro. Exemplo:
- `GET /api/especies?Familia=Urticaceae`
- `GET /api/biomas?Regiao=Sudeste`

## Exemplos de Uso

### Testar Conexão
```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/database/test
```

### Criar uma Espécie
```bash
curl -X POST http://localhost:5000/api/especies \
  -H "Content-Type: application/json" \
  -d '{
    "NomeCientifico": "Cecropia pachystachya",
    "NomePopular": "Embaúba",
    "Familia": "Urticaceae",
    "Descricao": "Árvore pioneira de crescimento rápido"
  }'
```

### Buscar Espécies por Nome
```bash
curl "http://localhost:5000/api/especies/search?nome=embauba"
```

### Listar com Relacionamentos
```bash
curl "http://localhost:5000/api/especies/1?include_relationships=true"
```

### Paginação
```bash
curl "http://localhost:5000/api/especies?page=2&per_page=50"
```

## Arquitetura da v2.0.0

### Estrutura do Projeto

```
arvores-brasileiras-api-pyodbc/
├── src/
│   ├── database/
│   │   └── connection.py      # Gerenciamento de conexões pyodbc
│   ├── models/
│   │   ├── base_model.py      # Classe base para modelos
│   │   ├── especies.py        # Modelo Especies
│   │   ├── biomas.py          # Modelo Biomas
│   │   ├── ocorrencias.py     # Modelo Ocorrencias
│   │   ├── caracteristicas.py # Modelo Caracteristicas
│   │   ├── curiosidades.py    # Modelo Curiosidades
│   │   └── dados_arvore.py    # Modelo DadosArvore
│   ├── routes/
│   │   ├── base_crud.py       # Classe base para CRUD
│   │   ├── especies.py        # Blueprint Especies
│   │   ├── biomas.py          # Blueprint Biomas
│   │   ├── ocorrencias.py     # Blueprint Ocorrencias
│   │   ├── caracteristicas.py # Blueprint Caracteristicas
│   │   ├── curiosidades.py    # Blueprint Curiosidades
│   │   └── dados_arvore.py    # Blueprint DadosArvore
│   ├── static/                # Arquivos estáticos
│   ├── config.py              # Configurações da aplicação
│   └── main.py                # Arquivo principal
├── venv/                      # Ambiente virtual Python
├── requirements.txt           # Dependências
└── README.md                  # Esta documentação
```

### Principais Componentes

#### 1. DatabaseConnection (`src/database/connection.py`)
- Gerencia conexões com SQL Server via pyodbc
- Context managers para transações automáticas
- Pool de conexões e tratamento de erros
- Métodos para teste de conectividade

#### 2. BaseModel (`src/models/base_model.py`)
- Classe abstrata base para todos os modelos
- Operações CRUD genéricas
- Paginação e filtros automáticos
- Gerenciamento de relacionamentos

#### 3. BaseCRUD (`src/routes/base_crud.py`)
- Classe base para endpoints CRUD
- Tratamento padronizado de erros
- Validação de parâmetros
- Formatação de respostas JSON

#### 4. Blueprints Modulares
- Cada tabela possui seu próprio blueprint
- Rotas auxiliares específicas por domínio
- Documentação inline das rotas

## Vantagens da v2.0.0

### Performance
- **Consultas SQL diretas**: Sem overhead do ORM
- **Controle total**: Otimização manual de queries
- **Transações eficientes**: Gerenciamento direto de commits/rollbacks

### Simplicidade
- **Menos dependências**: Apenas Flask, pyodbc e Flask-CORS
- **Código mais direto**: SQL explícito e transparente
- **Debugging facilitado**: Logs detalhados de todas as operações

### Flexibilidade
- **SQL customizado**: Facilidade para queries complexas
- **Stored procedures**: Suporte nativo se necessário
- **Configuração granular**: Controle total sobre conexões

## Migração da v1.0.0

Se você estava usando a versão anterior com SQLAlchemy:

1. **Backup dos dados**: Faça backup do seu banco de dados
2. **Atualize variáveis de ambiente**: Configure as novas variáveis SQL_*
3. **Teste a conexão**: Use `/api/database/test` para verificar
4. **Endpoints inalterados**: Todos os endpoints mantêm compatibilidade

## Tratamento de Erros

A API retorna códigos de status HTTP apropriados:

- `200` - Sucesso
- `201` - Criado com sucesso
- `400` - Erro de validação ou dados inválidos
- `404` - Recurso não encontrado
- `500` - Erro interno do servidor
- `503` - Serviço indisponível (problemas de banco)

Exemplo de resposta de erro:
```json
{
  "error": "Registro não encontrado",
  "traceback": "..." // Apenas em modo debug
}
```

## Monitoramento

### Health Check
```bash
curl http://localhost:5000/api/health
```

Retorna status da API e conexão com banco de dados.

### Logs
A aplicação gera logs detalhados de todas as operações:
- Conexões com banco de dados
- Execução de queries
- Erros e exceções
- Transações

## Desenvolvimento

### Adicionando Novos Endpoints

1. Crie o modelo em `src/models/` herdando de `BaseModel`
2. Crie o blueprint em `src/routes/` usando `BaseCRUD`
3. Registre o blueprint em `src/main.py`
4. Atualize a documentação

### Customizando Queries

Para queries específicas, adicione métodos nos modelos:

```python
def custom_query(self, param):
    try:
        query = "SELECT * FROM MinhaTabela WHERE campo = ?"
        with db_connection.get_cursor() as (cursor, connection):
            cursor.execute(query, [param])
            rows = cursor.fetchall()
            return [self.to_dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Erro na query customizada: {e}")
        raise
```

## Licença

Este projeto foi desenvolvido para gerenciamento de dados sobre árvores brasileiras.

