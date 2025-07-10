import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from src.database.connection import db_connection
from src.config import config
from src.routes.especies import especies_bp
from src.routes.biomas import biomas_bp
from src.routes.ocorrencias import ocorrencias_bp
from src.routes.caracteristicas import caracteristicas_bp
from src.routes.curiosidades import curiosidades_bp
from src.routes.dados_arvore import dados_arvore_bp
from src.routes.arvores import arvores_bp
import logging

'''Configuração do logger para registrar informações da aplicação'''
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name: str='default'):
    """Factory function para criar a aplicação Flask"""
    # Apenas Flask(__name__), sem static_folder
    app = Flask(__name__)
    
    # Carregar configuração
    app.config.from_object(config[config_name])
    
    # Configuração CORS para permitir requisições de qualquer origem
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    """Registrar blueprints para rotas da API"""
    app.register_blueprint(especies_bp, url_prefix='/api')
    app.register_blueprint(biomas_bp, url_prefix='/api')
    app.register_blueprint(ocorrencias_bp, url_prefix='/api')
    app.register_blueprint(caracteristicas_bp, url_prefix='/api')
    app.register_blueprint(curiosidades_bp, url_prefix='/api')
    app.register_blueprint(dados_arvore_bp, url_prefix='/api')
    app.register_blueprint(arvores_bp, url_prefix='/api')
    
    @app.route('/')
    def index_home() -> render_template: return render_template('index.html')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Endpoint para verificar se a API está funcionando"""
        try:
            # Testar conexão com banco de dados
            db_status = db_connection.test_connection()
            
            return jsonify({
                'status': 'healthy' if db_status else 'unhealthy',
                'message': 'API Árvores Brasileiras está funcionando',
                'database': 'connected' if db_status else 'disconnected',
                'version': '2.0.0 (pyodbc)'
            }), 200 if db_status else 503
            
        except Exception as e:
            logger.error(f"Erro no health check: {e}")
            return jsonify({
                'status': 'unhealthy', 'message': 'Erro na verificação de saúde', 'error': str(e)
            }), 503
    
    @app.route('/api/info', methods=['GET', 'HEAD'])
    def api_info() -> tuple:
        """Endpoint com informações sobre a API"""
        info = {
            'name': 'API Árvores Brasileiras', 'version': '2.0.0',
            'description': 'API completa para gerenciamento de dados sobre árvores brasileiras usando pyodbc',
            'database': 'SQL Server (pyodbc)',
            'endpoints': {
                'especies': '/api/especies', 'biomas': '/api/biomas', 'ocorrencias': '/api/ocorrencias',
                'caracteristicas': '/api/caracteristicas', 'curiosidades': '/api/curiosidades',
                'dados_arvore': '/api/dados-arvore'
            },
            'methods': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD'],
            'features': [
                'CRUD completo para todas as tabelas',
                'Paginação automática',
                'Filtros dinâmicos',
                'Relacionamentos opcionais',
                'Rotas auxiliares especializadas',
                'Conexão direta com SQL Server via pyodbc',
                'Gerenciamento automático de transações'
            ],
            'configuration': {
                'server': os.environ.get('SQL_SERVER', 'localhost'),
                'database': os.environ.get('SQL_DATABASE', 'ArvoresBrasileiras'),
                'driver': os.environ.get('SQL_DRIVER', 'ODBC Driver 17 for SQL Server')
            }
        }

        return render_template('API_INFO.html', info=info), 200
    
    @app.route('/api/database/test', methods=['GET'])
    def test_database():
        """Endpoint para testar conexão com banco de dados"""
        try:
            success = db_connection.test_connection()
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Conexão com banco de dados estabelecida com sucesso',
                    'server': os.environ.get('SQL_SERVER', 'localhost'),
                    'database': os.environ.get('SQL_DATABASE', 'ArvoresBrasileiras')
                }), 200
            else: return jsonify({'status': 'error', 'message': 'Falha na conexão com banco de dados'}), 503
                
        except Exception as e:
            logger.error(f"Erro no teste de banco de dados: {e}")
            return jsonify({'status': 'error', 'message': 'Erro ao testar conexão com banco de dados', 'error': str(e)}), 500
    
    """Handler para rotas não encontradas"""
    @app.errorhandler(404)
    def not_found(error): return jsonify({'error': 'Endpoint não encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handler para erros internos"""
        logger.error(f"Erro interno: {error}")
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
    return app

def main() -> None:
    """Função principal para executar a aplicação"""
    # Determinar ambiente
    config_name = os.environ.get('FLASK_ENV','development')
    
    # Criar aplicação
    app = create_app(config_name)
    app.config['JSON_SORT_KEYS'] = False  # Desabilitar ordenação de chaves JSON
 
    logger.info("=== API Árvores Brasileiras v2.0.0 (pyodbc) ===")
    logger.info(f"Ambiente: {config_name}")
    logger.info(f"Servidor SQL: {os.environ.get('SQL_SERVER', 'localhost')}")
    logger.info(f"Banco de dados: {os.environ.get('SQL_DATABASE', 'ArvoresBrasileiras')}")
    
    # Testar conexão com banco de dados
    logger.info("Testando conexão com banco de dados...")
    if db_connection.test_connection(): logger.info("✓ Conexão com banco de dados estabelecida com sucesso!")
    else: logger.warning("⚠ Falha na conexão com banco de dados. Verifique as configurações.")
    
    from package.FILEaux import Msgbox
    for msg in Msgbox: logger.info(msg)
    
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', False))

if __name__ == '__main__': 
    main()