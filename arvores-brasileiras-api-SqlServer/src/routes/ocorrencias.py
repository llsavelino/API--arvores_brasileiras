from flask import Blueprint, request, jsonify
from src.models.ocorrencias import ocorrencias_model
from src.routes.base_crud import BaseCRUD

ocorrencias_bp = Blueprint('ocorrencias', __name__)
ocorrencias_crud = BaseCRUD(ocorrencias_model)

@ocorrencias_bp.route('/ocorrencias', methods=['GET'])
def get_ocorrencias() -> tuple: return ocorrencias_crud.get_all()
"""GET /api/ocorrencias - Lista todas as ocorrências"""
@ocorrencias_bp.route('/ocorrencias/<int:ocorrencia_id>', methods=['GET'])
def get_ocorrencia(ocorrencia_id: int) -> tuple: return ocorrencias_crud.get_by_id(ocorrencia_id)
"""GET /api/ocorrencias/<id> - Obtém uma ocorrência específica"""
@ocorrencias_bp.route('/ocorrencias', methods=['POST'])
def create_ocorrencia() -> tuple: return ocorrencias_crud.create()
"""POST /api/ocorrencias - Cria uma nova ocorrência"""
@ocorrencias_bp.route('/ocorrencias/<int:ocorrencia_id>', methods=['PUT'])
def update_ocorrencia(ocorrencia_id: int) -> tuple: return ocorrencias_crud.update(ocorrencia_id)
"""PUT /api/ocorrencias/<id> - Atualiza completamente uma ocorrência"""
@ocorrencias_bp.route('/ocorrencias/<int:ocorrencia_id>', methods=['PATCH'])
def partial_update_ocorrencia(ocorrencia_id: int) -> tuple: return ocorrencias_crud.partial_update(ocorrencia_id)
"""PATCH /api/ocorrencias/<id> - Atualiza parcialmente uma ocorrência"""
@ocorrencias_bp.route('/ocorrencias/<int:ocorrencia_id>', methods=['DELETE'])
def delete_ocorrencia(ocorrencia_id: int) -> tuple: return ocorrencias_crud.delete(ocorrencia_id)
"""DELETE /api/ocorrencias/<id> - Remove uma ocorrência"""
@ocorrencias_bp.route('/ocorrencias', methods=['HEAD'])
def head_ocorrencias() -> tuple: return ocorrencias_crud.head()
"""HEAD /api/ocorrencias - Retorna headers com contagem total"""
@ocorrencias_bp.route('/ocorrencias/<int:ocorrencia_id>', methods=['HEAD'])
def head_ocorrencia(ocorrencia_id: int) -> tuple: return ocorrencias_crud.head(ocorrencia_id)
"""HEAD /api/ocorrencias/<id> - Verifica se uma ocorrência existe"""
    
# Rotas auxiliares específicas para Ocorrencias
@ocorrencias_bp.route('/ocorrencias/especie/<int:especie_id>', methods=['GET'])
def get_ocorrencias_by_especie(especie_id: int) -> tuple:
    """GET /api/ocorrencias/especie/<especie_id> - Lista ocorrências por espécie"""
    try:
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        ocorrencias = ocorrencias_model.get_by_especie(especie_id)
        
        if include_relationships: ocorrencias = [ocorrencias_model.add_relationships(item) for item in ocorrencias]
        
        return jsonify(ocorrencias), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@ocorrencias_bp.route('/ocorrencias/bioma/<int:bioma_id>', methods=['GET'])
def get_ocorrencias_by_bioma(bioma_id: int) -> tuple:
    """GET /api/ocorrencias/bioma/<bioma_id> - Lista ocorrências por bioma"""
    try:
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        ocorrencias = ocorrencias_model.get_by_bioma(bioma_id)
        
        if include_relationships: ocorrencias = [ocorrencias_model.add_relationships(item) for item in ocorrencias]
        
        return jsonify(ocorrencias), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@ocorrencias_bp.route('/ocorrencias/frequencia/<frequencia>', methods=['GET'])
def get_ocorrencias_by_frequencia(frequencia: int) -> tuple:
    """GET /api/ocorrencias/frequencia/<frequencia> - Lista ocorrências por frequência"""
    try:
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        ocorrencias = ocorrencias_model.get_by_frequencia(frequencia)
        
        if include_relationships: ocorrencias = [ocorrencias_model.add_relationships(item) for item in ocorrencias]
        
        return jsonify(ocorrencias), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

