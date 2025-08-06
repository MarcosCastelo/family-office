# API - Family Office

## Introdução
Sistema de gestão patrimonial multi-família. Esta API permite autenticação, cadastro de usuários, gestão de famílias, ativos, permissões, uploads, alertas, dashboard e administração.

**URL base:** `/`

### Autenticação
- JWT via endpoints de login/refresh
- Envie o token no header: `Authorization: Bearer <token>`

---

## Sumário de Endpoints

### Autenticação
- `POST /auth/register` — Cadastro de usuário
- `POST /auth/login` — Login
- `POST /auth/refresh` — Refresh do token JWT

### Famílias
- `GET /families` — Listar famílias do usuário
- `POST /families/join/<family_id>` — Solicitar associação a família
- `GET /families/<family_id>/risk/summary` — Resumo de risco consolidado
- `GET /families/<family_id>/alerts` — Listar alertas
- `POST /families/<family_id>/alerts/trigger` — Forçar verificação de alertas
- `POST /families/<family_id>/risk/trigger` — Forçar recálculo de risco

### Ativos
- `GET /assets` — Listar ativos
- `GET /assets/<asset_id>` — Detalhar ativo
- `POST /assets` — Criar ativo
- `PUT /assets/<asset_id>` — Editar ativo
- `DELETE /assets/<asset_id>` — Remover ativo
- `POST /assets/upload` — Upload de ativos (CSV/XLSX)
- `POST /assets/upload-pdf` — Upload de extrato PDF
- `GET /assets/<asset_id>/risk` — Risco individual do ativo

### Permissões
- `GET /permissions` — Listar permissões
- `GET /permissions/<permission_id>` — Detalhar permissão
- `POST /permissions` — Criar permissão
- `PUT /permissions/<permission_id>` — Editar permissão
- `DELETE /permissions/<permission_id>` — Remover permissão
- `GET /users/<user_id>/permissions` — Permissões do usuário
- `POST /users/permissions` — Atribuir permissão a usuário
- `POST /users/profile` — Editar perfil do usuário
- `GET /permissions/available` — Permissões disponíveis
- `POST /permissions/initialize` — Inicializar permissões padrão

### Dashboard
- `GET /dashboard` — Dados agregados do dashboard

### Administração
- `GET /admin/families` — Listar famílias (admin)
- `POST /admin/families` — Criar família (admin)
- `PUT /admin/families/<family_id>` — Editar família (admin)
- `DELETE /admin/families/<family_id>` — Remover família (admin)
- `POST /admin/families/<family_id>/add_user/<user_id>` — Adicionar usuário à família (admin)
- `POST /admin/families/<family_id>/remove_user/<user_id>` — Remover usuário da família (admin)
- `GET /admin/users` — Listar usuários (admin)

---

## Detalhamento dos Endpoints

### POST /auth/register
- **Descrição:** Cria um novo usuário. Requer e-mail válido e senha forte (mínimo 6 caracteres).
- **Parâmetros:**
  - Body (JSON):
    - `email` (string, obrigatório)
    - `password` (string, obrigatório)
- **Exemplo de Request:**
  ```json
  {
    "email": "user1@example.com",
    "password": "senha123"
  }
  ```
- **Exemplo de Response (201):**
  ```json
  {
    "message": "Usuario criado com sucesso"
  }
  ```
- **Códigos de status:**
  - 201: Usuário criado
  - 400: Dados ausentes, e-mail inválido, senha fraca ou usuário já existe
  - 500: Erro interno ao criar usuário
- **Observações:**
  - E-mail deve ser único e válido.
  - Senha deve ter pelo menos 6 caracteres.

---

### POST /auth/login
- **Descrição:** Realiza login e retorna tokens JWT.
- **Parâmetros:**
  - Body (JSON):
    - `email` (string, obrigatório)
    - `password` (string, obrigatório)
- **Exemplo de Request:**
  ```json
  {
    "email": "user2@example.com",
    "password": "senha123"
  }
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "access_token": "<jwt_token>",
    "refresh_token": "<jwt_refresh_token>",
    "user": {
      "id": 1,
      "email": "user2@example.com"
    }
  }
  ```
- **Códigos de status:**
  - 200: Login bem-sucedido
  - 400: Dados ausentes
  - 401: Credenciais inválidas
- **Observações:**
  - Retorna access_token e refresh_token.
  - Usar o access_token no header Authorization para acessar endpoints protegidos.

---

### POST /auth/refresh
- **Descrição:** Gera um novo access_token a partir de um refresh_token válido.
- **Parâmetros:**
  - Header: `Authorization: Bearer <refresh_token>`
- **Exemplo de Request:**
  ```
  (Header) Authorization: Bearer <refresh_token>
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "access_token": "<novo_access_token>"
  }
  ```
- **Códigos de status:**
  - 200: Token renovado
  - 401: Refresh token inválido ou ausente
- **Observações:**
  - Usar apenas com refresh_token válido.

---

### GET /families
- **Descrição:** Lista todas as famílias às quais o usuário autenticado está vinculado.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>`
- **Exemplo de Request:**
  ```
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  [
    {
      "id": 1,
      "name": "Familia Teste"
    }
  ]
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 401: Não autenticado
- **Observações:**
  - Retorna lista (pode ser vazia) das famílias do usuário autenticado.

---

### POST /families/join/<family_id>
- **Descrição:** Associa o usuário autenticado à família informada.
- **Parâmetros:**
  - Path: `family_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>`
- **Exemplo de Request:**
  ```
  POST /families/join/1
  (Header) Authorization: Bearer <access_token>
  Body: {}
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "message": "Usuário associado a família Familia Teste"
  }
  ```
- **Códigos de status:**
  - 200: Associação realizada
  - 404: Família não encontrada
  - 401/403: Não autenticado ou sem permissão
- **Observações:**
  - Se já estiver associado, não duplica a associação.

---

### GET /families/<family_id>/risk/summary
- **Descrição:** Retorna o resumo consolidado de risco da família.
- **Parâmetros:**
  - Path: `family_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>`
- **Exemplo de Request:**
  ```
  GET /families/1/risk/summary
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "score": 0.75,
    "detalhes": {
      "liquidez": 0.8,
      "concentracao": 0.7,
      "outros": 0.9
    }
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Família não encontrada
  - 401/403: Não autenticado ou sem permissão
- **Observações:**
  - O formato pode variar conforme a implementação do controller.

---

### GET /families/<family_id>/alerts
- **Descrição:** Lista todos os alertas ativos da família.
- **Parâmetros:**
  - Path: `family_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>`
- **Exemplo de Request:**
  ```
  GET /families/1/alerts
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  [
    {
      "id": 1,
      "tipo": "concentracao",
      "mensagem": "Concentração excessiva em um ativo"
    }
  ]
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Família não encontrada
  - 401/403: Não autenticado ou sem permissão

---

### POST /families/<family_id>/alerts/trigger
- **Descrição:** Força a verificação e geração de alertas para a família.
- **Parâmetros:**
  - Path: `family_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>`
- **Exemplo de Request:**
  ```
  POST /families/1/alerts/trigger
  (Header) Authorization: Bearer <access_token>
  Body: {}
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "message": "Alertas gerados"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 403: Acesso negado
  - 404: Família não encontrada

---

### POST /families/<family_id>/risk/trigger
- **Descrição:** Força o recálculo do score de risco da família (mock, apenas commit).
- **Parâmetros:**
  - Path: `family_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>`
- **Exemplo de Request:**
  ```
  POST /families/1/risk/trigger
  (Header) Authorization: Bearer <access_token>
  Body: {}
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "message": "Score recalculado (mock)"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 401/403: Não autenticado ou sem permissão

--- 

### GET /assets
- **Descrição:** Lista todos os ativos do usuário/família autenticada.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>`
  - (Opcional) Query: filtros por família, tipo, etc. (ver implementação)
- **Exemplo de Request:**
  ```
  GET /assets
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  [
    {
      "id": 1,
      "name": "Ativo XPTO",
      "asset_type": "renda_fixa",
      "value": 10000.0,
      "family_id": 1,
      "details": {...}
    }
  ]
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 401: Não autenticado

---

### GET /assets/<asset_id>
- **Descrição:** Detalha um ativo específico.
- **Parâmetros:**
  - Path: `asset_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>`
- **Exemplo de Request:**
  ```
  GET /assets/1
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "id": 1,
    "name": "Ativo XPTO",
    "asset_type": "renda_fixa",
    "value": 10000.0,
    "family_id": 1,
    "details": {...}
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Ativo não encontrado
  - 401/403: Não autenticado ou sem permissão

---

### POST /assets
- **Descrição:** Cria um novo ativo.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>`
  - Body (JSON):
    - `name` (string, obrigatório)
    - `asset_type` (string, obrigatório)
    - `value` (float, obrigatório)
    - `family_id` (int, obrigatório)
    - `details` (dict, campos variam conforme tipo)
- **Exemplo de Request:**
  ```json
  {
    "name": "Ativo XPTO",
    "asset_type": "renda_fixa",
    "value": 10000.0,
    "family_id": 1,
    "details": {
      "indexador": "IPCA",
      "vencimento": "2030-01-01",
      "taxa": 6.5
    }
  }
  ```
- **Exemplo de Response (201):**
  ```json
  {
    "id": 1,
    "name": "Ativo XPTO",
    "asset_type": "renda_fixa",
    "value": 10000.0,
    "family_id": 1,
    "details": {...}
  }
  ```
- **Códigos de status:**
  - 201: Criado
  - 400: Dados inválidos
  - 401/403: Não autenticado ou sem permissão

---

### PUT /assets/<asset_id>
- **Descrição:** Edita um ativo existente.
- **Parâmetros:**
  - Path: `asset_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>`
  - Body (JSON): campos a atualizar
- **Exemplo de Request:**
  ```json
  {
    "name": "Ativo Editado",
    "value": 20000.0
  }
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "id": 1,
    "name": "Ativo Editado",
    "asset_type": "renda_fixa",
    "value": 20000.0,
    "family_id": 1,
    "details": {...}
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Ativo não encontrado
  - 401/403: Não autenticado ou sem permissão

---

### DELETE /assets/<asset_id>
- **Descrição:** Remove um ativo.
- **Parâmetros:**
  - Path: `asset_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>`
- **Exemplo de Request:**
  ```
  DELETE /assets/1
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "message": "Ativo removido"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Ativo não encontrado
  - 401/403: Não autenticado ou sem permissão

---

### POST /assets/upload
- **Descrição:** Upload de ativos via arquivo CSV/XLSX.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>`
  - Body: multipart/form-data com campo `file`
- **Exemplo de Request:**  
  (multipart/form-data com arquivo .csv)
- **Exemplo de Response (201):**
  ```json
  {
    "message": "Upload realizado com sucesso",
    "importados": 2,
    "erros": []
  }
  ```
- **Códigos de status:**
  - 201: Sucesso
  - 400: Arquivo inválido
  - 401/403: Não autenticado ou sem permissão

---

### POST /assets/upload-pdf
- **Descrição:** Upload de extrato PDF para processamento automático de ativos.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>`
  - Body: multipart/form-data com campo `file`
- **Exemplo de Request:**  
  (multipart/form-data com arquivo .pdf)
- **Exemplo de Response (201):**
  ```json
  {
    "message": "Upload realizado com sucesso",
    "importados": 5,
    "erros": []
  }
  ```
- **Códigos de status:**
  - 201: Sucesso
  - 400: Arquivo inválido
  - 401/403: Não autenticado ou sem permissão

---

### GET /assets/<asset_id>/risk
- **Descrição:** Retorna o risco individual do ativo.
- **Parâmetros:**
  - Path: `asset_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>`
  - Query: `family_id` (int, obrigatório)
- **Exemplo de Request:**
  ```
  GET /assets/1/risk?family_id=1
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "id": 1,
    "risco_mercado": 0.12,
    "classificacao_final": "baixo"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Ativo não encontrado
  - 401/403: Não autenticado ou sem permissão

--- 

### GET /permissions
- **Descrição:** Lista todas as permissões do sistema.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  GET /permissions
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  [
    {
      "id": 1,
      "name": "perm1",
      "description": "Permission 1"
    },
    {
      "id": 2,
      "name": "perm2",
      "description": "Permission 2"
    }
  ]
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 403: Sem permissão

---

### GET /permissions/<permission_id>
- **Descrição:** Detalha uma permissão específica.
- **Parâmetros:**
  - Path: `permission_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  GET /permissions/1
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "id": 1,
    "name": "test_perm",
    "description": "Test permission"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Permissão não encontrada
  - 403: Sem permissão

---

### POST /permissions
- **Descrição:** Cria uma nova permissão.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>` (admin)
  - Body (JSON):
    - `name` (string, obrigatório)
    - `description` (string, opcional)
- **Exemplo de Request:**
  ```json
  {
    "name": "new_perm",
    "description": "New permission"
  }
  ```
- **Exemplo de Response (201):**
  ```json
  {
    "id": 3,
    "name": "new_perm",
    "description": "New permission"
  }
  ```
- **Códigos de status:**
  - 201: Criado
  - 400: Nome duplicado
  - 403: Sem permissão

---

### PUT /permissions/<permission_id>
- **Descrição:** Edita uma permissão existente.
- **Parâmetros:**
  - Path: `permission_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>` (admin)
  - Body (JSON): campos a atualizar
- **Exemplo de Request:**
  ```json
  {
    "name": "new_name",
    "description": "New description"
  }
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "id": 1,
    "name": "new_name",
    "description": "New description"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Permissão não encontrada
  - 403: Sem permissão

---

### DELETE /permissions/<permission_id>
- **Descrição:** Remove uma permissão.
- **Parâmetros:**
  - Path: `permission_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  DELETE /permissions/1
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (204):**
  ```
  (sem corpo)
  ```
- **Códigos de status:**
  - 204: Removido
  - 404: Permissão não encontrada
  - 403: Sem permissão

---

### GET /users/<user_id>/permissions
- **Descrição:** Lista as permissões de um usuário.
- **Parâmetros:**
  - Path: `user_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  GET /users/2/permissions
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  [
    {"id": 1, "name": "user_perm1"},
    {"id": 2, "name": "user_perm2"}
  ]
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 403: Sem permissão

---

### POST /users/permissions
- **Descrição:** Atribui permissões a um usuário.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>` (admin)
  - Body (JSON):
    - `user_id` (int, obrigatório)
    - `permission_ids` (lista de int, obrigatório)
- **Exemplo de Request:**
  ```json
  {
    "user_id": 2,
    "permission_ids": [1, 2]
  }
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "message": "Permissões atribuídas com sucesso"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 403: Sem permissão

---

### POST /users/profile
- **Descrição:** Atribui um perfil de permissões a um usuário.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>` (admin)
  - Body (JSON):
    - `user_id` (int, obrigatório)
    - `profile_name` (string, obrigatório)
- **Exemplo de Request:**
  ```json
  {
    "user_id": 2,
    "profile_name": "manager"
  }
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "message": "Perfil 'manager' atribuído"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 403: Sem permissão

---

### GET /permissions/available
- **Descrição:** Lista todas as permissões e perfis disponíveis.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  GET /permissions/available
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "permissions": ["perm1", "perm2", ...],
    "profiles": {
      "admin": ["perm1", "perm2"],
      "manager": ["perm3", ...]
    }
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 403: Sem permissão

---

### POST /permissions/initialize
- **Descrição:** Inicializa as permissões padrão do sistema.
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  POST /permissions/initialize
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "message": "Permissões criadas com sucesso",
    "total_permissions": 10
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 403: Sem permissão

--- 

### GET /dashboard
- **Descrição:** Retorna dados agregados do dashboard para o usuário autenticado (ativos, risco, alertas, etc).
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>`
- **Exemplo de Request:**
  ```
  GET /dashboard
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "total_ativos": 10,
    "total_familias": 2,
    "score_risco": 0.75,
    "alertas": [
      {"tipo": "concentracao", "mensagem": "Concentração excessiva em um ativo"}
    ]
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 401: Não autenticado

---

### GET /admin/families
- **Descrição:** Lista todas as famílias cadastradas (admin).
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  GET /admin/families
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  [
    {"id": 1, "name": "Familia 1"},
    {"id": 2, "name": "Familia 2"}
  ]
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 403: Sem permissão

---

### POST /admin/families
- **Descrição:** Cria uma nova família (admin).
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>` (admin)
  - Body (JSON):
    - `name` (string, obrigatório)
- **Exemplo de Request:**
  ```json
  {
    "name": "Nova Família"
  }
  ```
- **Exemplo de Response (201):**
  ```json
  {
    "id": 3,
    "name": "Nova Família"
  }
  ```
- **Códigos de status:**
  - 201: Criado
  - 400: Nome duplicado
  - 403: Sem permissão

---

### PUT /admin/families/<family_id>
- **Descrição:** Edita uma família existente (admin).
- **Parâmetros:**
  - Path: `family_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>` (admin)
  - Body (JSON): campos a atualizar
- **Exemplo de Request:**
  ```json
  {
    "name": "Família Editada"
  }
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "id": 1,
    "name": "Família Editada"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Família não encontrada
  - 403: Sem permissão

---

### DELETE /admin/families/<family_id>
- **Descrição:** Remove uma família (admin).
- **Parâmetros:**
  - Path: `family_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  DELETE /admin/families/1
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (204):**
  ```
  (sem corpo)
  ```
- **Códigos de status:**
  - 204: Removido
  - 404: Família não encontrada
  - 403: Sem permissão

---

### POST /admin/families/<family_id>/add_user/<user_id>
- **Descrição:** Adiciona um usuário a uma família (admin).
- **Parâmetros:**
  - Path: `family_id` (int, obrigatório), `user_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  POST /admin/families/1/add_user/2
  (Header) Authorization: Bearer <access_token>
  Body: {}
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "message": "Usuário adicionado à família"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Família ou usuário não encontrado
  - 403: Sem permissão

---

### POST /admin/families/<family_id>/remove_user/<user_id>
- **Descrição:** Remove um usuário de uma família (admin).
- **Parâmetros:**
  - Path: `family_id` (int, obrigatório), `user_id` (int, obrigatório)
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  POST /admin/families/1/remove_user/2
  (Header) Authorization: Bearer <access_token>
  Body: {}
  ```
- **Exemplo de Response (200):**
  ```json
  {
    "message": "Usuário removido da família"
  }
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 404: Família ou usuário não encontrado
  - 403: Sem permissão

---

### GET /admin/users
- **Descrição:** Lista todos os usuários cadastrados (admin).
- **Parâmetros:**
  - Header: `Authorization: Bearer <access_token>` (admin)
- **Exemplo de Request:**
  ```
  GET /admin/users
  (Header) Authorization: Bearer <access_token>
  ```
- **Exemplo de Response (200):**
  ```json
  [
    {"id": 1, "email": "admin@example.com"},
    {"id": 2, "email": "user@example.com"}
  ]
  ```
- **Códigos de status:**
  - 200: Sucesso
  - 403: Sem permissão

--- image.png