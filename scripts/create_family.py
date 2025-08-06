#!/usr/bin/env python3
"""
Script para criar famílias no sistema Family Office

Uso:
    python scripts/create_family.py "Nome da Família"                    # Criar uma família
    python scripts/create_family.py --name "Nome da Família"            # Criar uma família
    python scripts/create_family.py --list                              # Listar todas as famílias
    python scripts/create_family.py --admin-email admin@admin.com       # Especificar email do admin
    python scripts/create_family.py --add-user user@example.com         # Adicionar usuário à família
"""

import sys
import os
import argparse
import requests
import json

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.family import Family
from app.models.user import User
from app.config.extensions import db

def get_admin_token(admin_email="admin@admin.com", password="admin123"):
    """Obtém token de admin para autenticação"""
    try:
        response = requests.post("http://localhost:5000/auth/login", json={
            "email": admin_email,
            "password": password
        })
        
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Erro ao fazer login: {response.json()}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor. Certifique-se de que o Flask está rodando.")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None

def create_family_api(name, admin_token):
    """Cria família via API"""
    try:
        response = requests.post("http://localhost:5000/admin/families", 
            json={"name": name},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if response.status_code == 201:
            family_data = response.json()
            print(f"✅ Família '{name}' criada com sucesso! (ID: {family_data['id']})")
            return family_data
        else:
            error_msg = response.json().get("error", "Erro desconhecido")
            print(f"❌ Erro ao criar família: {error_msg}")
            return None
    except Exception as e:
        print(f"❌ Erro ao criar família via API: {e}")
        return None

def create_family_direct(name):
    """Cria família diretamente no banco de dados"""
    try:
        app = create_app()
        with app.app_context():
            # Verificar se família já existe
            existing_family = Family.query.filter_by(name=name).first()
            if existing_family:
                print(f"⚠️  Família '{name}' já existe! (ID: {existing_family.id})")
                return existing_family
            
            # Criar nova família
            family = Family(name=name)
            db.session.add(family)
            db.session.commit()
            
            print(f"✅ Família '{name}' criada com sucesso! (ID: {family.id})")
            return family
    except Exception as e:
        print(f"❌ Erro ao criar família: {e}")
        return None

def list_families_api(admin_token):
    """Lista famílias via API"""
    try:
        response = requests.get("http://localhost:5000/admin/families",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if response.status_code == 200:
            families = response.json()
            print(f"📋 {len(families)} famílias encontradas:")
            print("-" * 50)
            for family in families:
                print(f"ID: {family['id']} | Nome: {family['name']}")
            return families
        else:
            print(f"❌ Erro ao listar famílias: {response.json()}")
            return []
    except Exception as e:
        print(f"❌ Erro ao listar famílias via API: {e}")
        return []

def list_families_direct():
    """Lista famílias diretamente do banco de dados"""
    try:
        app = create_app()
        with app.app_context():
            families = Family.query.all()
            print(f"📋 {len(families)} famílias encontradas:")
            print("-" * 50)
            for family in families:
                print(f"ID: {family.id} | Nome: {family.name}")
            return families
    except Exception as e:
        print(f"❌ Erro ao listar famílias: {e}")
        return []

def add_user_to_family_api(family_id, user_email, admin_token):
    """Adiciona usuário à família via API"""
    try:
        # Primeiro, buscar o usuário
        response = requests.get("http://localhost:5000/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if response.status_code != 200:
            print(f"❌ Erro ao buscar usuários: {response.json()}")
            return False
        
        users = response.json()
        user = next((u for u in users if u["email"] == user_email), None)
        
        if not user:
            print(f"❌ Usuário '{user_email}' não encontrado!")
            return False
        
        # Adicionar usuário à família
        response = requests.post(f"http://localhost:5000/admin/families/{family_id}/add_user/{user['id']}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if response.status_code == 200:
            print(f"✅ Usuário '{user_email}' adicionado à família ID {family_id}!")
            return True
        else:
            print(f"❌ Erro ao adicionar usuário: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Erro ao adicionar usuário via API: {e}")
        return False

def add_user_to_family_direct(family_id, user_email):
    """Adiciona usuário à família diretamente no banco"""
    try:
        app = create_app()
        with app.app_context():
            family = Family.query.get(family_id)
            if not family:
                print(f"❌ Família ID {family_id} não encontrada!")
                return False
            
            user = User.query.filter_by(email=user_email).first()
            if not user:
                print(f"❌ Usuário '{user_email}' não encontrado!")
                return False
            
            if family not in user.families:
                user.families.append(family)
                db.session.commit()
                print(f"✅ Usuário '{user_email}' adicionado à família '{family.name}'!")
                return True
            else:
                print(f"⚠️  Usuário '{user_email}' já está na família '{family.name}'!")
                return True
    except Exception as e:
        print(f"❌ Erro ao adicionar usuário: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Script para criar famílias no sistema Family Office")
    parser.add_argument("name", nargs="?", help="Nome da família a ser criada")
    parser.add_argument("--name", help="Nome da família a ser criada")
    parser.add_argument("--list", action="store_true", help="Listar todas as famílias")
    parser.add_argument("--admin-email", default="admin@admin.com", help="Email do usuário admin")
    parser.add_argument("--admin-password", default="admin123", help="Senha do usuário admin")
    parser.add_argument("--add-user", help="Email do usuário para adicionar à família")
    parser.add_argument("--family-id", type=int, help="ID da família para adicionar usuário")
    parser.add_argument("--api", action="store_true", help="Usar API ao invés de acesso direto ao banco")
    
    args = parser.parse_args()
    
    family_name = args.name or args.name
    
    if args.list:
        if args.api:
            admin_token = get_admin_token(args.admin_email, args.admin_password)
            if admin_token:
                list_families_api(admin_token)
            else:
                print("❌ Não foi possível obter token de admin. Listando diretamente do banco...")
                list_families_direct()
        else:
            list_families_direct()
        return
    
    if not family_name:
        print("❌ Erro: Nome da família é obrigatório!")
        print("Uso: python scripts/create_family.py 'Nome da Família'")
        return
    
    if args.add_user:
        if not args.family_id:
            print("❌ Erro: --family-id é obrigatório quando usar --add-user!")
            return
        
        if args.api:
            admin_token = get_admin_token(args.admin_email, args.admin_password)
            if admin_token:
                add_user_to_family_api(args.family_id, args.add_user, admin_token)
            else:
                print("❌ Não foi possível obter token de admin. Adicionando diretamente...")
                add_user_to_family_direct(args.family_id, args.add_user)
        else:
            add_user_to_family_direct(args.family_id, args.add_user)
        return
    
    # Criar família
    if args.api:
        admin_token = get_admin_token(args.admin_email, args.admin_password)
        if admin_token:
            create_family_api(family_name, admin_token)
        else:
            print("❌ Não foi possível obter token de admin. Criando diretamente no banco...")
            create_family_direct(family_name)
    else:
        create_family_direct(family_name)

if __name__ == "__main__":
    main() 