from abc import ABC, abstractmethod
from src.database.connection import db_connection
import logging

logger = logging.getLogger(__name__)

class BaseModel(ABC):
    """Classe base para todos os modelos de dados usando pyodbc"""
    
    def __init__(self):
        self.table_name = self.get_table_name()
        self.primary_key = self.get_primary_key()
        self.fields = self.get_fields()
    
    @abstractmethod
    def get_table_name(self): pass
    """Retorna o nome da tabela"""
    @abstractmethod
    def get_primary_key(self): pass
    """Retorna o nome da chave primária"""
    @abstractmethod
    def get_fields(self): pass
    """Retorna lista de campos da tabela (exceto chave primária)"""
    @abstractmethod
    def to_dict(self, row): pass
    """Converte uma linha do banco para dicionário"""
    @abstractmethod
    def from_dict(self, data): pass
    """Converte dicionário para formato de inserção no banco"""
    
    def get_all(self, page=1, per_page=100, filters=None, include_relationships=False):
        """Retorna todos os registros com paginação e filtros"""
        try:
            offset = (page - 1) * per_page
            
            # Construir query base
            query = f"SELECT * FROM {self.table_name}"
            params = []
            
            # Adicionar filtros se fornecidos
            if filters:
                where_clauses = []
                for field, value in filters.items():
                    if field in self.fields or field == self.primary_key:
                        where_clauses.append(f"{field} LIKE ?")
                        params.append(f"%{value}%")
                
                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)
            
            # Adicionar paginação
            query += f" ORDER BY {self.primary_key} OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
            params.extend([offset, per_page])
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Contar total de registros
                count_query = f"SELECT COUNT(*) FROM {self.table_name}"
                count_params = []
                
                if filters:
                    where_clauses = []
                    for field, value in filters.items():
                        if field in self.fields or field == self.primary_key:
                            where_clauses.append(f"{field} LIKE ?")
                            count_params.append(f"%{value}%")
                    
                    if where_clauses:
                        count_query += " WHERE " + " AND ".join(where_clauses)
                
                cursor.execute(count_query, count_params)
                total = cursor.fetchone()[0]
                
                # Converter resultados
                items = [self.to_dict(row) for row in rows]
                
                # Adicionar relacionamentos se solicitado
                if include_relationships:
                    items = [self.add_relationships(item) for item in items]
                
                # Calcular informações de paginação
                pages = (total + per_page - 1) // per_page
                has_next = page < pages
                has_prev = page > 1
                
                return {
                    'data': items,
                    'pagination': {
                        'page': page,
                        'pages': pages,
                        'per_page': per_page,
                        'total': total,
                        'has_next': has_next,
                        'has_prev': has_prev
                    }
                }
                
        except Exception as e:
            logger.error(f"Erro ao buscar registros de {self.table_name}: {e}")
            raise
    
    def get_by_id(self, record_id, include_relationships=False):
        """Retorna um registro específico por ID"""
        try:
            query = f"SELECT * FROM {self.table_name} WHERE {self.primary_key} = ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [record_id])
                row = cursor.fetchone()
                
                if row:
                    result = self.to_dict(row)
                    if include_relationships:
                        result = self.add_relationships(result)
                    return result
                return None
                
        except Exception as e:
            logger.error(f"Erro ao buscar registro {record_id} de {self.table_name}: {e}")
            raise
    
    def create(self, data):
        """Cria um novo registro"""
        try:
            # Preparar dados para inserção
            insert_data = self.from_dict(data)
            
            # Construir query de inserção
            fields = list(insert_data.keys())
            placeholders = ', '.join(['?' for _ in fields])
            field_names = ', '.join(fields)
            
            query = f"INSERT INTO {self.table_name} ({field_names}) VALUES ({placeholders})"
            values = list(insert_data.values())
            
            with db_connection.get_transaction() as cursor:
                cursor.execute(query, values)
                
                # Obter ID do registro inserido
                cursor.execute("SELECT @@IDENTITY")
                new_id = cursor.fetchone()[0]
                
                # Retornar o registro criado
                return self.get_by_id(new_id)
                
        except Exception as e:
            logger.error(f"Erro ao criar registro em {self.table_name}: {e}")
            raise
    
    def update(self, record_id, data):
        """Atualiza um registro existente"""
        try:
            # Preparar dados para atualização
            update_data = self.from_dict(data)
            
            # Construir query de atualização
            set_clauses = [f"{field} = ?" for field in update_data.keys()]
            query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE {self.primary_key} = ?"
            
            values = list(update_data.values()) + [record_id]
            
            with db_connection.get_transaction() as cursor:
                cursor.execute(query, values)
                
                if cursor.rowcount == 0: return None # Se nenhum registro foi afetado, retornar None
                
                # Retornar o registro atualizado
                return self.get_by_id(record_id)
                
        except Exception as e:
            logger.error(f"Erro ao atualizar registro {record_id} em {self.table_name}: {e}")
            raise
    
    def delete(self, record_id):
        """Remove um registro"""
        try:
            query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = ?"
            
            with db_connection.get_transaction() as cursor:
                cursor.execute(query, [record_id])
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Erro ao deletar registro {record_id} de {self.table_name}: {e}")
            raise
    
    def exists(self, record_id):
        """Verifica se um registro existe"""
        try:
            query = f"SELECT 1 FROM {self.table_name} WHERE {self.primary_key} = ?"
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, [record_id])
                return cursor.fetchone() is not None
                
        except Exception as e:
            logger.error(f"Erro ao verificar existência do registro {record_id} em {self.table_name}: {e}")
            raise
    
    def count(self, filters=None):
        """Conta o total de registros"""
        try:
            query = f"SELECT COUNT(*) FROM {self.table_name}"
            params = []
            
            if filters:
                where_clauses = []
                for field, value in filters.items():
                    if field in self.fields or field == self.primary_key:
                        where_clauses.append(f"{field} LIKE ?")
                        params.append(f"%{value}%")
                
                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)
            
            with db_connection.get_cursor() as (cursor, connection):
                cursor.execute(query, params)
                return cursor.fetchone()[0]
                
        except Exception as e:
            logger.error(f"Erro ao contar registros de {self.table_name}: {e}")
            raise
    
    def add_relationships(self, item):
        """Adiciona relacionamentos ao item (implementar nas classes filhas se necessário)"""
        return item