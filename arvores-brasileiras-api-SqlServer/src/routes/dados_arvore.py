from flask import Blueprint, request, jsonify
from src.models.dados_arvore import dados_arvore_model
from src.routes.base_crud import BaseCRUD

dados_arvore_bp = Blueprint('dados_arvore', __name__)
dados_arvore_crud = BaseCRUD(dados_arvore_model)

@dados_arvore_bp.route('/dados-arvore', methods=['GET'])
def get_dados_arvore() -> tuple: return dados_arvore_crud.get_all()
"""GET /api/dados-arvore - Lista todos os dados de árvore"""
@dados_arvore_bp.route('/dados-arvore/<int:dados_id>', methods=['GET'])
def get_dados_arvore_by_id(dados_id: int) -> tuple: return dados_arvore_crud.get_by_id(dados_id)
"""GET /api/dados-arvore/<id> - Obtém dados de árvore específicos"""
@dados_arvore_bp.route('/dados-arvore', methods=['POST'])
def create_dados_arvore() -> tuple: return dados_arvore_crud.create()
"""POST /api/dados-arvore - Cria novos dados de árvore"""
@dados_arvore_bp.route('/dados-arvore/<int:dados_id>', methods=['PUT'])
def update_dados_arvore(dados_id: int) -> tuple: return dados_arvore_crud.update(dados_id)
"""PUT /api/dados-arvore/<id> - Atualiza completamente dados de árvore"""
@dados_arvore_bp.route('/dados-arvore/<int:dados_id>', methods=['PATCH'])
def partial_update_dados_arvore(dados_id: int) -> tuple: return dados_arvore_crud.partial_update(dados_id)
"""PATCH /api/dados-arvore/<id> - Atualiza parcialmente dados de árvore"""
@dados_arvore_bp.route('/dados-arvore/<int:dados_id>', methods=['DELETE'])
def delete_dados_arvore(dados_id: int) -> tuple: return dados_arvore_crud.delete(dados_id)
"""DELETE /api/dados-arvore/<id> - Remove dados de árvore"""
@dados_arvore_bp.route('/dados-arvore', methods=['HEAD'])
def head_dados_arvore() -> tuple: return dados_arvore_crud.head()
"""HEAD /api/dados-arvore - Retorna headers com contagem total"""
@dados_arvore_bp.route('/dados-arvore/<int:dados_id>', methods=['HEAD'])
def head_dados_arvore_by_id(dados_id: int) -> tuple: return dados_arvore_crud.head(dados_id)
"""HEAD /api/dados-arvore/<id> - Verifica se dados de árvore existem"""

# Rotas auxiliares específicas para DadosArvore
@dados_arvore_bp.route('/dados-arvore/especie/<int:especie_id>', methods=['GET'])
def get_dados_arvore_by_especie(especie_id: int) -> tuple:
    """GET /api/dados-arvore/especie/<especie_id> - Lista dados de árvore por espécie"""
    try:
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        dados_arvore = dados_arvore_model.get_by_especie(especie_id)
        
        if include_relationships: dados_arvore = [dados_arvore_model.add_relationships(item) for item in dados_arvore]
        
        return jsonify(dados_arvore), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@dados_arvore_bp.route('/dados-arvore/tempo-vida-range', methods=['GET'])
def get_dados_arvore_by_tempo_vida_range() -> tuple:
    """GET /api/dados-arvore/tempo-vida-range - Lista dados por faixa de tempo de vida"""
    try:
        tempo_min = request.args.get('min', type=int)
        tempo_max = request.args.get('max', type=int)
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        
        dados_arvore = dados_arvore_model.get_by_tempo_vida_range(tempo_min, tempo_max)
        
        if include_relationships: dados_arvore = [dados_arvore_model.add_relationships(item) for item in dados_arvore]
        
        return jsonify(dados_arvore), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@dados_arvore_bp.route('/dados-arvore/crescimento-range', methods=['GET'])
def get_dados_arvore_by_crescimento_range() -> tuple:
    """GET /api/dados-arvore/crescimento-range - Lista dados por faixa de crescimento anual"""
    try:
        crescimento_min = request.args.get('min', type=float)
        crescimento_max = request.args.get('max', type=float)
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        
        dados_arvore = dados_arvore_model.get_by_crescimento_range(crescimento_min, crescimento_max)
        
        if include_relationships: dados_arvore = [dados_arvore_model.add_relationships(item) for item in dados_arvore]
        
        return jsonify(dados_arvore), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

@dados_arvore_bp.route('/dados-arvore/densidade-range', methods=['GET'])
def get_dados_arvore_by_densidade_range() -> tuple:
    """GET /api/dados-arvore/densidade-range - Lista dados por faixa de densidade da madeira"""
    try:
        densidade_min = request.args.get('min', type=float)
        densidade_max = request.args.get('max', type=float)
        include_relationships = request.args.get('include_relationships', 'false').lower() == 'true'
        
        dados_arvore = dados_arvore_model.get_by_densidade_range(densidade_min, densidade_max)
        
        if include_relationships: dados_arvore = [dados_arvore_model.add_relationships(item) for item in dados_arvore]
        
        return jsonify(dados_arvore), 200
        
    except Exception as e: return jsonify({'error': str(e)}), 500

