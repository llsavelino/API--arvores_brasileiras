from src.models.base_model import BaseModel
from src.database.connection import db_connection
import logging

logger = logging.getLogger(__name__)

class CuriosidadesModel(BaseModel):
    """Modelo para a tabela Curiosidades"""
    
    def get_table_name(self):
        return "Curiosidades"
    
    def get_primary_key(self):
        return "CuriosidadeID"
    
    def get_fields(self):
        return ["EspecieID", "Texto", "Fonte"]
    
    def to_dict(self, row):
        """Converte linha do banco para dicionário"""
        if not row:
            return None
        
        return {
            'CuriosidadeID': row[0],
            'EspecieID': row[1],
            'Texto': row[2],
            'Fonte': row[3]
        }
    
    def from_dict(self, data):
        """Converte dicionário para formato de inserção"""
        result = {}
        
        if 'EspecieID' in data:
            result['EspecieID'] = data['EspecieID']
        if 'Texto' in data:
            result['Texto'] = data['Texto']
        if 'Fonte' in data:
            result['Fonte'] = data['Fonte']
        
        return result
    
    def add_relationships(self, item):
        """Adiciona relacionamentos da curiosidade"""
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
            logger.error(f"Erro ao buscar relacionamentos da curiosidade {item['CuriosidadeID']}: {e}")
            return item
    
    def get_by_especie(self, especie_id):
        """Busca curiosidades por espécie"""
        try:
            query = "SELECT * FROM Curiosidades WHERE EspecieID = ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [especie_id])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar curiosidades por espécie {especie_id}: {e}")
            raise
    
    def search_by_text(self, texto):
        """Busca curiosidades por texto"""
        try:
            query = "SELECT * FROM Curiosidades WHERE Texto LIKE ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [f"%{texto}%"])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar curiosidades por texto '{texto}': {e}")
            raise
    
    def get_by_fonte(self, fonte):
        """Busca curiosidades por fonte"""
        try:
            query = "SELECT * FROM Curiosidades WHERE Fonte LIKE ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [f"%{fonte}%"])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar curiosidades por fonte '{fonte}': {e}")
            raise

# Instância global do modelo
curiosidades_model = CuriosidadesModel()

