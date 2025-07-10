from src.models.base_model import BaseModel
from src.database.connection import db_connection
import logging

logger = logging.getLogger(__name__)

class CaracteristicasModel(BaseModel):
    """Modelo para a tabela Caracteristicas"""
    
    def get_table_name(self):
        return "Caracteristicas"
    
    def get_primary_key(self):
        return "CaracteristicaID"
    
    def get_fields(self):
        return ["EspecieID", "AlturaMedia", "DiametroMedio", "TipoFolha", "Floracao"]
    
    def to_dict(self, row):
        """Converte linha do banco para dicionário"""
        if not row:
            return None
        
        return {
            'CaracteristicaID': row[0],
            'EspecieID': row[1],
            'AlturaMedia': float(row[2]) if row[2] else None,
            'DiametroMedio': float(row[3]) if row[3] else None,
            'TipoFolha': row[4],
            'Floracao': row[5]
        }
    
    def from_dict(self, data):
        """Converte dicionário para formato de inserção"""
        result = {}
        
        if 'EspecieID' in data:
            result['EspecieID'] = data['EspecieID']
        if 'AlturaMedia' in data:
            result['AlturaMedia'] = data['AlturaMedia']
        if 'DiametroMedio' in data:
            result['DiametroMedio'] = data['DiametroMedio']
        if 'TipoFolha' in data:
            result['TipoFolha'] = data['TipoFolha']
        if 'Floracao' in data:
            result['Floracao'] = data['Floracao']
        
        return result
    
    def add_relationships(self, item):
        """Adiciona relacionamentos da característica"""
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
            logger.error(f"Erro ao buscar relacionamentos da característica {item['CaracteristicaID']}: {e}")
            return item
    
    def get_by_especie(self, especie_id):
        """Busca características por espécie"""
        try:
            query = "SELECT * FROM Caracteristicas WHERE EspecieID = ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [especie_id])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar características por espécie {especie_id}: {e}")
            raise
    
    def get_by_tipo_folha(self, tipo_folha):
        """Busca características por tipo de folha"""
        try:
            query = "SELECT * FROM Caracteristicas WHERE TipoFolha LIKE ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [f"%{tipo_folha}%"])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar características por tipo de folha '{tipo_folha}': {e}")
            raise
    
    def get_by_altura_range(self, altura_min=None, altura_max=None):
        """Busca características por faixa de altura"""
        try:
            query = "SELECT * FROM Caracteristicas WHERE 1=1"
            params = []
            
            if altura_min is not None:
                query += " AND AlturaMedia >= ?"
                params.append(altura_min)
            
            if altura_max is not None:
                query += " AND AlturaMedia <= ?"
                params.append(altura_max)
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar características por faixa de altura: {e}")
            raise

# Instância global do modelo
caracteristicas_model = CaracteristicasModel()

