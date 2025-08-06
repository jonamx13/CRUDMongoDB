"""
Definición de modelos de datos usando dataclasses
Representa la estructura de empleados y departamentos
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class Departamento:
    """
    Modelo de datos para un departamento
    
    Attributes:
        deptno: Número de departamento
        dname: Nombre del departamento
        loc: Ubicación del departamento
    """
    deptno: int
    dname: str
    loc: str
    
    def to_dict(self) -> Dict:
        """
        Convierte el objeto a diccionario
        
        Returns:
            dict: Representación en diccionario del departamento
        """
        return {
            "deptno": self.deptno,
            "dname": self.dname,
            "loc": self.loc
        }

@dataclass
class Empleado:
    """
    Modelo de datos para un empleado
    
    Attributes:
        empno: Número de empleado
        ename: Nombre del empleado
        job: Puesto del empleado
        sal: Salario del empleado
        departamento: Departamento asociado (objeto Departamento)
    """
    empno: int
    ename: str
    job: str
    sal: float
    departamento: Departamento
    
    def to_dict(self) -> Dict:
        """
        Convierte el objeto a diccionario
        
        Returns:
            dict: Representación en diccionario del empleado
        """
        return {
            "empno": self.empno,
            "ename": self.ename,
            "job": self.job,
            "sal": self.sal,
            "departamento": self.departamento.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Empleado':
        """
        Crea un Empleado desde un diccionario
        
        Args:
            data: Diccionario con datos del empleado
            
        Returns:
            Empleado: Instancia de Empleado
        """
        dept_data = data.get('departamento', {})
        departamento = Departamento(
            deptno=dept_data.get('deptno'),
            dname=dept_data.get('dname'),
            loc=dept_data.get('loc')
        )
        
        return cls(
            empno=data.get('empno'),
            ename=data.get('ename'),
            job=data.get('job'),
            sal=data.get('sal'),
            departamento=departamento
        )