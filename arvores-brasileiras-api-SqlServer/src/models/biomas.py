from src.models.base_model import BaseModel
from src.database.connection import db_connection
import logging

logger = logging.getLogger(__name__)

class BiomasModel(BaseModel):
    """Modelo para a tabela Biomas"""
    
    def get_table_name(self): return "Biomas"
    
    def get_primary_key(self): return "BiomaID"
    
    def get_fields(self): return ["Nome", "Descricao", "Regiao"]
    
    def to_dict(self, row):
        """Converte linha do banco para dicionário"""
        if not row: return None
        
        return {
            'BiomaID': row[0],
            'Nome': row[1],
            'Descricao': row[2],
            'Regiao': row[3]
        }
    
    def from_dict(self, data):
        """Converte dicionário para formato de inserção"""
        result = {}
        
        if 'Nome' in data:
            result['Nome'] = data['Nome']
        if 'Descricao' in data:
            result['Descricao'] = data['Descricao']
        if 'Regiao' in data:
            result['Regiao'] = data['Regiao']
        
        return result
    
    def add_relationships(self, item):
        """Adiciona relacionamentos do bioma"""
        try:
            bioma_id = item['BiomaID']
            
            # Buscar ocorrências
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute("""
                    SELECT o.OcorrenciaID, o.EspecieID, o.BiomaID, o.Frequencia,
                           e.NomeCientifico, e.NomePopular, e.Familia
                    FROM Ocorrencias o
                    LEFT JOIN Especies e ON o.EspecieID = e.EspecieID
                    WHERE o.BiomaID = ?
                """, [bioma_id])
                
                ocorrencias = []
                for row in cursor.fetchall():
                    ocorrencias.append({
                        'OcorrenciaID': row[0],
                        'EspecieID': row[1],
                        'BiomaID': row[2],
                        'Frequencia': row[3],
                        'Especie': {
                            'NomeCientifico': row[4],
                            'NomePopular': row[5],
                            'Familia': row[6]
                        } if row[4] else None
                    })
                
                item['ocorrencias'] = ocorrencias
                return item
                
        except Exception as e:
            logger.error(f"Erro ao buscar relacionamentos do bioma {item['BiomaID']}: {e}")
            return item
    
    def search_by_name(self, nome):
        """Busca biomas por nome"""
        try:
            query = "SELECT * FROM Biomas WHERE Nome LIKE ? ORDER BY Nome"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [f"%{nome}%"])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar biomas por nome '{nome}': {e}")
            raise
    
    def get_by_regiao(self, regiao):
        """Busca biomas por região"""
        try:
            query = "SELECT * FROM Biomas WHERE Regiao LIKE ? ORDER BY Nome"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [f"%{regiao}%"])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar biomas por região '{regiao}': {e}")
            raise

# Instância global do modelo
biomas_model = BiomasModel()

