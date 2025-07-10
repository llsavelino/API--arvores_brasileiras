from flask import Blueprint, request, jsonify
from src.models.biomas import biomas_model
from src.routes.base_crud import BaseCRUD

biomas_bp = Blueprint('biomas', __name__)
biomas_crud = BaseCRUD(biomas_model)

@biomas_bp.route('/biomas', methods=['GET'])
def get_biomas() -> tuple: return biomas_crud.get_all()
"""GET /api/biomas - Lista todos os biomas"""
@biomas_bp.route('/biomas/<int:bioma_id>', methods=['GET'])
def get_bioma(bioma_id: int) -> tuple: return biomas_crud.get_by_id(bioma_id)
"""GET /api/biomas/<id> - Obtém um bioma específico"""
@biomas_bp.route('/biomas', methods=['POST'])
def create_bioma() -> tuple: return biomas_crud.create()
"""POST /api/biomas - Cria um novo bioma"""
@biomas_bp.route('/biomas/<int:bioma_id>', methods=['PUT'])
def update_bioma(bioma_id: int) -> tuple:  return biomas_crud.update(bioma_id)
"""PUT /api/biomas/<id> - Atualiza completamente um bioma"""
@biomas_bp.route('/biomas/<int:bioma_id>', methods=['PATCH'])
def partial_update_bioma(bioma_id: int) -> tuple: return biomas_crud.partial_update(bioma_id)
"""PATCH /api/biomas/<id> - Atualiza parcialmente um bioma"""
@biomas_bp.route('/biomas/<int:bioma_id>', methods=['DELETE'])
def delete_bioma(bioma_id: int) -> tuple: return biomas_crud.delete(bioma_id)
"""DELETE /api/biomas/<id> - Remove um bioma"""
@biomas_bp.route('/biomas', methods=['HEAD'])
def head_biomas() -> tuple: return biomas_crud.head()
"""HEAD /api/biomas - Retorna headers com contagem total"""
@biomas_bp.route('/biomas/<int:bioma_id>', methods=['HEAD'])
def head_bioma(bioma_id: int) -> tuple: return biomas_crud.head(bioma_id)
"""HEAD /api/biomas/<id> - Verifica se um bioma existe"""

# Rotas auxiliares específicas para Biomas
@biomas_bp.route('/biomas/regiao/<regiao>', methods=['GET'])
def get_biomas_by_regiao(regiao: str) -> tuple:
    """GET /api/biomas/regiao/<regiao> - Lista biomas por região"""
    try:
        biomas = biomas_model.get_by_regiao(regiao)
        return jsonify(biomas), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@biomas_bp.route('/biomas/search', methods=['GET'])
def search_biomas() -> tuple:
    """GET /api/biomas/search - Busca biomas por nome"""
    try:
        nome = request.args.get('nome', '')
        if not nome: return jsonify({'error': 'Parâmetro nome é obrigatório'}), 400
        
        biomas = biomas_model.search_by_name(nome)
        return jsonify(biomas), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

