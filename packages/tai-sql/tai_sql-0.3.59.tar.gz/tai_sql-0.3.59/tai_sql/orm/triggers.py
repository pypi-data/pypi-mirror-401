"""
Sistema de triggers para tai-sql.

Este módulo proporciona decoradores y clases para definir triggers que se ejecutan
automáticamente en operaciones CRUD (create, UPDATE, DELETE).

Los triggers definidos en los modelos (public.py) son analizados y convertidos a
código ejecutable que se inyecta en los DAOs generados.

Example:
    ```python
    from tai_sql import *
    from tai_sql.orm.triggers import on_create, on_update, on_delete, TriggerAPI
    
    class Usuario(Table):
        __tablename__ = "usuario"
        
        id: int = column(primary_key=True, autoincrement=True)
        email: str
        status: str
        
        @on_create(timing='before')
        def normalize_email(self, t: TriggerAPI):
            '''Normaliza el email antes de insertar'''
            t.data['email'] = t.data['email'].lower().strip()
        
        @on_update(
            timing='before',
            fields=['status'],
            when=lambda t: t.old['status'] != t.new['status']
        )
        def log_status_change(self, t: TriggerAPI):
            '''Registra cambios de estado'''
            t.log(f"Estado cambiado: {t.old['status']} -> {t.new['status']}")
    ```
"""
from __future__ import annotations
from typing import Callable, Optional, List, Any, Dict, Type, TYPE_CHECKING, Union
import inspect
import ast
import textwrap

from .descriptors import AutoRegisterDescriptor

if TYPE_CHECKING:
    from .table import Table


class TriggerStep:
    """
    Representa un paso/operación dentro de un trigger.
    
    Cada step corresponde a una operación del TriggerAPI o una operación Python estándar.
    """
    
    def __init__(
        self,
        step_type: str,
        operation: str,
        args: Optional[List[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        target: Optional[str] = None,
        source_line: Optional[str] = None,
        ast_node: Optional[ast.AST] = None,
        trigger_refs: Optional[List[str]] = None
    ):
        """
        Args:
            step_type: Tipo de operación ('data_access', 'data_mutation', 'crud_call', 'log', 'abort', 'control_flow', 'other')
            operation: Nombre de la operación específica ('get', 'set', 'find', 'create', 'count', 'log', 'abort', etc.)
            args: Argumentos posicionales de la operación
            kwargs: Argumentos nombrados de la operación
            target: Variable o modelo objetivo (ej: 'Post', 'Usuario', 'Post -> post_count')
            source_line: Línea de código fuente original
            ast_node: Nodo AST original para análisis avanzado
            trigger_refs: Referencias a TriggerAPI usadas (ej: ['t.data', 't.instance'])
        """
        self.step_type = step_type
        self.operation = operation
        self.args = args or []
        self.kwargs = kwargs or {}
        self.target = target
        self.source_line = source_line
        self.ast_node = ast_node
        self.trigger_refs = trigger_refs or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el step a diccionario para serialización"""
        return {
            'step_type': self.step_type,
            'operation': self.operation,
            'args': self.args,
            'kwargs': self.kwargs,
            'target': self.target,
            'source_line': self.source_line,
            'trigger_refs': self.trigger_refs
        }
    
    def transform_code(self, code: str, context: Dict[str, str]) -> str:
        """
        Transforma el código del trigger reemplazando referencias de TriggerAPI.
        
        Args:
            code: Código a transformar
            context: Mapeo de referencias (ej: {'t.data': 't_data', 't.instance': 'instance'})
        
        Returns:
            Código transformado con las referencias correctas
        """
        result = code
        # Ordenar por longitud descendente para evitar reemplazos parciales
        for trigger_ref, actual_var in sorted(context.items(), key=lambda x: len(x[0]), reverse=True):
            result = result.replace(trigger_ref, actual_var)
        return result
    
    def __repr__(self) -> str:
        return f"<TriggerStep {self.step_type}:{self.operation} target={self.target}>"


class TriggerAnalyzer(ast.NodeVisitor):
    """
    Analizador AST para extraer operaciones del TriggerAPI de un trigger.
    
    Recorre el árbol AST de la función trigger e identifica:
    - Accesos a t.data, t.old, t.new, t.instance
    - Llamadas a t.dao(), t.log(), t.abort()
    - Operaciones de mutación de datos
    """
    
    def __init__(self, source_lines: List[str]):
        """
        Args:
            source_lines: Líneas del código fuente para obtener el texto original
        """
        self.steps: List[TriggerStep] = []
        self.source_lines = source_lines
        self.trigger_var = 't'  # Nombre del parámetro TriggerAPI (por defecto 't')
    
    def visit_Assign(self, node: ast.Assign) -> None:
        """Visita asignaciones para detectar mutaciones de datos"""
        # Detectar asignaciones a t.data['campo']
        for target in node.targets:
            if isinstance(target, ast.Subscript):
                if self._is_trigger_attr(target.value, 'data'):
                    # t.data['campo'] = valor
                    field_name = self._extract_subscript_key(target)
                    source_line = self._get_source_line(node)
                    value_code = self._ast_to_repr(node.value)
                    trigger_refs = self._extract_trigger_references(node)
                    
                    self.steps.append(TriggerStep(
                        step_type='data_mutation',
                        operation='set_data',
                        target=field_name,
                        args=[value_code],
                        source_line=source_line,
                        ast_node=node,
                        trigger_refs=trigger_refs
                    ))
        
        # Detectar asignaciones que incluyan llamadas CRUD
        if isinstance(node.value, ast.Call):
            if self._is_crud_method(node.value.func):
                crud_operation = node.value.func.attr
                
                # El primer argumento debe ser el modelo
                model_name = None
                if len(node.value.args) > 0 and isinstance(node.value.args[0], ast.Name):
                    model_name = node.value.args[0].id
                
                # Los demás argumentos
                args = [self._ast_to_repr(arg) for arg in node.value.args[1:]]
                kwargs = {kw.arg: self._ast_to_repr(kw.value) for kw in node.value.keywords}
                trigger_refs = self._extract_trigger_references(node)
                
                # Obtener el nombre de la variable de asignación
                var_name = None
                if node.targets and isinstance(node.targets[0], ast.Name):
                    var_name = node.targets[0].id
                
                self.steps.append(TriggerStep(
                    step_type='crud_call',
                    operation=crud_operation,
                    args=args,
                    kwargs=kwargs,
                    target=f"{model_name} -> {var_name}" if var_name else model_name,
                    source_line=self._get_source_line(node),
                    ast_node=node,
                    trigger_refs=trigger_refs
                ))
        
        self.generic_visit(node)
    
    def visit_Expr(self, node: ast.Expr) -> None:
        """Visita expresiones para detectar llamadas a métodos del TriggerAPI"""
        if isinstance(node.value, ast.Call):
            self._visit_call(node.value)
        self.generic_visit(node)
    
    def _visit_call(self, node: ast.Call) -> None:
        """Procesa llamadas a funciones/métodos"""
        # Detectar t.log(...)
        if self._is_trigger_method(node.func, 'log'):
            args = [self._ast_to_repr(arg) for arg in node.args]
            kwargs = {kw.arg: self._ast_to_repr(kw.value) for kw in node.keywords}
            trigger_refs = self._extract_trigger_references(node)
            
            self.steps.append(TriggerStep(
                step_type='log',
                operation='log',
                args=args,
                kwargs=kwargs,
                source_line=self._get_source_line(node),
                ast_node=node,
                trigger_refs=trigger_refs
            ))
        
        # Detectar t.abort(...)
        elif self._is_trigger_method(node.func, 'abort'):
            args = [self._ast_to_repr(arg) for arg in node.args]
            trigger_refs = self._extract_trigger_references(node)
            
            self.steps.append(TriggerStep(
                step_type='abort',
                operation='abort',
                args=args,
                source_line=self._get_source_line(node),
                ast_node=node,
                trigger_refs=trigger_refs
            ))
        
        # Detectar llamadas CRUD: t.find(...), t.create(...), t.count(...), etc.
        elif self._is_crud_method(node.func):
            crud_operation = node.func.attr  # find, create, count, etc.
            
            # El primer argumento debe ser el modelo
            model_name = None
            if len(node.args) > 0 and isinstance(node.args[0], ast.Name):
                model_name = node.args[0].id
            
            # Los demás argumentos son parámetros de la operación
            args = [self._ast_to_repr(arg) for arg in node.args[1:]]  # Saltar el modelo
            kwargs = {kw.arg: self._ast_to_repr(kw.value) for kw in node.keywords}
            trigger_refs = self._extract_trigger_references(node)
            
            self.steps.append(TriggerStep(
                step_type='crud_call',
                operation=crud_operation,
                args=args,
                kwargs=kwargs,
                target=model_name,
                source_line=self._get_source_line(node),
                ast_node=node,
                trigger_refs=trigger_refs
            ))
    
    def _is_trigger_attr(self, node: ast.AST, attr_name: str) -> bool:
        """Verifica si un nodo es un atributo del trigger (ej: t.data, t.old)"""
        return (isinstance(node, ast.Attribute) and 
                isinstance(node.value, ast.Name) and 
                node.value.id == self.trigger_var and 
                node.attr == attr_name)
    
    def _is_trigger_method(self, node: ast.AST, method_name: str) -> bool:
        """Verifica si un nodo es una llamada a método del trigger (ej: t.log, t.abort)"""
        return (isinstance(node, ast.Attribute) and 
                isinstance(node.value, ast.Name) and 
                node.value.id == self.trigger_var and 
                node.attr == method_name)
    
    def _is_crud_method(self, node: ast.AST) -> bool:
        """Verifica si un nodo es una llamada CRUD (t.find, t.create, t.count, etc.)"""
        # Lista de métodos CRUD del TriggerAPI
        crud_methods = {
            # Read operations
            'find', 'find_many', 'count', 'exists', 'sum', 'mean', 'max', 'min',
            # Write operations
            'create', 'create_many', 'update', 'update_many', 'delete', 'delete_many'
        }
        
        return (isinstance(node, ast.Attribute) and 
                isinstance(node.value, ast.Name) and 
                node.value.id == self.trigger_var and 
                node.attr in crud_methods)
    
    def _extract_subscript_key(self, node: ast.Subscript) -> Optional[str]:
        """Extrae la clave de un subscript (ej: data['email'] -> 'email')"""
        if isinstance(node.slice, ast.Constant):
            return str(node.slice.value)
        elif isinstance(node.slice, ast.Str):  # Python < 3.8
            return node.slice.s
        return None
    
    def _ast_to_repr(self, node: ast.AST) -> str:
        """
        Convierte un nodo AST a su representación como string.
        Mantiene el código original sin transformar.
        """
        try:
            return ast.unparse(node)
        except:
            # Fallback para versiones antiguas de Python
            return ast.dump(node)
    
    def _extract_trigger_references(self, node: ast.AST) -> List[str]:
        """
        Extrae todas las referencias a TriggerAPI (t.data, t.old, t.new, t.instance)
        de un nodo AST.
        
        Returns:
            Lista de referencias encontradas (ej: ['t.data', 't.instance'])
        """
        references = []
        
        class ReferenceExtractor(ast.NodeVisitor):
            def visit_Attribute(self, node):
                if isinstance(node.value, ast.Name) and node.value.id == 't':
                    if node.attr in ['data', 'old', 'new', 'instance']:
                        references.append(f't.{node.attr}')
                self.generic_visit(node)
        
        extractor = ReferenceExtractor()
        extractor.visit(node)
        return list(set(references))  # Eliminar duplicados
    
    def _get_source_line(self, node: ast.AST) -> Optional[str]:
        """Obtiene la línea de código fuente original de un nodo AST"""
        if hasattr(node, 'lineno') and node.lineno <= len(self.source_lines):
            # lineno es 1-indexed
            return self.source_lines[node.lineno - 1].strip()
        return None


class TriggerAPI:
    """
    API que el usuario utiliza dentro de los triggers.
    
    Esta clase es SOLO para type hints y documentación.
    El generador extraerá los metadatos de uso y generará código equivalente.
    
    Attributes:
        data: Diccionario con los datos a insertar/actualizar (modificable en 'before')
        instance: Instancia del modelo actual (disponible en 'after' y 'before' de update/delete)
        old: Valores anteriores a la operación (solo en update/delete)
        new: Valores nuevos después de la operación (alias de data en update)
    
    Methods (Read):
        find(model, id, includes): Busca un registro por primary key
        find_many(model, limit, offset, **filters): Busca múltiples registros
        count(model, **filters): Cuenta registros
        exists(model, **filters): Verifica existencia
        sum(model, agg_fields, **filters): Suma campos numéricos
        mean(model, agg_fields, **filters): Calcula media
        max(model, agg_fields, **filters): Obtiene máximo
        min(model, agg_fields, **filters): Obtiene mínimo
    
    Methods (Write):
        create(model, **data): Crea un registro
        create_many(model, records): Crea múltiples registros
        update(model, id, **data): Actualiza un registro
        update_many(model, filters, **data): Actualiza múltiples registros
        delete(model, id): Elimina un registro
        delete_many(model, **filters): Elimina múltiples registros
    
    Methods (Utility):
        log(message, level): Registra un mensaje
        abort(message): Aborta la operación
    
    Note:
        Esta clase NO se instancia en runtime. Es solo para documentación y type hints.
        El generador transforma las llamadas a métodos en código imperativo.
    """
    
    @property
    def data(self) -> Dict[str, Any]:
        """
        Datos a insertar/actualizar.
        Modificable en triggers 'before'.
        
        En triggers de create: contiene los datos que se van a insertar
        En triggers de UPDATE: contiene los campos que se van a actualizar
        
        Example:
            ```python
            @on_create(timing='before')
            def normalize_data(self, t: TriggerAPI):
                t.data['email'] = t.data['email'].lower()
                t.data['name'] = t.data['name'].strip()
            ```
        
        Returns:
            Diccionario con los datos de la operación
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    @property
    def instance(self) -> Any:
        """
        Instancia del modelo actual.
        
        Disponible en:
        - Triggers 'after' (create, UPDATE, DELETE)
        - Triggers 'before' de UPDATE y DELETE
        
        No disponible en:
        - Triggers 'before' de create (aún no existe la instancia)
        
        Example:
            ```python
            @on_create(timing='after')
            def create_profile(self, t: TriggerAPI):
                user_id = t.instance.id
                t.create(Profile, user_id=user_id)
            ```
        
        Returns:
            Instancia del modelo SQLAlchemy
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    @property
    def old(self) -> Dict[str, Any]:
        """
        Valores anteriores (solo en UPDATE y DELETE).
        
        Contiene los valores de todos los campos antes de la operación.
        Útil para comparar cambios y ejecutar lógica condicional.
        
        Example:
            ```python
            @on_update(
                fields=['status'],
                when=lambda t: t.old['status'] == 'active' and t.new['status'] == 'inactive'
            )
            def on_deactivate(self, t: TriggerAPI):
                t.log(f"Usuario desactivado: {t.instance.id}")
            ```
        
        Returns:
            Diccionario con los valores anteriores
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    @property
    def new(self) -> Dict[str, Any]:
        """
        Valores nuevos (solo en UPDATE).
        
        Alias de t.data para mejor legibilidad en triggers de update.
        Útil para comparar valores antiguos vs nuevos.
        
        Example:
            ```python
            @on_update(fields=['price'])
            def check_price_change(self, t: TriggerAPI):
                old_price = t.old['price']
                new_price = t.new['price']
                if new_price > old_price * 1.5:
                    t.abort("El precio no puede aumentar más del 50%")
            ```
        
        Returns:
            Diccionario con los valores nuevos (mismo que t.data)
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    # ============================================
    # Métodos de lectura
    # ============================================
    
    def find(self, model: Type[Table], id: Any, includes: Optional[List[str]] = None) -> Any:
        """
        Busca un único registro por primary key.
        
        Args:
            model: Clase del modelo (Usuario, Post, Comment, etc.)
            id: Valor de la primary key
            includes: Lista de relaciones a incluir
        
        Returns:
            Instancia del modelo o None si no se encuentra
        
        Example:
            ```python
            @on_create(timing='after')
            def create_profile(self, t: TriggerAPI):
                user = t.find(Usuario, id=t.instance.author_id)
                if user:
                    t.log(f"Autor: {user.name}")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def find_many(
        self, 
        model: Type[Table], 
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[str]] = None,
        order: str = "ASC",
        includes: Optional[List[str]] = None,
        **filters
    ) -> List[Any]:
        """
        Busca múltiples registros con filtros.
        
        Args:
            model: Clase del modelo
            limit: Límite de registros
            offset: Número de registros a saltar
            order_by: Lista de campos para ordenar
            order: 'ASC' o 'DESC'
            includes: Relaciones a incluir
            **filters: Filtros adicionales (campo=valor)
        
        Returns:
            Lista de instancias del modelo
        
        Example:
            ```python
            @on_update(timing='after', fields=['status'])
            def notify_related(self, t: TriggerAPI):
                posts = t.find_many(
                    Post, 
                    author_id=t.instance.id,
                    limit=10
                )
                t.log(f"Usuario tiene {len(posts)} posts")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def count(self, model: Type[Table], **filters) -> int:
        """
        Cuenta registros que coincidan con los filtros.
        
        Args:
            model: Clase del modelo
            **filters: Filtros (campo=valor)
        
        Returns:
            Número de registros
        
        Example:
            ```python
            @on_delete(timing='before')
            def check_dependencies(self, t: TriggerAPI):
                post_count = t.count(Post, author_id=t.instance.id)
                if post_count > 0:
                    t.abort(f"No se puede eliminar usuario con {post_count} posts")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def exists(self, model: Type[Table], **filters) -> bool:
        """
        Verifica si existe al menos un registro con los filtros.
        
        Args:
            model: Clase del modelo
            **filters: Filtros (campo=valor)
        
        Returns:
            True si existe al menos un registro
        
        Example:
            ```python
            @on_create(timing='before')
            def validate_unique_email(self, t: TriggerAPI):
                if t.exists(Usuario, email=t.data['email']):
                    t.abort("El email ya está registrado")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def sum(self, model: Type[Table], agg_fields: List[str], **filters) -> Dict[str, Optional[float]]:
        """
        Suma valores de campos numéricos.
        
        Args:
            model: Clase del modelo
            agg_fields: Lista de campos a sumar
            **filters: Filtros (campo=valor)
        
        Returns:
            Diccionario con las sumas {"sum_<field>": value}
        
        Example:
            ```python
            @on_update(timing='after')
            def update_totals(self, t: TriggerAPI):
                totals = t.sum(Order, agg_fields=['amount'], user_id=t.instance.id)
                t.log(f"Total: ${totals['sum_amount']}")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def mean(self, model: Type[Table], agg_fields: List[str], **filters) -> Dict[str, Optional[float]]:
        """
        Calcula la media de campos numéricos.
        
        Args:
            model: Clase del modelo
            agg_fields: Lista de campos
            **filters: Filtros (campo=valor)
        
        Returns:
            Diccionario con las medias {"mean_<field>": value}
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def max(self, model: Type[Table], agg_fields: List[str], **filters) -> Dict[str, Optional[Any]]:
        """
        Obtiene el valor máximo de campos.
        
        Args:
            model: Clase del modelo
            agg_fields: Lista de campos
            **filters: Filtros (campo=valor)
        
        Returns:
            Diccionario con los máximos {"max_<field>": value}
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def min(self, model: Type[Table], agg_fields: List[str], **filters) -> Dict[str, Optional[Any]]:
        """
        Obtiene el valor mínimo de campos.
        
        Args:
            model: Clase del modelo
            agg_fields: Lista de campos
            **filters: Filtros (campo=valor)
        
        Returns:
            Diccionario con los mínimos {"min_<field>": value}
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    # ============================================
    # Métodos de escritura
    # ============================================
    
    def create(self, model: Type[Table], **data) -> Any:
        """
        Crea un nuevo registro.
        
        Args:
            model: Clase del modelo
            **data: Datos del registro a crear
        
        Returns:
            Instancia del modelo creado
        
        Example:
            ```python
            @on_create(timing='after')
            def create_profile(self, t: TriggerAPI):
                profile = t.create(
                    Profile,
                    user_id=t.instance.id,
                    bio="Nuevo usuario"
                )
                t.log(f"Perfil creado: {profile.id}")
            ```
        
        Note:
            La operación se ejecuta en la misma sesión/transacción del trigger.
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def create_many(self, model: Type[Table], records: List[Dict[str, Any]]) -> int:
        """
        Crea múltiples registros.
        
        Args:
            model: Clase del modelo
            records: Lista de diccionarios con los datos
        
        Returns:
            Número de registros creados
        
        Example:
            ```python
            @on_create(timing='after')
            def create_default_tags(self, t: TriggerAPI):
                tags = [
                    {'post_id': t.instance.id, 'name': 'nuevo'},
                    {'post_id': t.instance.id, 'name': 'destacado'}
                ]
                count = t.create_many(Tag, records=tags)
                t.log(f"{count} tags creados")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def update(self, model: Type[Table], id: Any, **data) -> int:
        """
        Actualiza un registro por primary key.
        
        Args:
            model: Clase del modelo
            id: Valor de la primary key
            **data: Campos a actualizar
        
        Returns:
            Número de registros actualizados (0 o 1)
        
        Example:
            ```python
            @on_create(timing='after')
            def update_user_stats(self, t: TriggerAPI):
                t.update(
                    UserStats,
                    id=t.instance.author_id,
                    post_count=10
                )
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def update_many(self, model: Type[Table], filters: Dict[str, Any], **data) -> int:
        """
        Actualiza múltiples registros que coincidan con los filtros.
        
        Args:
            model: Clase del modelo
            filters: Diccionario con filtros (campo=valor)
            **data: Campos a actualizar
        
        Returns:
            Número de registros actualizados
        
        Example:
            ```python
            @on_update(timing='after', fields=['status'])
            def archive_related(self, t: TriggerAPI):
                updated = t.update_many(
                    Post,
                    filters={'author_id': t.instance.id},
                    archived=True
                )
                t.log(f"{updated} posts archivados")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def delete(self, model: Type[Table], id: Any) -> int:
        """
        Elimina un registro por primary key.
        
        Args:
            model: Clase del modelo
            id: Valor de la primary key
        
        Returns:
            Número de registros eliminados (0 o 1)
        
        Example:
            ```python
            @on_delete(timing='before')
            def delete_profile(self, t: TriggerAPI):
                deleted = t.delete(Profile, id=t.instance.id)
                t.log(f"Perfil eliminado: {deleted}")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def delete_many(self, model: Type[Table], **filters) -> int:
        """
        Elimina múltiples registros que coincidan con los filtros.
        
        Args:
            model: Clase del modelo
            **filters: Filtros (campo=valor)
        
        Returns:
            Número de registros eliminados
        
        Example:
            ```python
            @on_delete(timing='before')
            def cascade_delete(self, t: TriggerAPI):
                deleted = t.delete_many(Post, author_id=t.instance.id)
                t.log(f"{deleted} posts eliminados")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    # ============================================
    # Métodos de utilidad
    # ============================================
    
    def log(self, message: str, level: str = 'info') -> None:
        """
        Registra un mensaje en el logger del sistema.
        
        Args:
            message: Mensaje a registrar
            level: Nivel de log. Valores: 'info', 'warning', 'error', 'debug'
        
        Example:
            ```python
            @on_update(fields=['status'])
            def log_status_change(self, t: TriggerAPI):
                t.log(f"Estado cambiado de {t.old['status']} a {t.new['status']}")
                
                if t.new['status'] == 'deleted':
                    t.log("Usuario marcado para eliminación", level='warning')
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    def abort(self, message: str) -> None:
        """
        Aborta la operación lanzando una excepción.
        
        Útil para validaciones que deben detener la operación CRUD.
        La excepción causa un rollback de toda la transacción.
        
        Args:
            message: Mensaje de error descriptivo
        
        Raises:
            ValueError: Siempre lanza esta excepción con el mensaje proporcionado
        
        Example:
            ```python
            @on_update(timing='before', fields=['price'])
            def validate_price(self, t: TriggerAPI):
                if t.data['price'] < 0:
                    t.abort("El precio no puede ser negativo")
                
                if t.data['price'] > t.old['price'] * 2:
                    t.abort("El precio no puede duplicarse en una sola actualización")
            ```
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    """
    API que el usuario utiliza dentro de los triggers.
    
    Esta clase es SOLO para type hints y documentación.
    El generador extraerá los metadatos de uso y generará código equivalente.
    
    Attributes:
        data: Diccionario con los datos a insertar/actualizar (modificable en 'before')
        instance: Instancia del modelo actual (disponible en 'after' y 'before' de update/delete)
        old: Valores anteriores a la operación (solo en update/delete)
        new: Valores nuevos después de la operación (alias de data en update)
    
    Methods:
        dao(model): Obtiene el DAO de otra tabla para operaciones CRUD
        log(message, level): Registra un mensaje en el logger
        abort(message): Aborta la operación lanzando una excepción
    
    Note:
        Esta clase NO se instancia en runtime. Es solo para documentación y type hints.
        El generador transforma las llamadas a métodos en código imperativo.
    """
    
    @property
    def data(self) -> Dict[str, Any]:
        """
        Datos a insertar/actualizar.
        Modificable en triggers 'before'.
        
        En triggers de create: contiene los datos que se van a insertar
        En triggers de UPDATE: contiene los campos que se van a actualizar
        
        Example:
            ```python
            @on_create(timing='before')
            def normalize_data(self, t: TriggerAPI):
                t.data['email'] = t.data['email'].lower()
                t.data['name'] = t.data['name'].strip()
            ```
        
        Returns:
            Diccionario con los datos de la operación
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    @property
    def instance(self) -> Any:
        """
        Instancia del modelo actual.
        
        Disponible en:
        - Triggers 'after' (create, UPDATE, DELETE)
        - Triggers 'before' de UPDATE y DELETE
        
        No disponible en:
        - Triggers 'before' de create (aún no existe la instancia)
        
        Example:
            ```python
            @on_create(timing='after')
            def create_profile(self, t: TriggerAPI):
                user_id = t.instance.id
                t.dao(Profile).create(user_id=user_id)
            ```
        
        Returns:
            Instancia del modelo SQLAlchemy
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    @property
    def old(self) -> Dict[str, Any]:
        """
        Valores anteriores (solo en UPDATE y DELETE).
        
        Contiene los valores de todos los campos antes de la operación.
        Útil para comparar cambios y ejecutar lógica condicional.
        
        Example:
            ```python
            @on_update(
                fields=['status'],
                when=lambda t: t.old['status'] == 'active' and t.new['status'] == 'inactive'
            )
            def on_deactivate(self, t: TriggerAPI):
                t.log(f"Usuario desactivado: {t.instance.id}")
            ```
        
        Returns:
            Diccionario con los valores anteriores
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")
    
    @property
    def new(self) -> Dict[str, Any]:
        """
        Valores nuevos (solo en UPDATE).
        
        Alias de t.data para mejor legibilidad en triggers de update.
        Útil para comparar valores antiguos vs nuevos.
        
        Example:
            ```python
            @on_update(fields=['price'])
            def check_price_change(self, t: TriggerAPI):
                old_price = t.old['price']
                new_price = t.new['price']
                if new_price > old_price * 1.5:
                    t.abort("El precio no puede aumentar más del 50%")
            ```
        
        Returns:
            Diccionario con los valores nuevos (mismo que t.data)
        """
        raise NotImplementedError("TriggerAPI es solo para type hints")


class Trigger(AutoRegisterDescriptor):
    """
    Descriptor que representa un trigger definido en un modelo.
    
    Utiliza el protocolo de descriptores para auto-registrarse en el modelo
    cuando se asigna como atributo de clase.
    
    Attributes:
        name: Nombre del método trigger
        event: Tipo de evento ('create', 'update', 'delete')
        timing: Momento de ejecución ('before', 'after')
        priority: Orden de ejecución (menor número = mayor prioridad)
        fields: Lista de campos que activan el trigger (solo para UPDATE)
        when_lambda: Función lambda de condición (puede ser None)
        when_source: Código fuente de la lambda como string
        function: Función original del trigger
        source_code: Código fuente completo de la función
        ast_tree: Árbol AST de la función para análisis y transformación
        docstring: Documentación del trigger
        owner: Referencia al modelo Table al que pertenece
    """
    
    @property
    def collection_name(self) -> str:
        """Nombre de la colección en Table donde se almacenan los triggers"""
        return 'triggers'
    
    @property
    def registry_key(self) -> Optional[str]:
        """Clave del evento para registrar el trigger ('create', 'update', 'delete')"""
        return self.event
    
    def __init__(
        self,
        event: str,
        timing: str = 'before',
        priority: int = 1,
        fields: Optional[List[str]] = None,
        when_lambda: Optional[Callable] = None,
        when_source: Optional[str] = None,
        function: Optional[Callable] = None,
        source_code: Optional[str] = None,
        ast_tree: Optional[ast.FunctionDef] = None,
        docstring: Optional[str] = None
    ):
        """
        Inicializa un nuevo trigger.
        
        Args:
            event: Tipo de evento ('create', 'update', 'delete')
            timing: Momento de ejecución ('before' o 'after')
            priority: Orden de ejecución (menor número = mayor prioridad)
            fields: Lista de campos que activan el trigger (solo para UPDATE)
            when_lambda: Función lambda de condición
            when_source: Código fuente de la lambda
            function: Función original del trigger
            source_code: Código fuente completo de la función
            ast_tree: Árbol AST de la función
            docstring: Documentación del trigger
        """
        super().__init__()
        self.event = event
        self.timing = timing
        self.priority = priority
        self.fields = fields
        self.when_lambda = when_lambda
        self.when_source = when_source
        self.function = function
        self.source_code = source_code
        self.ast_tree = ast_tree
        self.docstring = docstring
        self.steps: List[TriggerStep] = []
        
        # Analizar el AST para extraer los steps
        if ast_tree is not None and source_code is not None:
            self._analyze_steps()
    
    def _analyze_steps(self) -> None:
        """
        Analiza el AST del trigger para extraer los steps basados en TriggerAPI.
        """
        if not self.ast_tree or not self.source_code:
            return
        
        # Obtener las líneas de código fuente
        source_lines = self.source_code.split('\n')
        
        # Crear el analizador y visitar el AST
        analyzer = TriggerAnalyzer(source_lines)
        analyzer.visit(self.ast_tree)
        
        # Guardar los steps encontrados
        self.steps = analyzer.steps
    
    def _initialize_collection(self, owner: Table):
        """
        Inicializa el diccionario de triggers con estructura anidada por evento.
        """
        # Obtener la colección actual (puede ser un dict vacío de __init_subclass__)
        current = getattr(owner, self.collection_name, None)
        
        # Si no tiene la estructura correcta (con keys 'create', 'update', 'delete'), inicializar
        if not isinstance(current, dict) or 'create' not in current:
            setattr(owner, self.collection_name, {
                'create': [],
                'update': [],
                'delete': []
            })
    
    def __get__(self, instance, owner: Table):
        """
        Protocolo de descriptores: retorna la función original cuando se accede al trigger.
        
        Args:
            instance: La instancia desde la que se accede (None si es desde la clase)
            owner: La clase propietaria
        
        Returns:
            El trigger mismo si se accede desde la clase,
            o la función bound si se accede desde una instancia
        """
        if instance is None:
            return self
        return self.function.__get__(instance, owner)
    
    def info(self) -> Dict[str, Any]:
        """
        Devuelve un diccionario con la información del trigger.
        """
        return {
            'name': self.name,
            'event': self.event,
            'timing': self.timing,
            'priority': self.priority,
            'fields': self.fields,
            'when_source': self.when_source,
            'docstring': self.docstring,
            'has_condition': self.when_lambda is not None,
            'steps': [step.to_dict() for step in self.steps],
            'steps_count': len(self.steps)
        }
    
    def __repr__(self) -> str:
        """Representación en string del trigger"""
        return f"<Trigger {self.name}({self.event}, {self.timing}, priority={self.priority})>"


def on_create(
    timing: str = 'before',
    priority: int = 1,
    when: Optional[Callable[[TriggerAPI], bool]] = None
):
    """
    Decorador para definir triggers de create.
    
    Los triggers de create se ejecutan cuando se crea un nuevo registro.
    
    Args:
        timing: Momento de ejecución:
            - 'before': Antes de insertar el registro (puede modificar datos)
            - 'after': Después de insertar el registro (acceso a instance.id)
        priority: Orden de ejecución cuando hay múltiples triggers (menor = primero)
        when: Lambda opcional con condición. Si retorna False, no se ejecuta el trigger
    
    Returns:
        Decorador que marca el método como trigger de create
    
    Example:
        ```python
        @on_create(timing='before', priority=1)
        def normalize_email(self, t: TriggerAPI):
            '''Normaliza el email antes de insertar'''
            t.data['email'] = t.data['email'].lower().strip()
        
        @on_create(timing='after', priority=2)
        def create_profile(self, t: TriggerAPI):
            '''Crea perfil automáticamente'''
            t.dao(Profile).create(user_id=t.instance.id)
        
        @on_create(
            timing='before',
            when=lambda t: '@' not in t.data.get('email', '')
        )
        def validate_email(self, t: TriggerAPI):
            '''Valida formato de email'''
            t.abort("Email inválido")
        ```
    
    Note:
        - En triggers 'before' de create, t.instance no está disponible
        - En triggers 'after' de create, t.instance contiene el registro creado con su ID
    """
    def decorator(func: Callable) -> Callable:
        # Extraer código fuente y AST
        try:
            source = inspect.getsource(func)
            # Limpiar indentación para parsing
            source = textwrap.dedent(source)
            tree = ast.parse(source)
            func_ast = tree.body[0]
        except Exception as e:
            raise RuntimeError(f"No se pudo extraer el código fuente del trigger '{func.__name__}': {e}")
        
        # Extraer código fuente de la lambda 'when' si existe
        when_source = None
        if when is not None:
            try:
                when_source = inspect.getsource(when).strip()
                # Limpiar el código (remover lambda t:)
                if 'lambda' in when_source:
                    when_source = when_source.split('lambda')[1].strip()
                    if when_source.startswith('t:'):
                        when_source = when_source[2:].strip()
            except:
                # Si no se puede extraer, usar la representación
                when_source = str(when)
        
        # Crear y retornar el objeto Trigger como descriptor
        # El descriptor se auto-registrará cuando se asigne a la clase
        trigger = Trigger(
            event='create',
            timing=timing,
            priority=priority,
            fields=None,
            when_lambda=when,
            when_source=when_source,
            function=func,
            source_code=source,
            ast_tree=func_ast,
            docstring=func.__doc__
        )
        
        return trigger
    return decorator


def on_update(
    timing: str = 'before',
    priority: int = 1,
    fields: Optional[List[str]] = None,
    when: Optional[Callable[[TriggerAPI], bool]] = None
):
    """
    Decorador para definir triggers de UPDATE.
    
    Los triggers de UPDATE se ejecutan cuando se actualiza un registro existente.
    
    Args:
        timing: Momento de ejecución:
            - 'before': Antes de actualizar (puede modificar datos)
            - 'after': Después de actualizar (cambios ya persistidos)
        priority: Orden de ejecución cuando hay múltiples triggers (menor = primero)
        fields: Lista de campos que activan el trigger. Si None, se ejecuta siempre
        when: Lambda opcional con condición. Recibe TriggerAPI y retorna bool
    
    Returns:
        Decorador que marca el método como trigger de UPDATE
    
    Example:
        ```python
        # Ejecutar en cualquier update
        @on_update(timing='before')
        def update_modified_at(self, t: TriggerAPI):
            '''Actualiza timestamp de modificación'''
            t.data['modified_at'] = datetime.now()
        
        # Solo cuando cambian campos específicos
        @on_update(timing='after', fields=['status'])
        def log_status_change(self, t: TriggerAPI):
            '''Registra cambios de estado'''
            t.log(f"Estado: {t.old['status']} -> {t.new['status']}")
        
        # Con condición compleja
        @on_update(
            timing='before',
            fields=['status'],
            when=lambda t: t.old['status'] == 'active' and t.new['status'] == 'inactive'
        )
        def archive_on_deactivate(self, t: TriggerAPI):
            '''Archiva datos cuando se desactiva'''
            t.dao(Post).update_many(
                filters={'author_id': t.instance.id},
                archived=True
            )
        ```
    
    Note:
        - t.old contiene los valores antes del update
        - t.new (alias de t.data) contiene los valores nuevos
        - t.instance está disponible en ambos timings
    """
    def decorator(func: Callable) -> Callable:
        try:
            source = inspect.getsource(func)
            import textwrap
            source = textwrap.dedent(source)
            tree = ast.parse(source)
            func_ast = tree.body[0]
        except Exception as e:
            raise RuntimeError(f"No se pudo extraer el código fuente del trigger '{func.__name__}': {e}")
        
        when_source = None
        if when is not None:
            try:
                when_source = inspect.getsource(when).strip()
                if 'lambda' in when_source:
                    when_source = when_source.split('lambda')[1].strip()
                    if when_source.startswith('t:'):
                        when_source = when_source[2:].strip()
            except:
                when_source = str(when)
        
        trigger = Trigger(
            event='update',
            timing=timing,
            priority=priority,
            fields=fields,
            when_lambda=when,
            when_source=when_source,
            function=func,
            source_code=source,
            ast_tree=func_ast,
            docstring=func.__doc__
        )
        
        return trigger
    return decorator


def on_delete(
    timing: str = 'before',
    priority: int = 1,
    when: Optional[Callable[[TriggerAPI], bool]] = None
):
    """
    Decorador para definir triggers de DELETE.
    
    Los triggers de DELETE se ejecutan cuando se elimina un registro.
    
    Args:
        timing: Momento de ejecución:
            - 'before': Antes de eliminar (puede hacer operaciones con el registro)
            - 'after': Después de eliminar (registro ya no existe en DB)
        priority: Orden de ejecución cuando hay múltiples triggers (menor = primero)
        when: Lambda opcional con condición. Recibe TriggerAPI y retorna bool
    
    Returns:
        Decorador que marca el método como trigger de DELETE
    
    Example:
        ```python
        @on_delete(timing='before', priority=1)
        def cascade_delete_posts(self, t: TriggerAPI):
            '''Elimina posts relacionados'''
            deleted = t.dao(Post).delete_many(
                filters={'author_id': t.instance.id}
            )
            t.log(f"Eliminados {deleted} posts del usuario {t.instance.id}")
        
        @on_delete(timing='before', priority=2)
        def archive_before_delete(self, t: TriggerAPI):
            '''Archiva datos antes de eliminar'''
            t.dao(Archive).create(
                table='usuario',
                record_id=t.instance.id,
                data=t.instance.to_dict()
            )
        
        @on_delete(
            timing='after',
            when=lambda t: t.old['is_premium']
        )
        def notify_premium_deletion(self, t: TriggerAPI):
            '''Notifica eliminación de usuario premium'''
            t.log(f"Usuario premium eliminado: {t.old['email']}", level='warning')
        ```
    
    Note:
        - t.instance está disponible en 'before'
        - En 'after', el registro ya no existe, usar t.old para acceder a valores
    """
    def decorator(func: Callable) -> Callable:
        try:
            source = inspect.getsource(func)
            import textwrap
            source = textwrap.dedent(source)
            tree = ast.parse(source)
            func_ast = tree.body[0]
        except Exception as e:
            raise RuntimeError(f"No se pudo extraer el código fuente del trigger '{func.__name__}': {e}")
        
        when_source = None
        if when is not None:
            try:
                when_source = inspect.getsource(when).strip()
                if 'lambda' in when_source:
                    when_source = when_source.split('lambda')[1].strip()
                    if when_source.startswith('t:'):
                        when_source = when_source[2:].strip()
            except:
                when_source = str(when)
        
        trigger = Trigger(
            event='delete',
            timing=timing,
            priority=priority,
            fields=None,
            when_lambda=when,
            when_source=when_source,
            function=func,
            source_code=source,
            ast_tree=func_ast,
            docstring=func.__doc__
        )
        
        return trigger
    return decorator
