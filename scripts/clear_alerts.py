#!/usr/bin/env python3
"""
Script para limpar alertas do sistema Family Office

Uso:
    python scripts/clear_alerts.py --all                    # Limpa todos os alertas
    python scripts/clear_alerts.py --family-id 1           # Limpa alertas de uma família específica
    python scripts/clear_alerts.py --alert-id 5            # Limpa um alerta específico
    python scripts/clear_alerts.py --type concentracao     # Limpa alertas de um tipo específico
    python scripts/clear_alerts.py --older-than 30         # Limpa alertas mais antigos que 30 dias
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
from sqlalchemy import and_

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.alert import Alert
from app.models.family import Family
from app.config.extensions import db

def clear_all_alerts():
    """Limpa todos os alertas do sistema"""
    try:
        count = Alert.query.delete()
        db.session.commit()
        print(f"✅ {count} alertas deletados com sucesso!")
        return count
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao deletar alertas: {e}")
        return 0

def clear_family_alerts(family_id):
    """Limpa alertas de uma família específica"""
    try:
        # Verificar se a família existe
        family = Family.query.get(family_id)
        if not family:
            print(f"❌ Família com ID {family_id} não encontrada!")
            return 0
        
        count = Alert.query.filter_by(family_id=family_id).delete()
        db.session.commit()
        print(f"✅ {count} alertas da família '{family.name}' deletados com sucesso!")
        return count
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao deletar alertas da família {family_id}: {e}")
        return 0

def clear_specific_alert(alert_id):
    """Limpa um alerta específico"""
    try:
        alert = Alert.query.get(alert_id)
        if not alert:
            print(f"❌ Alerta com ID {alert_id} não encontrado!")
            return 0
        
        db.session.delete(alert)
        db.session.commit()
        print(f"✅ Alerta '{alert.mensagem}' (ID: {alert_id}) deletado com sucesso!")
        return 1
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao deletar alerta {alert_id}: {e}")
        return 0

def clear_alerts_by_type(alert_type):
    """Limpa alertas de um tipo específico"""
    try:
        count = Alert.query.filter_by(tipo=alert_type).delete()
        db.session.commit()
        print(f"✅ {count} alertas do tipo '{alert_type}' deletados com sucesso!")
        return count
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao deletar alertas do tipo {alert_type}: {e}")
        return 0

def clear_old_alerts(days):
    """Limpa alertas mais antigos que X dias"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        count = Alert.query.filter(Alert.criado_em < cutoff_date).delete()
        db.session.commit()
        print(f"✅ {count} alertas mais antigos que {days} dias deletados com sucesso!")
        return count
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao deletar alertas antigos: {e}")
        return 0

def list_alerts():
    """Lista todos os alertas existentes"""
    try:
        alerts = Alert.query.all()
        if not alerts:
            print("📭 Nenhum alerta encontrado no sistema.")
            return
        
        print(f"📋 {len(alerts)} alertas encontrados:")
        print("-" * 80)
        
        for alert in alerts:
            family = Family.query.get(alert.family_id)
            family_name = family.name if family else "Família não encontrada"
            
            print(f"ID: {alert.id}")
            print(f"Família: {family_name} (ID: {alert.family_id})")
            print(f"Tipo: {alert.tipo}")
            print(f"Severidade: {alert.severidade}")
            print(f"Mensagem: {alert.mensagem}")
            print(f"Criado em: {alert.criado_em}")
            print("-" * 80)
    
    except Exception as e:
        print(f"❌ Erro ao listar alertas: {e}")

def get_stats():
    """Mostra estatísticas dos alertas"""
    try:
        total_alerts = Alert.query.count()
        
        # Alertas por tipo
        tipos = db.session.query(Alert.tipo, db.func.count(Alert.id)).group_by(Alert.tipo).all()
        
        # Alertas por severidade
        severidades = db.session.query(Alert.severidade, db.func.count(Alert.id)).group_by(Alert.severidade).all()
        
        # Alertas por família
        familias = db.session.query(Alert.family_id, db.func.count(Alert.id)).group_by(Alert.family_id).all()
        
        print("📊 Estatísticas dos Alertas:")
        print("-" * 40)
        print(f"Total de alertas: {total_alerts}")
        print()
        
        print("Por tipo:")
        for tipo, count in tipos:
            print(f"  {tipo}: {count}")
        print()
        
        print("Por severidade:")
        for severidade, count in severidades:
            print(f"  {severidade}: {count}")
        print()
        
        print("Por família:")
        for family_id, count in familias:
            family = Family.query.get(family_id)
            family_name = family.name if family else "Família não encontrada"
            print(f"  {family_name} (ID: {family_id}): {count}")
    
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")

def main():
    parser = argparse.ArgumentParser(description="Script para limpar alertas do sistema Family Office")
    parser.add_argument("--all", action="store_true", help="Limpa todos os alertas")
    parser.add_argument("--family-id", type=int, help="Limpa alertas de uma família específica")
    parser.add_argument("--alert-id", type=int, help="Limpa um alerta específico")
    parser.add_argument("--type", type=str, help="Limpa alertas de um tipo específico")
    parser.add_argument("--older-than", type=int, help="Limpa alertas mais antigos que X dias")
    parser.add_argument("--list", action="store_true", help="Lista todos os alertas")
    parser.add_argument("--stats", action="store_true", help="Mostra estatísticas dos alertas")
    
    args = parser.parse_args()
    
    # Criar aplicação Flask
    app = create_app()
    
    with app.app_context():
        if args.list:
            list_alerts()
        elif args.stats:
            get_stats()
        elif args.all:
            if input("⚠️  Tem certeza que deseja deletar TODOS os alertas? (y/N): ").lower() == 'y':
                clear_all_alerts()
            else:
                print("❌ Operação cancelada.")
        elif args.family_id:
            clear_family_alerts(args.family_id)
        elif args.alert_id:
            clear_specific_alert(args.alert_id)
        elif args.type:
            clear_alerts_by_type(args.type)
        elif args.older_than:
            clear_old_alerts(args.older_than)
        else:
            print("📋 Alertas no sistema:")
            list_alerts()
            print()
            print("📊 Estatísticas:")
            get_stats()
            print()
            print("💡 Use --help para ver as opções disponíveis.")

if __name__ == "__main__":
    main() 