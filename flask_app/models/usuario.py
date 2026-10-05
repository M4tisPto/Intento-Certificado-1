import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
BD = "esquema_cinepedia"
class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(BD).query_db(query, data)
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL(BD).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    @staticmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        result = connectToMySQL(BD).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_register(form):
        is_valid = True
        if len(form['nombre']) < 2:
            flash("El nombre debe tener al menos 2 letras", "registro")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash("E-mail inválido", "registro")
            is_valid = False
        if form['password'] != form['confirmar']:
            flash("Las contraseñas no coinciden", "registro")
            is_valid = False
        return is_valid
    