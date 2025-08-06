# 🧹 Scripts de Gerenciamento do Sistema

Este diretório contém scripts para gerenciar e administrar o sistema Family Office.

## 📁 Arquivos

### Limpeza de Alertas
- `clear_alerts.py` - Script Python principal para limpeza de alertas
- `clear_alerts.sh` - Script bash wrapper para facilitar o uso

### Criação de Famílias
- `create_family.py` - Script Python para criar e gerenciar famílias
- `create_family.sh` - Script bash wrapper para facilitar o uso

- `README.md` - Esta documentação

## 🚀 Uso Rápido

### Scripts de Limpeza de Alertas

#### Script Bash (Recomendado)
```bash
# Listar todos os alertas
./scripts/clear_alerts.sh list

# Mostrar estatísticas
./scripts/clear_alerts.sh stats

# Limpar todos os alertas (com confirmação)
./scripts/clear_alerts.sh all

# Limpar alertas de uma família específica
./scripts/clear_alerts.sh family 1

# Limpar um alerta específico
./scripts/clear_alerts.sh alert 5

# Limpar alertas de um tipo específico
./scripts/clear_alerts.sh type concentracao

# Limpar alertas mais antigos que 30 dias
./scripts/clear_alerts.sh old 30
```

#### Script Python Direto
```bash
# Listar alertas
poetry run python scripts/clear_alerts.py --list

# Mostrar estatísticas
poetry run python scripts/clear_alerts.py --stats

# Limpar todos os alertas
poetry run python scripts/clear_alerts.py --all

# Limpar alertas de uma família
poetry run python scripts/clear_alerts.py --family-id 1

# Limpar alerta específico
poetry run python scripts/clear_alerts.py --alert-id 5

# Limpar por tipo
poetry run python scripts/clear_alerts.py --type concentracao

# Limpar alertas antigos
poetry run python scripts/clear_alerts.py --older-than 30
```

### Scripts de Criação de Famílias

#### Script Bash (Recomendado)
```bash
# Criar uma nova família
./scripts/create_family.sh create 'Família Silva'

# Listar todas as famílias
./scripts/create_family.sh list

# Adicionar usuário à família
./scripts/create_family.sh add-user 1 user@example.com
```

#### Script Python Direto
```bash
# Criar uma nova família
poetry run python scripts/create_family.py 'Família Silva'

# Listar todas as famílias
poetry run python scripts/create_family.py --list

# Adicionar usuário à família
poetry run python scripts/create_family.py --family-id 1 --add-user user@example.com

# Usar API (requer servidor rodando)
poetry run python scripts/create_family.py 'Família API' --api
```

## 📋 Funcionalidades

### 🔍 Visualização
- **Listar Alertas**: Mostra todos os alertas com detalhes
- **Estatísticas**: Conta alertas por tipo, severidade e família
- **Listar Famílias**: Mostra todas as famílias cadastradas

### 🗑️ Limpeza Seletiva
- **Por Família**: Remove alertas de uma família específica
- **Por Tipo**: Remove alertas de um tipo específico (ex: concentracao, liquidez)
- **Por ID**: Remove um alerta específico
- **Por Idade**: Remove alertas mais antigos que X dias

### ⚠️ Limpeza Total
- **Todos os Alertas**: Remove todos os alertas do sistema (com confirmação)

### 🏠 Gerenciamento de Famílias
- **Criar Família**: Cria nova família no sistema
- **Listar Famílias**: Mostra todas as famílias cadastradas
- **Adicionar Usuário**: Adiciona usuário existente à família

## 🛡️ Segurança

- **Confirmação**: Limpeza total requer confirmação manual
- **Rollback**: Operações são revertidas em caso de erro
- **Validação**: Verifica existência de famílias e alertas antes de deletar
- **Logs**: Mostra feedback detalhado de todas as operações
- **Duplicação**: Evita criar famílias com nomes duplicados

## 📊 Tipos de Alerta

O sistema gera automaticamente os seguintes tipos de alerta:

- **concentracao**: Ativo representa mais de 30% da carteira
- **liquidez**: Mais de 50% da carteira em ativos ilíquidos
- **risco**: Alertas gerais de risco (exemplo do seed)

## 🔧 Endpoints da API

Além dos scripts, você pode usar os endpoints da API:

### Alertas
```bash
# Listar alertas de uma família
curl -X GET "http://localhost:5000/families/1/alerts" \
  -H "Authorization: Bearer <token>"

# Deletar todos os alertas de uma família
curl -X DELETE "http://localhost:5000/families/1/alerts" \
  -H "Authorization: Bearer <token>"

# Deletar alerta específico
curl -X DELETE "http://localhost:5000/families/1/alerts/5" \
  -H "Authorization: Bearer <token>"
```

### Famílias
```bash
# Criar família (admin)
curl -X POST "http://localhost:5000/admin/families" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Nova Família"}'

# Listar famílias (admin)
curl -X GET "http://localhost:5000/admin/families" \
  -H "Authorization: Bearer <admin_token>"

# Adicionar usuário à família (admin)
curl -X POST "http://localhost:5000/admin/families/1/add_user/2" \
  -H "Authorization: Bearer <admin_token>"
```

## 🚨 Exemplos de Uso

### Limpeza de Manutenção
```bash
# Verificar alertas existentes
./scripts/clear_alerts.sh stats

# Limpar alertas antigos (mais de 7 dias)
./scripts/clear_alerts.sh old 7

# Limpar alertas de concentração (já resolvidos)
./scripts/clear_alerts.sh type concentracao
```

### Limpeza de Desenvolvimento
```bash
# Limpar todos os alertas para testes
./scripts/clear_alerts.sh all

# Verificar se foram removidos
./scripts/clear_alerts.sh list
```

### Limpeza Específica
```bash
# Limpar alertas de uma família específica
./scripts/clear_alerts.sh family 2

# Limpar um alerta problemático
./scripts/clear_alerts.sh alert 15
```

### Gerenciamento de Famílias
```bash
# Criar nova família
./scripts/create_family.sh create 'Família Santos'

# Listar famílias existentes
./scripts/create_family.sh list

# Adicionar usuário à família
./scripts/create_family.sh add-user 1 user@example.com
```

## 📝 Logs e Feedback

Os scripts fornecem feedback detalhado:

- ✅ Sucesso: Operação realizada com sucesso
- ❌ Erro: Problema durante a operação
- ⚠️ Confirmação: Requer confirmação para operações críticas
- 📊 Estatísticas: Contadores e resumos
- 📋 Listagem: Detalhes completos dos alertas e famílias

## 🔄 Integração

Os scripts se integram com:

- **Flask App**: Usa o contexto da aplicação
- **SQLAlchemy**: Acesso direto ao banco de dados
- **JWT**: Verificação de permissões (via API)
- **Migrations**: Compatível com estrutura de migrações
- **Poetry**: Gerenciamento de dependências

## 🛠️ Desenvolvimento

Para modificar os scripts:

1. **Adicionar nova funcionalidade**: Edite os scripts Python
2. **Adicionar nova opção**: Atualize os scripts bash
3. **Testar**: Execute com dados de teste
4. **Documentar**: Atualize este README

## 📞 Suporte

Em caso de problemas:

1. Verifique se está no diretório raiz do projeto
2. Confirme que o ambiente virtual está ativo (`poetry shell`)
3. Teste com `./scripts/clear_alerts.sh help` ou `./scripts/create_family.sh help`
4. Verifique os logs de erro detalhados
5. Certifique-se de que o servidor Flask está rodando para operações via API 