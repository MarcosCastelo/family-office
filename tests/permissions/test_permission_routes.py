import pytest
import json
from app.models.permission import Permission
from app.models.user import User
from app.config.extensions import db
from app.constants.permissions import ALL_PERMISSIONS, PERMISSION_PROFILES

class TestPermissionRoutes:
    """Testes para as rotas de permissões"""
    
    def test_list_permissions_success(self, client, admin_user_fixture):
        """Teste de listagem de permissões com sucesso"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Criar algumas permissões
            perm1 = Permission(name="perm1", description="Permission 1")
            perm2 = Permission(name="perm2", description="Permission 2")
            db.session.add_all([perm1, perm2])
            db.session.commit()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Fazer requisição para listar permissões
            response = client.get('/permissions', headers={
                'Authorization': f'Bearer {token}'
            })
            
            assert response.status_code == 200
            data = response.json
            assert len(data) >= 2  # Pode ter mais permissões do admin_user_fixture
            assert any(p['name'] == 'perm1' for p in data)
            assert any(p['name'] == 'perm2' for p in data)
    
    def test_list_permissions_unauthorized(self, client, user_fixture):
        """Teste de listagem de permissões sem autorização"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Fazer login como usuário normal
            login_response = client.post('/auth/login', json={
                'email': user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Tentar listar permissões
            response = client.get('/permissions', headers={
                'Authorization': f'Bearer {token}'
            })
            
            assert response.status_code == 403
    
    def test_get_permission_success(self, client, admin_user_fixture):
        """Teste de obtenção de permissão específica"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Criar permissão
            permission = Permission(name="test_perm", description="Test permission")
            db.session.add(permission)
            db.session.commit()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Obter permissão específica
            response = client.get(f'/permissions/{permission.id}', headers={
                'Authorization': f'Bearer {token}'
            })
            
            assert response.status_code == 200
            data = response.json
            assert data['name'] == 'test_perm'
            assert data['description'] == 'Test permission'
    
    def test_get_permission_not_found(self, client, admin_user_fixture):
        """Teste de obtenção de permissão inexistente"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Tentar obter permissão inexistente
            response = client.get('/permissions/999', headers={
                'Authorization': f'Bearer {token}'
            })
            
            assert response.status_code == 404
    
    def test_create_permission_success(self, client, admin_user_fixture):
        """Teste de criação de permissão"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Criar permissão
            response = client.post('/permissions', 
                json={'name': 'new_perm', 'description': 'New permission'},
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 201
            data = response.json
            assert data['name'] == 'new_perm'
            assert data['description'] == 'New permission'
    
    def test_create_permission_duplicate_name(self, client, admin_user_fixture):
        """Teste de criação de permissão com nome duplicado"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Criar permissão existente
            existing_perm = Permission(name="existing_perm")
            db.session.add(existing_perm)
            db.session.commit()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Tentar criar permissão com mesmo nome
            response = client.post('/permissions', 
                json={'name': 'existing_perm', 'description': 'Duplicate'},
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 400
            assert "já existe" in response.json['error']
    
    def test_update_permission_success(self, client, admin_user_fixture):
        """Teste de atualização de permissão"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Criar permissão
            permission = Permission(name="old_name", description="Old description")
            db.session.add(permission)
            db.session.commit()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Atualizar permissão
            response = client.put(f'/permissions/{permission.id}', 
                json={'name': 'new_name', 'description': 'New description'},
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            data = response.json
            assert data['name'] == 'new_name'
            assert data['description'] == 'New description'
    
    def test_delete_permission_success(self, client, admin_user_fixture):
        """Teste de exclusão de permissão"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Criar permissão
            permission = Permission(name="to_delete")
            db.session.add(permission)
            db.session.commit()
            permission_id = permission.id
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Deletar permissão
            response = client.delete(f'/permissions/{permission_id}', 
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 204
            
            # Verificar se foi realmente deletada
            deleted_perm = db.session.get(Permission, permission_id)
            assert deleted_perm is None
    
    def test_get_user_permissions_success(self, client, admin_user_fixture, user_fixture):
        """Teste de obtenção de permissões de usuário"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Criar permissões e atribuir ao usuário
            perm1 = Permission(name="user_perm1")
            perm2 = Permission(name="user_perm2")
            db.session.add_all([perm1, perm2])
            db.session.commit()
            
            user = db.session.get(User, user_fixture.id)
            user.permissions.extend([perm1, perm2])
            db.session.commit()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Obter permissões do usuário
            response = client.get(f'/users/{user_fixture.id}/permissions', 
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            data = response.json
            assert len(data) == 2
            assert any(p['name'] == 'user_perm1' for p in data)
            assert any(p['name'] == 'user_perm2' for p in data)
    
    def test_assign_permissions_success(self, client, admin_user_fixture, user_fixture):
        """Teste de atribuição de permissões a usuário"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Criar permissões
            perm1 = Permission(name="assign_perm1")
            perm2 = Permission(name="assign_perm2")
            db.session.add_all([perm1, perm2])
            db.session.commit()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Atribuir permissões
            response = client.post('/users/permissions', 
                json={
                    'user_id': user_fixture.id,
                    'permission_ids': [perm1.id, perm2.id]
                },
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            assert "atribuídas com sucesso" in response.json['message']
            
            # Verificar se as permissões foram atribuídas
            user = db.session.get(User, user_fixture.id)
            user_permissions = user.permissions
            assert len(user_permissions) == 2
            assert any(p.name == 'assign_perm1' for p in user_permissions)
            assert any(p.name == 'assign_perm2' for p in user_permissions)
    
    def test_assign_profile_success(self, client, admin_user_fixture, user_fixture):
        """Teste de atribuição de perfil a usuário"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Criar permissões do perfil manager (apenas as que não existem)
            manager_permissions = PERMISSION_PROFILES['manager']
            for perm_name in manager_permissions:
                existing = Permission.query.filter_by(name=perm_name).first()
                if not existing:
                    perm = Permission(name=perm_name)
                    db.session.add(perm)
            db.session.commit()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Atribuir perfil
            response = client.post('/users/profile', 
                json={
                    'user_id': user_fixture.id,
                    'profile_name': 'manager'
                },
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            assert "Perfil 'manager' atribuído" in response.json['message']
            
            # Verificar se as permissões do perfil foram atribuídas
            user = db.session.get(User, user_fixture.id)
            user_permissions = [p.name for p in user.permissions]
            for perm_name in manager_permissions:
                assert perm_name in user_permissions
    
    def test_list_available_permissions_success(self, client, admin_user_fixture):
        """Teste de listagem de permissões disponíveis"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Listar permissões disponíveis
            response = client.get('/permissions/available', 
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            data = response.json
            assert 'permissions' in data
            assert 'profiles' in data
            assert len(data['permissions']) == len(ALL_PERMISSIONS)
            assert len(data['profiles']) == len(PERMISSION_PROFILES)
    
    def test_initialize_permissions_success(self, client, admin_user_fixture):
        """Teste de inicialização de permissões"""
        with client.application.app_context():
            # Limpar sessão para evitar conflitos
            db.session.rollback()
            
            # Fazer login como admin
            login_response = client.post('/auth/login', json={
                'email': admin_user_fixture.email,
                'password': 'password123'
            })
            token = login_response.json['access_token']
            
            # Inicializar permissões
            response = client.post('/permissions/initialize', 
                headers={'Authorization': f'Bearer {token}'}
            )
            
            assert response.status_code == 200
            data = response.json
            assert "criadas com sucesso" in data['message']
            assert data['total_permissions'] == len(ALL_PERMISSIONS)
            
            # Verificar se as permissões foram criadas
            all_permissions = Permission.query.all()
            assert len(all_permissions) >= len(ALL_PERMISSIONS)  # Pode ter mais do admin_user_fixture 