#!/bin/bash

# Script para limpar alertas do sistema Family Office
# Uso: ./scripts/clear_alerts.sh [opção]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para mostrar ajuda
show_help() {
    echo -e "${BLUE}Script para limpar alertas do sistema Family Office${NC}"
    echo ""
    echo "Uso:"
    echo "  $0 [opção]"
    echo ""
    echo "Opções:"
    echo "  all                    - Limpa todos os alertas"
    echo "  family <id>            - Limpa alertas de uma família específica"
    echo "  alert <id>             - Limpa um alerta específico"
    echo "  type <tipo>            - Limpa alertas de um tipo específico"
    echo "  old <dias>             - Limpa alertas mais antigos que X dias"
    echo "  list                   - Lista todos os alertas"
    echo "  stats                  - Mostra estatísticas dos alertas"
    echo "  help                   - Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 all                 # Limpa todos os alertas"
    echo "  $0 family 1            # Limpa alertas da família ID 1"
    echo "  $0 alert 5             # Limpa alerta ID 5"
    echo "  $0 type concentracao   # Limpa alertas de concentração"
    echo "  $0 old 30              # Limpa alertas mais antigos que 30 dias"
    echo "  $0 list                # Lista todos os alertas"
    echo "  $0 stats               # Mostra estatísticas"
}

# Verificar se estamos no diretório correto
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Erro: Execute este script do diretório raiz do projeto${NC}"
    exit 1
fi

# Verificar se o script Python existe
if [ ! -f "scripts/clear_alerts.py" ]; then
    echo -e "${RED}❌ Erro: Script Python não encontrado em scripts/clear_alerts.py${NC}"
    exit 1
fi

# Tornar o script Python executável
chmod +x scripts/clear_alerts.py

# Função principal
case "$1" in
    "all")
        echo -e "${YELLOW}⚠️  Limpando todos os alertas...${NC}"
        python scripts/clear_alerts.py --all
        ;;
    "family")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Erro: ID da família é obrigatório${NC}"
            echo "Uso: $0 family <id>"
            exit 1
        fi
        echo -e "${YELLOW}🗑️  Limpando alertas da família ID $2...${NC}"
        python scripts/clear_alerts.py --family-id "$2"
        ;;
    "alert")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Erro: ID do alerta é obrigatório${NC}"
            echo "Uso: $0 alert <id>"
            exit 1
        fi
        echo -e "${YELLOW}🗑️  Limpando alerta ID $2...${NC}"
        python scripts/clear_alerts.py --alert-id "$2"
        ;;
    "type")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Erro: Tipo do alerta é obrigatório${NC}"
            echo "Uso: $0 type <tipo>"
            exit 1
        fi
        echo -e "${YELLOW}🗑️  Limpando alertas do tipo '$2'...${NC}"
        python scripts/clear_alerts.py --type "$2"
        ;;
    "old")
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Erro: Número de dias é obrigatório${NC}"
            echo "Uso: $0 old <dias>"
            exit 1
        fi
        echo -e "${YELLOW}🗑️  Limpando alertas mais antigos que $2 dias...${NC}"
        python scripts/clear_alerts.py --older-than "$2"
        ;;
    "list")
        echo -e "${BLUE}📋 Listando todos os alertas...${NC}"
        python scripts/clear_alerts.py --list
        ;;
    "stats")
        echo -e "${BLUE}📊 Mostrando estatísticas...${NC}"
        python scripts/clear_alerts.py --stats
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