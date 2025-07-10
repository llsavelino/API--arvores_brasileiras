from flask import Blueprint, request, jsonify
from src.models.especies import especies_model
from src.routes.base_crud import BaseCRUD

especies_bp = Blueprint('especies', __name__)
especies_crud = BaseCRUD(especies_model)

@especies_bp.route('/especies', methods=['GET'])
def get_especies() -> tuple: return especies_crud.get_all()
"""GET /api/especies - Lista todas as espécies"""
@especies_bp.route('/especies/<int:especie_id>', methods=['GET'])
def get_especie(especie_id: int) -> tuple: return especies_crud.get(especie_id)
"""GET /api/especies/<id> - Obtém uma espécie específica"""
@especies_bp.route('/especies', methods=['POST'])
def create_especie() -> tuple: return especies_crud.create()
"""POST /api/especies - Cria uma nova espécie"""
@especies_bp.route('/especies/<int:especie_id>', methods=['PUT'])
def update_especie(especie_id: int) -> tuple: return especies_crud.update(especie_id)
"""PUT /api/especies/<id> - Atualiza completamente uma espécie"""
@especies_bp.route('/especies/<int:especie_id>', methods=['PATCH'])
def partial_update_especie(especie_id: int) -> tuple: return especies_crud.partial_update(especie_id)
"""PATCH /api/especies/<id> - Atualiza parcialmente uma espécie"""
@especies_bp.route('/especies/<int:especie_id>', methods=['DELETE'])
def delete_especie(especie_id: int) -> tuple: return especies_crud.delete(especie_id)
"""DELETE /api/especies/<id> - Remove uma espécie"""
@especies_bp.route('/especies', methods=['HEAD'])
def head_especies() -> tuple: return especies_crud.head()
"""HEAD /api/especies - Retorna headers com contagem total"""
@especies_bp.route('/especies/<int:especie_id>', methods=['HEAD'])
def head_especie(especie_id: int) -> tuple: return especies_crud.head(especie_id)
"""HEAD /api/especies/<id> - Verifica se uma espécie existe"""
    
# Rotas auxiliares específicas para Especies
@especies_bp.route('/especies/search', methods=['GET'])
def search_especies() -> tuple:
    """GET /api/especies/search - Busca espécies por nome científico ou popular"""
    try:
        nome = request.args.get('nome', '')
        if not nome: return jsonify({'error': 'Parâmetro nome é obrigatório'}), 400
        
        especies = especies_model.search_by_name(nome)
        return jsonify(especies), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@especies_bp.route('/especies/familia/<familia>', methods=['GET'])
def get_especies_by_familia(familia: str) -> tuple:
    """GET /api/especies/familia/<familia> - Lista espécies por família"""
    try:
        especies = especies_model.get_by_familia(familia)
        return jsonify(especies), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

