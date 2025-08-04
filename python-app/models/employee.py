from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Departamento:
    deptno: int
    dname: str
    loc: str
    
    def to_dict(self) -> Dict:
        return {
            "deptno": self.deptno,
            "dname": self.dname,
            "loc": self.loc
        }

@dataclass
class Empleado:
    empno: int
    ename: str
    job: str
    sal: float
    departamento: Departamento
    
    def to_dict(self) -> Dict:
        return {
            "empno": self.empno,
            "ename": self.ename,
            "job": self.job,
            "sal": self.sal,
            "departamento": self.departamento.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Empleado':
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