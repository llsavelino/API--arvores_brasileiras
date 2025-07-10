from src.models.base_model import BaseModel
from src.database.connection import db_connection
import logging

logger = logging.getLogger(__name__)

class DadosArvoreModel(BaseModel):
    """Modelo para a tabela DadosArvore"""
    
    def get_table_name(self):
        return "DadosArvore"
    
    def get_primary_key(self):
        return "DadosID"
    
    def get_fields(self):
        return ["EspecieID", "TempoDeVidaEstimado", "CrescimentoAnual", "RaizProfundidadeMedia", "DensidadeMadeira"]
    
    def to_dict(self, row):
        """Converte linha do banco para dicionário"""
        if not row:
            return None
        
        return {
            'DadosID': row[0],
            'EspecieID': row[1],
            'TempoDeVidaEstimado': row[2],
            'CrescimentoAnual': float(row[3]) if row[3] else None,
            'RaizProfundidadeMedia': float(row[4]) if row[4] else None,
            'DensidadeMadeira': float(row[5]) if row[5] else None
        }
    
    def from_dict(self, data):
        """Converte dicionário para formato de inserção"""
        result = {}
        
        if 'EspecieID' in data:
            result['EspecieID'] = data['EspecieID']
        if 'TempoDeVidaEstimado' in data:
            result['TempoDeVidaEstimado'] = data['TempoDeVidaEstimado']
        if 'CrescimentoAnual' in data:
            result['CrescimentoAnual'] = data['CrescimentoAnual']
        if 'RaizProfundidadeMedia' in data:
            result['RaizProfundidadeMedia'] = data['RaizProfundidadeMedia']
        if 'DensidadeMadeira' in data:
            result['DensidadeMadeira'] = data['DensidadeMadeira']
        
        return result
    
    def add_relationships(self, item):
        """Adiciona relacionamentos dos dados da árvore"""
        try:
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute("""
                    SELECT EspecieID, NomeCientifico, NomePopular, Familia
                    FROM Especies WHERE EspecieID = ?
                """, [item['EspecieID']])
                
                especie_row = cursor.fetchone()
                if especie_row:
                    item['especie'] = {
                        'EspecieID': especie_row[0],
                        'NomeCientifico': especie_row[1],
                        'NomePopular': especie_row[2],
                        'Familia': especie_row[3]
                    }
                
                return item
                
        except Exception as e:
            logger.error(f"Erro ao buscar relacionamentos dos dados da árvore {item['DadosID']}: {e}")
            return item
    
    def get_by_especie(self, especie_id):
        """Busca dados da árvore por espécie"""
        try:
            query = "SELECT * FROM DadosArvore WHERE EspecieID = ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [especie_id])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar dados da árvore por espécie {especie_id}: {e}")
            raise
    
    def get_by_tempo_vida_range(self, tempo_min=None, tempo_max=None):
        """Busca dados por faixa de tempo de vida"""
        try:
            query = "SELECT * FROM DadosArvore WHERE 1=1"
            params = []
            
            if tempo_min is not None:
                query += " AND TempoDeVidaEstimado >= ?"
                params.append(tempo_min)
            
            if tempo_max is not None:
                query += " AND TempoDeVidaEstimado <= ?"
                params.append(tempo_max)
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar dados por faixa de tempo de vida: {e}")
            raise
    
    def get_by_crescimento_range(self, crescimento_min=None, crescimento_max=None):
        """Busca dados por faixa de crescimento anual"""
        try:
            query = "SELECT * FROM DadosArvore WHERE 1=1"
            params = []
            
            if crescimento_min is not None:
                query += " AND CrescimentoAnual >= ?"
                params.append(crescimento_min)
            
            if crescimento_max is not None:
                query += " AND CrescimentoAnual <= ?"
                params.append(crescimento_max)
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar dados por faixa de crescimento: {e}")
            raise
    
    def get_by_densidade_range(self, densidade_min=None, densidade_max=None):
        """Busca dados por faixa de densidade da madeira"""
        try:
            query = "SELECT * FROM DadosArvore WHERE 1=1"
            params = []
            
            if densidade_min is not None:
                query += " AND DensidadeMadeira >= ?"
                params.append(densidade_min)
            
            if densidade_max is not None:
                query += " AND DensidadeMadeira <= ?"
                params.append(densidade_max)
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar dados por faixa de densidade: {e}")
            raise

# Instância global do modelo
dados_arvore_model = DadosArvoreModel()

