from src.models.base_model import BaseModel
from src.database.connection import db_connection
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EspeciesModel(BaseModel):
    """Modelo para a tabela Especies"""
    
    def get_table_name(self): return "Especies"
    
    def get_primary_key(self): return "EspecieID"
    
    def get_fields(self): return ["NomeCientifico", "NomePopular", "Familia", "Descricao", "DataCadastro"]
    
    def to_dict(self, row):
        """Converte linha do banco para dicionário"""
        if not row: return None
        
        return {
            'EspecieID': row[0],
            'NomeCientifico': row[1],
            'NomePopular': row[2],
            'Familia': row[3],
            'Descricao': row[4],
            'DataCadastro': row[5].isoformat() if row[5] else None
        }
    
    def from_dict(self, data):
        """Converte dicionário para formato de inserção"""
        result = {}
        
        if 'NomeCientifico' in data:
            result['NomeCientifico'] = data['NomeCientifico']
        if 'NomePopular' in data:
            result['NomePopular'] = data['NomePopular']
        if 'Familia' in data:
            result['Familia'] = data['Familia']
        if 'Descricao' in data:
            result['Descricao'] = data['Descricao']
        if 'DataCadastro' in data:
            result['DataCadastro'] = data['DataCadastro']
        else:
            # Se não fornecido, usar data atual
            result['DataCadastro'] = datetime.now()
        
        return result
    
    def add_relationships(self, item):
        """Adiciona relacionamentos da espécie"""
        try:
            especie_id = item['EspecieID']
            
            # Buscar ocorrências
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute("""
                    SELECT o.OcorrenciaID, o.EspecieID, o.BiomaID, o.Frequencia,
                           b.Nome as BiomaNome, b.Descricao as BiomaDescricao, b.Regiao
                    FROM Ocorrencias o
                    LEFT JOIN Biomas b ON o.BiomaID = b.BiomaID
                    WHERE o.EspecieID = ?
                """, [especie_id])
                
                ocorrencias = []
                for row in cursor.fetchall():
                    ocorrencias.append({
                        'OcorrenciaID': row[0],
                        'EspecieID': row[1],
                        'BiomaID': row[2],
                        'Frequencia': row[3],
                        'Bioma': {
                            'Nome': row[4],
                            'Descricao': row[5],
                            'Regiao': row[6]
                        } if row[4] else None
                    })
                
                # Buscar características
                cursor.execute("""
                    SELECT CaracteristicaID, EspecieID, AlturaMedia, DiametroMedio, TipoFolha, Floracao
                    FROM Caracteristicas
                    WHERE EspecieID = ?
                """, [especie_id])
                
                caracteristicas = []
                for row in cursor.fetchall():
                    caracteristicas.append({
                        'CaracteristicaID': row[0],
                        'EspecieID': row[1],
                        'AlturaMedia': float(row[2]) if row[2] else None,
                        'DiametroMedio': float(row[3]) if row[3] else None,
                        'TipoFolha': row[4],
                        'Floracao': row[5]
                    })
                
                # Buscar curiosidades
                cursor.execute("""
                    SELECT CuriosidadeID, EspecieID, Texto, Fonte
                    FROM Curiosidades
                    WHERE EspecieID = ?
                """, [especie_id])
                
                curiosidades = []
                for row in cursor.fetchall():
                    curiosidades.append({
                        'CuriosidadeID': row[0],
                        'EspecieID': row[1],
                        'Texto': row[2],
                        'Fonte': row[3]
                    })
                
                # Buscar dados da árvore
                cursor.execute("""
                    SELECT DadosID, EspecieID, TempoDeVidaEstimado, CrescimentoAnual, 
                           RaizProfundidadeMedia, DensidadeMadeira
                    FROM DadosArvore
                    WHERE EspecieID = ?
                """, [especie_id])
                
                dados_arvore = []
                for row in cursor.fetchall():
                    dados_arvore.append({
                        'DadosID': row[0],
                        'EspecieID': row[1],
                        'TempoDeVidaEstimado': row[2],
                        'CrescimentoAnual': float(row[3]) if row[3] else None,
                        'RaizProfundidadeMedia': float(row[4]) if row[4] else None,
                        'DensidadeMadeira': float(row[5]) if row[5] else None
                    })
                
                # Adicionar relacionamentos ao item
                item['ocorrencias'] = ocorrencias
                item['caracteristicas'] = caracteristicas
                item['curiosidades'] = curiosidades
                item['dados_arvore'] = dados_arvore
                
                return item
                
        except Exception as e:
            logger.error(f"Erro ao buscar relacionamentos da espécie {item['EspecieID']}: {e}")
            return item
    
    def search_by_name(self, nome):
        """Busca espécies por nome científico ou popular"""
        try:
            query = """
                SELECT * FROM Especies 
                WHERE NomeCientifico LIKE ? OR NomePopular LIKE ?
                ORDER BY NomePopular
            """
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [f"%{nome}%", f"%{nome}%"])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar espécies por nome '{nome}': {e}")
            raise
    
    def get_by_familia(self, familia):
        """Busca espécies por família"""
        try:
            query = """
                SELECT * FROM Especies 
                WHERE Familia LIKE ?
                ORDER BY NomePopular
            """
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [f"%{familia}%"])
                rows = cursor.fetchall()
                return [self.to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Erro ao buscar espécies por família '{familia}': {e}")
            raise

# Instância global do modelo
especies_model = EspeciesModel()

