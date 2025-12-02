# работа с базой данных SQLite
import sqlite3
import os
from .project import Project


class Database:
    def __init__(self):
        # создаём папку если нет
        if not os.path.exists('data'):
            os.makedirs('data')

        # подключение к базе
        self.db_path = 'data/projects.db'
        self.conn = None
        self.create_tables()

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        # таблица проектов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                doc_type TEXT NOT NULL,
                system_type TEXT,
                deadline TEXT,
                description TEXT,
                func_req TEXT,
                nonfunc_req TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')

        conn.commit()

    def save_project(self, project):
        conn = self.connect()
        cursor = conn.cursor()

        data = project.to_dict()

        if project.project_id:
            # обновление
            cursor.execute('''
                UPDATE projects
                SET name=?, doc_type=?, system_type=?, deadline=?,
                    description=?, func_req=?, nonfunc_req=?, updated_at=?
                WHERE project_id=?
            ''', (
                data['name'], data['doc_type'], data['system_type'],
                data['deadline'], data['description'], data['func_req'],
                data['nonfunc_req'], data['updated_at'], project.project_id
            ))
            project_id = project.project_id
        else:
            # создание нового
            cursor.execute('''
                INSERT INTO projects (
                    name, doc_type, system_type, deadline,
                    description, func_req, nonfunc_req,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['name'], data['doc_type'], data['system_type'],
                data['deadline'], data['description'], data['func_req'],
                data['nonfunc_req'], data['created_at'], data['updated_at']
            ))
            project_id = cursor.lastrowid
            project.project_id = project_id

        conn.commit()
        return project_id

    def load_project(self, project_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
        row = cursor.fetchone()

        if row:
            return Project.from_dict(dict(row))
        return None

    def get_all_projects(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects ORDER BY updated_at DESC')
        rows = cursor.fetchall()

        projects = []
        for row in rows:
            projects.append(Project.from_dict(dict(row)))

        return projects

    def delete_project(self, project_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM projects WHERE project_id = ?', (project_id,))
        conn.commit()
        return cursor.rowcount > 0
