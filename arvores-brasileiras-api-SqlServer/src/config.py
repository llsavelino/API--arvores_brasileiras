import os

class Config:
    """Configuração base da aplicação"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'arvores-brasileiras-secret-key-2024'
    
    # Configurações do SQL Server
    SQL_SERVER = os.environ.get('SQL_SERVER') or 'FRA0685193W11-1\SQLEXPRESS'
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or 'ArvoresBrasileiras'
    SQL_USERNAME = os.environ.get('SQL_USERNAME') or 'sa'
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or '1234567890'
    SQL_DRIVER = os.environ.get('SQL_DRIVER') or 'ODBC Driver 17 for SQL Server'
    
    # Configurações da aplicação
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    """Retorna a string de conexão formatada"""
    @staticmethod
    def get_connection_string():
        return (
            f"DRIVER={{{Config.SQL_DRIVER}}}; "f"SERVER={Config.SQL_SERVER};"
            f"DATABASE={Config.SQL_DATABASE}; "f"UID={Config.SQL_USERNAME};"
            f"PWD={Config.SQL_PASSWORD};" f"TrustServerCertificate=yes;"
            f"Encrypt=no;"
        )

"""Configuração para desenvolvimento"""
class DevelopmentConfig(Config): DEBUG = True
"""Configuração para produção"""
class ProductionConfig(Config): DEBUG = False
"""Configuração para testes"""
class TestingConfig(Config):
    DEBUG = True
    SQL_DATABASE = 'ArvoresBrasileiras_Test'

# Dicionário de configurações
config = {
    'development': DevelopmentConfig, 'production': ProductionConfig,
    'testing': TestingConfig, 'default': DevelopmentConfig
}