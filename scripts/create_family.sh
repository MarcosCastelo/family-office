#!/bin/bash

# Script para criar famílias no sistema Family Office
# Uso: ./scripts/create_family.sh [opção]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para mostrar ajuda
show_help() {
    echo -e "${BLUE}Script para criar famílias no sistema Family Office${NC}"
    echo ""
    echo "Uso:"
    echo "  $0 [opção]"
    echo ""
    echo "Opções:"
    echo "  create <nome>              - Criar uma nova família"
    echo "  list                       - Listar todas as famílias"
    echo "  add-user <family_id> <email> - Adicionar usuário à família"
    echo "  help                       - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 create 'Família Silva'        # Criar família 'Família Silva'"
    echo "  $0 list                           # Listar todas as famílias"
    echo "  $0 add-user 1 user@example.com   # Adicionar usuário à família ID 1"
    echo ""
    echo "Opções avançadas:"
    echo "  --api                        # Usar API ao invés de acesso direto"
    echo "  --admin-email <email>        # Email do admin (padrão: admin@admin.com)"
    echo "  --admin-password <senha>     # Senha do admin (padrão: admin123)"
}

# Verificar se estamos no diretório correto
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Erro: Execute este script do diretório raiz do projeto${NC}"
    exit 1
fi

# Verificar se o script Python existe
if [ ! -f "scripts/create_family.py" ]; then
    echo -e "${RED}❌ Erro: Script Python não encontrado em scripts/create_family.py${NC}"
    exit 1
fi

# Tornar o script Python executável
chmod +x scripts/create_family.py

# Função principal
case "$1" in
    "create")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Erro: Nome da família é obrigatório${NC}"
            echo "Uso: $0 create 'Nome da Família'"
            exit 1
        fi
        echo -e "${YELLOW}🏠 Criando família '$2'...${NC}"
        python scripts/create_family.py "$2"
        ;;
    "list")
        echo -e "${BLUE}📋 Listando famílias...${NC}"
        python scripts/create_family.py --list
        ;;
    "add-user")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}❌ Erro: ID da família e email do usuário são obrigatórios${NC}"
            echo "Uso: $0 add-user <family_id> <email>"
            exit 1
        fi
        echo -e "${YELLOW}👤 Adicionando usuário '$3' à família ID $2...${NC}"
        python scripts/create_family.py --family-id "$2" --add-user "$3"
        ;;
    "help"|"-h"|"--help"|"")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Opção inválida: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo -e "${GREEN}✅ Script executado com sucesso!${NC}" 