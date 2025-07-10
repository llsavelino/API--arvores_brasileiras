from flask import Blueprint, jsonify
from src.database.connection import db_connection
import pyodbc

arvores_bp = Blueprint('arvores', __name__)

@arvores_bp.route('/arvores-completa/<int:especie_id>', methods=['GET'])
def get_arvores_completa(especie_id: int) -> tuple:
    try:   
        query = """
        SELECT 
            e.EspecieID,
            e.NomeCientifico,
            e.NomePopular,
            e.Familia,
            e.Descricao AS DescricaoEspecie,
            e.DataCadastro,
            b.BiomaID,
            b.Nome AS NomeBioma,
            b.Descricao AS DescricaoBioma,
            b.Regiao,
            o.OcorrenciaID,
            o.Frequencia,
            c.CaracteristicaID,
            c.AlturaMedia,
            c.DiametroMedio,
            c.TipoFolha,
            c.Floracao,
            cu.CuriosidadeID,
            cu.Texto AS TextoCuriosidade,
            cu.Fonte,
            d.DadosID,
            d.TempoDeVidaEstimado,
            d.CrescimentoAnual,
            d.RaizProfundidadeMedia,
            d.DensidadeMadeira
        FROM 
            Especies e
            LEFT JOIN Ocorrencias o ON e.EspecieID = o.EspecieID
            LEFT JOIN Biomas b ON o.BiomaID = b.BiomaID
            LEFT JOIN Caracteristicas c ON e.EspecieID = c.EspecieID
            LEFT JOIN Curiosidades cu ON e.EspecieID = cu.EspecieID
            LEFT JOIN DadosArvore d ON e.EspecieID = d.EspecieID
        WHERE 
            e.EspecieID = ?
        """
        
        with db_connection.get_cursor() as (cursor, conn): # Obtém o cursor e conexão do banco de dados            cursor.execute(query, especie_id)
            rows = cursor.fetchall()
            conn.commit()  # Garante que as alterações sejam salvas, se houver
        if not rows: return jsonify({'message': f'Nenhuma árvore com id {especie_id} encontrada para a espécie informada.'}), 404
        
        # Transformar os resultados em uma lista de dicionários
        resultados = []
        for row in rows:
            resultado = {
                'EspecieID': row.EspecieID,
                'NomeCientifico': row.NomeCientifico,
                'NomePopular': row.NomePopular,
                'Familia': row.Familia,
                'DescricaoEspecie': row.DescricaoEspecie,
                'DataCadastro': row.DataCadastro.isoformat() if row.DataCadastro else None,
                'Biomas': {
                    'BiomaID': row.BiomaID, 'NomeBioma': row.NomeBioma,
                    'DescricaoBioma': row.DescricaoBioma, 'Regiao': row.Regiao, 'Frequencia': row.Frequencia
                } if row.BiomaID else None,
                'Caracteristicas': {
                    'CaracteristicaID': row.CaracteristicaID,
                    'AlturaMedia': float(row.AlturaMedia) if row.AlturaMedia else None,
                    'DiametroMedio': float(row.DiametroMedio) if row.DiametroMedio else None,
                    'TipoFolha': row.TipoFolha,
                    'Floracao': row.Floracao
                } if row.CaracteristicaID else None,
                'Curiosidades': {
                    'CuriosidadeID': row.CuriosidadeID, 'Texto': row.TextoCuriosidade, 'Fonte': row.Fonte
                } if row.CuriosidadeID else None,
                'DadosArvore': {
                    'DadosID': row.DadosID,
                    'TempoDeVidaEstimado': row.TempoDeVidaEstimado,
                    'CrescimentoAnual': float(row.CrescimentoAnual) if row.CrescimentoAnual else None,
                    'RaizProfundidadeMedia': float(row.RaizProfundidadeMedia) if row.RaizProfundidadeMedia else None,
                    'DensidadeMadeira': float(row.DensidadeMadeira) if row.DensidadeMadeira else None
                } if row.DadosID else None
            }
            
            resultados.append(resultado)

        if resultados: return jsonify({'message': 'Nenhuma árvore encontrada para a espécie informada.'}), 404
        
        return jsonify({'tree': resultados,}), 200 
        
    except pyodbc.Error as e: return jsonify({'error': 'Erro ao acessar o banco de dados', 'details': str(e)}), 500
    except Exception as e: return jsonify({'error': str(e)}), 500
