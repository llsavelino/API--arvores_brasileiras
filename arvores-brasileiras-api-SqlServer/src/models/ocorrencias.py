from src.models.base_model import BaseModel
from src.database.connection import db_connection
import logging

logger = logging.getLogger(__name__)

class OcorrenciasModel(BaseModel):
    """Modelo para a tabela Ocorrencias"""
    
    def get_table_name(self): return "Ocorrencias"
    
    def get_primary_key(self): return "OcorrenciaID"
    
    def get_fields(self): return ["EspecieID", "BiomaID", "Frequencia"]
    
    def to_dict(self, row):
        """Converte linha do banco para dicionário"""
        if not row: return None
        
        return {
            'OcorrenciaID': row[0],
            'EspecieID': row[1],
            'BiomaID': row[2],
            'Frequencia': row[3]
        }
    
    def from_dict(self, data):
        """Converte dicionário para formato de inserção"""
        result = {}
        
        if 'EspecieID' in data:
            result['EspecieID'] = data['EspecieID']
        if 'BiomaID' in data:
            result['BiomaID'] = data['BiomaID']
        if 'Frequencia' in data:
            result['Frequencia'] = data['Frequencia']
        
        return result
    
    def add_relationships(self, item):
        """Adiciona relacionamentos da ocorrência"""
        try:
            with db_connection.get_cursor() as (cursor, connection):
                # Buscar dados da espécie
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
                
                # Buscar dados do bioma
                cursor.execute("""
                    SELECT BiomaID, Nome, Descricao, Regiao
                    FROM Biomas WHERE BiomaID = ?
                """, [item['BiomaID']])
                
                bioma_row = cursor.fetchone()
                if bioma_row:
                    item['bioma'] = {
                        'BiomaID': bioma_row[0],
                        'Nome': bioma_row[1],
                        'Descricao': bioma_row[2],
                        'Regiao': bioma_row[3]
                    }
                
                return item
                
        except Exception as e:
            logger.error(f"Erro ao buscar relacionamentos da ocorrência {item['OcorrenciaID']}: {e}")
            return item
    
    def get_by_especie(self, especie_id):
        """Busca ocorrências por espécie"""
        try:
            query = "SELECT * FROM Ocorrencias WHERE EspecieID = ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [especie_id])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar ocorrências por espécie {especie_id}: {e}")
            raise
    
    def get_by_bioma(self, bioma_id):
        """Busca ocorrências por bioma"""
        try:
            query = "SELECT * FROM Ocorrencias WHERE BiomaID = ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [bioma_id])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar ocorrências por bioma {bioma_id}: {e}")
            raise
    
    def get_by_frequencia(self, frequencia):
        """Busca ocorrências por frequência"""
        try:
            query = "SELECT * FROM Ocorrencias WHERE Frequencia LIKE ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [f"%{frequencia}%"])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar ocorrências por frequência '{frequencia}': {e}")
            raise

# Instância global do modelo
ocorrencias_model = OcorrenciasModel()

