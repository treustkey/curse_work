# модель проекта
from datetime import datetime
import json


class Project:
    def __init__(self, project_id=None, name="", doc_type="ГОСТ 34.602-89",
                 system_type="", deadline=None, description="",
                 func_req=None, nonfunc_req=None):
        self.project_id = project_id
        self.name = name
        self.doc_type = doc_type
        self.system_type = system_type
        self.deadline = deadline
        self.description = description
        self.func_req = func_req if func_req else {}
        self.nonfunc_req = nonfunc_req if nonfunc_req else {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        # преобразование объекта в словарь для сохранения
        data = {
            'project_id': self.project_id,
            'name': self.name,
            'doc_type': self.doc_type,
            'system_type': self.system_type,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'description': self.description,
            'func_req': json.dumps(self.func_req, ensure_ascii=False),
            'nonfunc_req': json.dumps(self.nonfunc_req, ensure_ascii=False),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        return data

    @classmethod
    def from_dict(cls, data):
        # создание объекта из словаря
        proj = cls(
            project_id=data.get('project_id'),
            name=data.get('name', ''),
            doc_type=data.get('doc_type', 'ГОСТ 34.602-89'),
            system_type=data.get('system_type', ''),
            deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
            description=data.get('description', ''),
            func_req=json.loads(data.get('func_req', '{}')),
            nonfunc_req=json.loads(data.get('nonfunc_req', '{}'))
        )
        if data.get('created_at'):
            proj.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('updated_at'):
            proj.updated_at = datetime.fromisoformat(data['updated_at'])
        return proj
