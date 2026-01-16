"""
Descriptores base para el sistema de ORM de tai-sql.

Este módulo proporciona clases base para implementar el patrón descriptor
de manera consistente en toda la aplicación, permitiendo auto-registro
mediante __set_name__.
"""
from __future__ import annotations
from typing import Any, Dict, TypeVar, Generic, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .table import Table

T = TypeVar('T')


class AutoRegisterDescriptor(ABC):
    """
    Clase base abstracta para descriptores que se auto-registran en la clase propietaria.
    
    Los descriptores que heredan de esta clase se registran automáticamente
    cuando se asignan como atributos de clase, usando el protocolo __set_name__.
    
    Cada tipo de descriptor debe especificar:
    - collection_name: El nombre del atributo ClassVar donde se almacenan (ej: 'triggers', 'relations')
    - registry_key: Opcional, si el collection es un diccionario con subcategorías (ej: 'insert' para triggers)
    """
    
    def __init__(self):
        """Inicializa el descriptor"""
        self.name: Optional[str] = None
        self.owner: Optional[Table] = None
    
    @property
    @abstractmethod
    def collection_name(self) -> str:
        """
        Nombre del atributo ClassVar en la clase propietaria donde se almacenan
        estos descriptores.
        
        Ejemplos:
        - 'triggers' para Trigger
        - 'relations' para Relation
        - 'rbac' para permisos
        """
        pass
    
    @property
    def registry_key(self) -> Optional[str]:
        """
        Clave opcional para registros que usan diccionarios anidados.
        
        Por ejemplo, para Trigger:
        - Si event='insert', retorna 'insert'
        - El trigger se guarda en owner.triggers['insert']
        
        Si retorna None, el descriptor se guarda directamente en la colección.
        """
        return None
    
    def __set_name__(self, owner: Table, name: str):
        """
        Protocolo de descriptores: se llama automáticamente cuando el descriptor
        se asigna como atributo de una clase.
        
        Args:
            owner: La clase Table a la que pertenece el descriptor
            name: El nombre del atributo
        """
        self.name = name
        self.owner = owner
        
        # Asegurar que la colección existe y tiene la estructura correcta
        self._initialize_collection(owner)
        
        # Registrar el descriptor
        self._register_in_collection(owner)
    
    def _initialize_collection(self, owner: Table):
        """
        Inicializa la colección en la clase propietaria.
        
        Debe ser sobrescrito si la estructura de la colección no es un dict simple.
        """
        collection = getattr(owner, self.collection_name, None)
        
        # Si la colección no existe o es heredada, crear una nueva
        if self.registry_key is not None:
            # Colección con subcategorías (ej: triggers)
            setattr(owner, self.collection_name, {})
        else:
            # Colección simple (ej: relations)
            setattr(owner, self.collection_name, {})
    
    def _register_in_collection(self, owner: Table):
        """
        Registra este descriptor en la colección de la clase propietaria.
        """
        collection = getattr(owner, self.collection_name)
        
        if self.registry_key is not None:
            # Registrar en subcategoría
            if self.registry_key not in collection:
                collection[self.registry_key] = []
            collection[self.registry_key].append(self)
        else:
            # Registrar directamente
            if isinstance(collection, dict):
                collection[self.name] = self
            elif isinstance(collection, list):
                collection.append(self)
            else:
                raise TypeError(
                    f"La colección '{self.collection_name}' debe ser dict o list, "
                    f"no {type(collection).__name__}"
                )
    
    def __get__(self, instance, owner):
        """
        Protocolo de descriptores: se llama cuando se accede al atributo.
        
        Args:
            instance: La instancia desde la que se accede (None si es desde la clase)
            owner: La clase propietaria
        
        Returns:
            El descriptor mismo cuando se accede desde la clase
        """
        if instance is None:
            return self
        # Para acceso desde instancia, retornar el descriptor
        # (las subclases pueden sobrescribir esto)
        return self
    
    @abstractmethod
    def info(self) -> Dict[str, Any]:
        """
        Retorna información del descriptor en formato diccionario.
        
        Debe ser implementado por las subclases.
        """
        pass
    
    def __repr__(self) -> str:
        """Representación en string del descriptor"""
        return f"<{self.__class__.__name__} {self.name}>"


class CollectionManager(Generic[T]):
    """
    Administrador de colecciones para descriptores auto-registrables.
    
    Esta clase se puede usar como ClassVar en Table para gestionar
    colecciones de descriptores de forma más explícita y con mejor tipo.
    """
    
    def __init__(self, descriptor_type: type):
        """
        Args:
            descriptor_type: El tipo de descriptor que esta colección administra
        """
        self.descriptor_type = descriptor_type
        self._items: Dict[str, T] = {}
    
    def __set_name__(self, owner, name):
        """Registra el nombre de esta colección"""
        self.name = name
        self.owner = owner
    
    def __get__(self, instance, owner) -> Dict[str, T]:
        """Retorna el diccionario de items"""
        return self._items
    
    def add(self, item: T):
        """Agrega un item a la colección"""
        if not isinstance(item, self.descriptor_type):
            raise TypeError(
                f"Solo se pueden agregar items de tipo {self.descriptor_type.__name__}"
            )
        self._items[item.name] = item
    
    def clear(self):
        """Limpia la colección"""
        self._items.clear()
    
    def __iter__(self):
        """Permite iterar sobre los items"""
        return iter(self._items.values())
    
    def __len__(self):
        """Retorna el número de items"""
        return len(self._items)
