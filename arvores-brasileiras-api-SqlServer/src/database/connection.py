import pyodbc
import os
from contextlib import contextmanager
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Classe para gerenciar conexões com SQL Server usando pyodbc"""
    
    def __init__(self): self.connection_string = self._build_connection_string()
        
    def _build_connection_string(self):
        """Constrói a string de conexão baseada em variáveis de ambiente ou configuração padrão"""
        
        # Configurações do SQL Server
        server = os.environ.get('SQL_SERVER', 'FRA0685193W11-1\SQLEXPRESS')
        database = os.environ.get('SQL_DATABASE', 'ArvoresBrasileiras')
        username = os.environ.get('SQL_USERNAME', 'sa')
        password = os.environ.get('SQL_PASSWORD', '1234567890')
        driver = os.environ.get('SQL_DRIVER', 'ODBC Driver 17 for SQL Server')
        
        # Construir string de conexão
        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
            f"Encrypt=no;"
        )
        
        logger.info(f"String de conexão configurada para servidor: {server}, banco: {database}")
        return connection_string
    
    def get_connection(self):
        """Retorna uma nova conexão com o banco de dados"""
        try:
            connection = pyodbc.connect(self.connection_string)
            connection.autocommit = False  # Controle manual de transações
            return connection
        except pyodbc.Error as e:
            logger.error(f"Erro ao conectar com o banco de dados: {e}")
            raise
    
    @contextmanager
    def get_cursor(self):
        """Context manager para obter cursor com gerenciamento automático de conexão"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            yield cursor, connection
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Erro na operação do banco de dados: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @contextmanager
    def get_transaction(self):
        """Context manager para transações com commit/rollback automático"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except Exception as e:
            if connection: connection.rollback()
            logger.error(f"Erro na transação: {e}")
            raise
        finally:
            if connection or cursor: 
                cursor.close()
                connection.close()
    
    def test_connection(self):
        """Testa a conexão com o banco de dados"""
        try:
            with self.get_cursor() as (cursor, connection):
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                logger.info("Conexão com banco de dados testada com sucesso")
                return True
        except Exception as e:
            logger.error(f"Falha no teste de conexão: {e}")
            return False
    
    def execute_script(self, script_path):
        """Executa um script SQL a partir de um arquivo"""
        try:
            with open(script_path, 'r', encoding='utf-8') as file: script = file.read()
            
            with self.get_transaction() as cursor:
                # Dividir script em comandos individuais
                commands = [cmd.strip() for cmd in script.split('GO') if cmd.strip()]
                
                for command in commands:
                    if command: cursor.execute(command)
                        
            logger.info(f"Script {script_path} executado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao executar script {script_path}: {e}")
            return False

# Instância global da conexão
db_connection = DatabaseConnection()

