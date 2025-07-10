from flask import request, jsonify
import traceback
import logging

logger = logging.getLogger(__name__)

class BaseCRUD:
    """Classe base para operações CRUD usando pyodbc"""
    
    def __init__(self, model):
        self.model = model
    
    def get_all(self):
        """GET - Retorna todos os registros com paginação e filtros"""
        try:
            # Parâmetros de paginação
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 100, type=int), 1000)
            
            # Parâmetro de relacionamentos
            include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
            
            # Filtros dinâmicos
            filters = {}
            for key, value in request.args.items():
                if key not in ['page', 'per_page', 'include_relationships']:
                    filters[key] = value
            
            # Buscar dados usando o modelo
            result = self.model.get_all(
                page=page,
                per_page=per_page,
                filters=filters if filters else None,
                include_relationships=include_relationships
            )
            
            return jsonify(result), 200
            
        except Exception as e:
            logger.error(f"Erro ao buscar registros: {e}")
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
    
    def get_by_id(self, record_id):
        """GET - Retorna um registro específico por ID"""
        try:
            include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
            
            record = self.model.get_by_id(record_id, include_relationships=include_relationships)
            
            if not record:
                return jsonify({'error': 'Registro não encontrado'}), 404
            
            return jsonify(record), 200
            
        except Exception as e:
            logger.error(f"Erro ao buscar registro {record_id}: {e}")
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
    
    def create(self):
        """POST - Cria um novo registro"""
        try:
            data = request.get_json()
            if not data: return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
            
            record = self.model.create(data)
            return jsonify(record), 201
            
        except Exception as e:
            logger.error(f"Erro ao criar registro: {e}")
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
    
    def update(self, record_id):
        """PUT - Atualiza completamente um registro"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
            
            record = self.model.update(record_id, data)
            
            if not record:
                return jsonify({'error': 'Registro não encontrado'}), 404
            
            return jsonify(record), 200
            
        except Exception as e:
            logger.error(f"Erro ao atualizar registro {record_id}: {e}")
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
    
    def partial_update(self, record_id):
        """PATCH - Atualiza parcialmente um registro"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Dados JSON são obrigatórios'}), 400
            
            record = self.model.update(record_id, data)
            
            if not record:
                return jsonify({'error': 'Registro não encontrado'}), 404
            
            return jsonify(record), 200
            
        except Exception as e:
            logger.error(f"Erro ao atualizar parcialmente registro {record_id}: {e}")
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
    
    def delete(self, record_id):
        """DELETE - Remove um registro"""
        try:
            success = self.model.delete(record_id)
            
            if not success:
                return jsonify({'error': 'Registro não encontrado'}), 404
            
            return jsonify({'message': 'Registro removido com sucesso'}), 200
            
        except Exception as e:
            logger.error(f"Erro ao deletar registro {record_id}: {e}")
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500
    
    def head(self, record_id=None):
        """HEAD - Retorna apenas os headers"""
        try:
            if record_id:
                exists = self.model.exists(record_id)
                return '', 200 if exists else 404
            else:
                count = self.model.count()
                response = jsonify()
                response.headers['X-Total-Count'] = str(count)
                return response, 200
                
        except Exception as e:
            logger.error(f"Erro na operação HEAD: {e}")
            return '', 500

