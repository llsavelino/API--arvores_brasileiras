from flask import Blueprint, request, jsonify
from src.models.caracteristicas import caracteristicas_model
from src.routes.base_crud import BaseCRUD

caracteristicas_bp = Blueprint('caracteristicas', __name__)
caracteristicas_crud = BaseCRUD(caracteristicas_model)

@caracteristicas_bp.route('/caracteristicas', methods=['GET'])
def get_caracteristicas() -> tuple: return caracteristicas_crud.get_all()
"""GET /api/caracteristicas - Lista todas as características"""
@caracteristicas_bp.route('/caracteristicas/<int:caracteristica_id>', methods=['GET'])
def get_caracteristica(caracteristica_id: int) -> tuple: return caracteristicas_crud.get_by_id(caracteristica_id)
"""GET /api/caracteristicas/<id> - Obtém uma característica específica"""
@caracteristicas_bp.route('/caracteristicas', methods=['POST'])
def create_caracteristica() -> tuple: return caracteristicas_crud.create()
"""POST /api/caracteristicas - Cria uma nova característica"""
@caracteristicas_bp.route('/caracteristicas/<int:caracteristica_id>', methods=['PUT'])
def update_caracteristica(caracteristica_id: int) -> tuple: return caracteristicas_crud.update(caracteristica_id)
"""PUT /api/caracteristicas/<id> - Atualiza completamente uma característica"""
@caracteristicas_bp.route('/caracteristicas/<int:caracteristica_id>', methods=['PATCH'])
def partial_update_caracteristica(caracteristica_id: int) -> tuple: return caracteristicas_crud.partial_update(caracteristica_id)
"""PATCH /api/caracteristicas/<id> - Atualiza parcialmente uma característica"""
@caracteristicas_bp.route('/caracteristicas/<int:caracteristica_id>', methods=['DELETE'])
def delete_caracteristica(caracteristica_id: int) -> tuple: return caracteristicas_crud.delete(caracteristica_id)
"""DELETE /api/caracteristicas/<id> - Remove uma característica"""
@caracteristicas_bp.route('/caracteristicas', methods=['HEAD'])
def head_caracteristicas() -> tuple: return caracteristicas_crud.head()
"""HEAD /api/caracteristicas - Retorna headers com contagem total"""
@caracteristicas_bp.route('/caracteristicas/<int:caracteristica_id>', methods=['HEAD'])
def head_caracteristica(caracteristica_id: int) -> tuple: return caracteristicas_crud.head(caracteristica_id)
"""HEAD /api/caracteristicas/<id> - Verifica se uma característica existe"""
    
# Rotas auxiliares específicas para Caracteristicas
@caracteristicas_bp.route('/caracteristicas/especie/<int:especie_id>', methods=['GET'])
def get_caracteristicas_by_especie(especie_id: int) -> tuple:
    """GET /api/caracteristicas/especie/<especie_id> - Lista características por espécie"""
    try:
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        caracteristicas = caracteristicas_model.get_by_especie(especie_id)
        
        if include_relationships: caracteristicas = [caracteristicas_model.add_relationships(item) for item in caracteristicas]
        
        return jsonify(caracteristicas), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@caracteristicas_bp.route('/caracteristicas/tipo-folha/<tipo_folha>', methods=['GET'])
def get_caracteristicas_by_tipo_folha(tipo_folha: int) -> tuple:
    """GET /api/caracteristicas/tipo-folha/<tipo_folha> - Lista características por tipo de folha"""
    try:
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        caracteristicas = caracteristicas_model.get_by_tipo_folha(tipo_folha)
        
        if include_relationships: caracteristicas = [caracteristicas_model.add_relationships(item) for item in caracteristicas]
        
        return jsonify(caracteristicas), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@caracteristicas_bp.route('/caracteristicas/altura-range', methods=['GET'])
def get_caracteristicas_by_altura_range() -> tuple:
    """GET /api/caracteristicas/altura-range - Lista características por faixa de altura"""
    try:
        altura_min = request.args.get('min', type=float)
        altura_max = request.args.get('max', type=float)
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        
        caracteristicas = caracteristicas_model.get_by_altura_range(altura_min, altura_max)
        
        if include_relationships: caracteristicas = [caracteristicas_model.add_relationships(item) for item in caracteristicas]
        
        return jsonify(caracteristicas), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

