from flask import Blueprint, request, jsonify
from src.models.curiosidades import curiosidades_model
from src.routes.base_crud import BaseCRUD

curiosidades_bp = Blueprint('curiosidades', __name__)
curiosidades_crud = BaseCRUD(curiosidades_model)

@curiosidades_bp.route('/curiosidades', methods=['GET'])
def get_curiosidades() -> tuple: return curiosidades_crud.get_all()
"""GET /api/curiosidades - Lista todas as curiosidades"""
@curiosidades_bp.route('/curiosidades/<int:curiosidade_id>', methods=['GET'])
def get_curiosidade(curiosidade_id: int) -> tuple: return curiosidades_crud.get_by_id(curiosidade_id)
"""GET /api/curiosidades/<id> - Obtém uma curiosidade específica"""
@curiosidades_bp.route('/curiosidades', methods=['POST'])
def create_curiosidade() -> tuple: return curiosidades_crud.create()
"""POST /api/curiosidades - Cria uma nova curiosidade"""
@curiosidades_bp.route('/curiosidades/<int:curiosidade_id>', methods=['PUT'])
def update_curiosidade(curiosidade_id: int) -> tuple: return curiosidades_crud.update(curiosidade_id)
"""PUT /api/curiosidades/<id> - Atualiza completamente uma curiosidade"""    
@curiosidades_bp.route('/curiosidades/<int:curiosidade_id>', methods=['PATCH'])
def partial_update_curiosidade(curiosidade_id: int) -> tuple: return curiosidades_crud.partial_update(curiosidade_id)
"""PATCH /api/curiosidades/<id> - Atualiza parcialmente uma curiosidade"""
@curiosidades_bp.route('/curiosidades/<int:curiosidade_id>', methods=['DELETE'])
def delete_curiosidade(curiosidade_id: int) -> tuple: return curiosidades_crud.delete(curiosidade_id)
"""DELETE /api/curiosidades/<id> - Remove uma curiosidade"""
@curiosidades_bp.route('/curiosidades', methods=['HEAD'])
def head_curiosidades() -> tuple: return curiosidades_crud.head()
"""HEAD /api/curiosidades - Retorna headers com contagem total"""
@curiosidades_bp.route('/curiosidades/<int:curiosidade_id>', methods=['HEAD'])
def head_curiosidade(curiosidade_id: int) -> tuple: return curiosidades_crud.head(curiosidade_id)
"""HEAD /api/curiosidades/<id> - Verifica se uma curiosidade existe"""
    
# Rotas auxiliares específicas para Curiosidades
@curiosidades_bp.route('/curiosidades/especie/<int:especie_id>', methods=['GET'])
def get_curiosidades_by_especie(especie_id: int) -> tuple:
    """GET /api/curiosidades/especie/<especie_id> - Lista curiosidades por espécie"""
    try:
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        curiosidades = curiosidades_model.get_by_especie(especie_id)
        
        if include_relationships: curiosidades = [curiosidades_model.add_relationships(item) for item in curiosidades]
        
        return jsonify(curiosidades), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@curiosidades_bp.route('/curiosidades/search', methods=['GET'])
def search_curiosidades() -> tuple:
    """GET /api/curiosidades/search - Busca curiosidades por texto"""
    try:
        texto = request.args.get('texto', '')
        if not texto: return jsonify({'error': 'Parâmetro texto é obrigatório'}), 400
        
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        curiosidades = curiosidades_model.search_by_text(texto)
        
        if include_relationships: curiosidades = [curiosidades_model.add_relationships(item) for item in curiosidades]
        
        return jsonify(curiosidades), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@curiosidades_bp.route('/curiosidades/fonte/<fonte>', methods=['GET'])
def get_curiosidades_by_fonte(fonte: str) -> tuple:
    """GET /api/curiosidades/fonte/<fonte> - Lista curiosidades por fonte"""
    try:
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        curiosidades = curiosidades_model.get_by_fonte(fonte)
        
        if include_relationships: curiosidades = [curiosidades_model.add_relationships(item) for item in curiosidades]
        
        return jsonify(curiosidades), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

