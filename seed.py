import os
from app import create_app
from app.config.extensions import db
from app.models.user import User
from app.models.family import Family
from app.models.permission import Permission
from app.models.asset import Asset
from app.models.alert import Alert
from app.models.suitability import SuitabilityProfile
from app.models.transaction import Transaction
from app.models.quote_history import QuoteHistory
from app.constants.permissions import ALL_PERMISSIONS, PERMISSION_PROFILES
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from datetime import datetime

# Utilitário para idempotência

def get_or_create(model, defaults=None, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    params = dict((k, v) for k, v in kwargs.items())
    if defaults:
        params.update(defaults)
    # Garante password_hash para User
    if model.__name__ == "User" and "password_hash" not in params:
        params["password_hash"] = generate_password_hash("senha123")
    instance = model(**params)
    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        instance = model.query.filter_by(**kwargs).first()
        return instance, False
    return instance, True

def seed_permissions():
    """Cria todas as permissões do sistema"""
    created = 0
    for perm in ALL_PERMISSIONS:
        _, was_created = get_or_create(Permission, name=perm)
        if was_created:
            created += 1
    
    print(f"🔐 Permissões do sistema:")
    print(f"   ✅ {created} novas permissões criadas")
    print(f"   🔄 {len(ALL_PERMISSIONS)-created} permissões já existiam")
    print(f"   📊 Total: {len(ALL_PERMISSIONS)} permissões disponíveis")
    
    # Mostrar algumas permissões importantes
    important_perms = ["ASSET_CREATE", "ASSET_READ", "RISK_ANALYSIS", "REPORT_GENERATE", "ADMIN_ACCESS"]
    print(f"   🎯 Permissões principais: {', '.join(important_perms)}")

def seed_admin():
    """Cria usuário administrador com todas as permissões"""
    admin_email = "admin@seed.com"
    admin_password = "admin123"
    
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            password_hash=generate_password_hash(admin_password), 
            active=True
        )
        db.session.add(admin)
        db.session.commit()
        created = True
    else:
        created = False
    
    # Atualiza senha se necessário
    if not admin.check_password(admin_password):
        admin.password_hash = generate_password_hash(admin_password)
        admin.active = True
        db.session.commit()
    
    # Garantir todas permissões
    all_perms = Permission.query.all()
    admin.permissions = all_perms
    db.session.commit()
    
    print(f"👑 Usuário admin: {admin.email} (senha: {admin_password})")
    print(f"   Permissões: {len(all_perms)} total")
    
    return admin

def seed_families_and_users():
    """Cria famílias e usuários com perfis diferentes para demonstrar funcionalidades"""
    families = []
    users = []
    
    # Criar famílias com diferentes perfis
    family_profiles = [
        {"name": "Família Conservadora", "cash_balance": 100000.0, "profile": "conservador"},
        {"name": "Família Moderada", "cash_balance": 75000.0, "profile": "moderado"},
        {"name": "Família Agressiva", "cash_balance": 50000.0, "profile": "agressivo"}
    ]
    
    for profile in family_profiles:
        fam, _ = get_or_create(
            Family, 
            name=profile["name"], 
            defaults={"cash_balance": profile["cash_balance"]}
        )
        families.append(fam)
    
    # Usuários com diferentes perfis e permissões
    user_profiles = [
        {"email": "user1@seed.com", "profile": "conservador"},
        {"email": "user2@seed.com", "profile": "moderado"},
        {"email": "user3@seed.com", "profile": "agressivo"}
    ]
    
    for i, profile in enumerate(user_profiles):
        user, created = get_or_create(
            User, 
            email=profile["email"]
        )
        
        if created or not user.check_password("senha123"):
            user.password_hash = generate_password_hash("senha123")
            user.active = True
            db.session.commit()
        
        # Associa a uma família correspondente
        fam = families[i % len(families)]
        if fam not in user.families:
            user.families.append(fam)
            db.session.commit()
        
        users.append(user)
    
    print(f"👨‍👩‍👧‍👦 Famílias e usuários criados:")
    for i, fam in enumerate(families):
        print(f"   🏠 {fam.name} (Saldo: R$ {fam.cash_balance:,.2f})")
        print(f"      👤 {user_profiles[i]['email']}")
    
    return families, users

def seed_assets(families):
    asset_data = [
        {
            "name": "Tesouro Selic", 
            "asset_type": "renda_fixa", 
            "acquisition_date": "2024-01-01", 
            "details": {"indexador": "SELIC", "vencimento": "2025-12-31"}
        },
        {
            "name": "PETR4", 
            "asset_type": "renda_variavel", 
            "acquisition_date": "2023-12-01", 
            "details": {"ticker": "PETR4.SA"}
        },
        {
            "name": "FII XPML11", 
            "asset_type": "fundo_imobiliario", 
            "acquisition_date": "2022-06-15", 
            "details": {"ticker": "XPML11.SA"}
        },
        {
            "name": "Bitcoin", 
            "asset_type": "criptomoeda", 
            "acquisition_date": "2024-03-01", 
            "details": {"coin_id": "bitcoin"}
        },
        {
            "name": "Dólar Americano", 
            "asset_type": "moeda_estrangeira", 
            "acquisition_date": "2024-01-15", 
            "details": {"currency": "USD"}
        }
    ]
    
    for fam in families:
        for data in asset_data:
            acq_date = datetime.strptime(data["acquisition_date"], "%Y-%m-%d").date()
            asset, _ = get_or_create(
                Asset,
                name=data["name"],
                family_id=fam.id,
                defaults={
                    "asset_type": data["asset_type"],
                    "acquisition_date": acq_date,
                    "details": data["details"]
                }
            )
    print(f"Ativos criados para cada família.")

def seed_alerts(families):
    """Cria alertas de exemplo para demonstrar o sistema de monitoramento"""
    for fam in families:
        # Alerta de risco
        risk_alert, _ = get_or_create(
            Alert,
            family_id=fam.id,
            tipo="risco",
            mensagem="Portfólio com exposição acima do recomendado para o perfil de risco",
            severidade="warning"
        )
        
        # Alerta de oportunidade
        opp_alert, _ = get_or_create(
            Alert,
            family_id=fam.id,
            tipo="oportunidade",
            mensagem="Novas opções de investimento disponíveis com melhor rentabilidade",
            severidade="info"
        )
        
        # Alerta de vencimento
        maturity_alert, _ = get_or_create(
            Alert,
            family_id=fam.id,
            tipo="vencimento",
            mensagem="Tesouro Selic vence em 30 dias - considere reinvestir",
            severidade="info"
        )
        
        # Alerta de performance
        perf_alert, _ = get_or_create(
            Alert,
            family_id=fam.id,
            tipo="performance",
            mensagem="Portfólio com performance acima da média do mercado",
            severidade="success"
        )
    
    print(f"Alertas de exemplo criados para cada família.")

def seed_suitability_profiles(families):
    """Cria perfis de suitability para cada família"""
    for fam in families:
        # Buscar um usuário da família para associar o perfil
        user = fam.users[0] if fam.users else None
        if not user:
            continue
            
        # Perfil conservador
        conservative, _ = get_or_create(
            SuitabilityProfile,
            user_id=user.id,
            family_id=fam.id,
            defaults={
                "risk_tolerance": "conservative",
                "investment_horizon": "short_term",
                "liquidity_needs": "low",
                "investment_experience": "intermediate",
                "primary_goal": "capital_preservation",
                "preferred_asset_classes": ["renda_fixa", "tesouro_direto"],
                "overall_risk_score": 25
            }
        )
        
        # Perfil moderado
        moderate, _ = get_or_create(
            SuitabilityProfile,
            user_id=user.id,
            family_id=fam.id,
            defaults={
                "risk_tolerance": "moderate",
                "investment_horizon": "medium_term",
                "liquidity_needs": "medium",
                "investment_experience": "intermediate",
                "primary_goal": "growth",
                "preferred_asset_classes": ["renda_fixa", "renda_variavel", "fundo_imobiliario"],
                "overall_risk_score": 50
            }
        )
        
        # Perfil agressivo
        aggressive, _ = get_or_create(
            SuitabilityProfile,
            user_id=user.id,
            family_id=fam.id,
            defaults={
                "risk_tolerance": "aggressive",
                "investment_horizon": "long_term",
                "liquidity_needs": "high",
                "investment_experience": "advanced",
                "primary_goal": "growth",
                "preferred_asset_classes": ["renda_variavel", "criptomoeda", "fundo_imobiliario"],
                "overall_risk_score": 75
            }
        )
    
    print(f"Perfis de suitability criados para cada família.")

def seed_transactions(families):
    """Cria transações de exemplo para demonstrar cálculo de valores"""
    for fam in families:
        # Buscar ativos da família
        assets = Asset.query.filter_by(family_id=fam.id).all()
        
        for asset in assets:
            if asset.asset_type == "renda_fixa":
                # Compra de renda fixa
                transaction, _ = get_or_create(
                    Transaction,
                    asset_id=asset.id,
                    transaction_type="buy",
                    defaults={
                        "quantity": 1000.0,
                        "unit_price": 1.0,
                        "transaction_date": datetime.strptime("2024-01-01", "%Y-%m-%d").date(),
                        "description": "Compra inicial"
                    }
                )
            
            elif asset.asset_type == "renda_variavel":
                # Compra de ações
                transaction, _ = get_or_create(
                    Transaction,
                    asset_id=asset.id,
                    transaction_type="buy",
                    defaults={
                        "quantity": 100.0,
                        "unit_price": 25.0,
                        "transaction_date": datetime.strptime("2023-12-01", "%Y-%m-%d").date(),
                        "description": "Compra inicial de ações"
                    }
                )
            
            elif asset.asset_type == "fundo_imobiliario":
                # Compra de FII
                transaction, _ = get_or_create(
                    Transaction,
                    asset_id=asset.id,
                    transaction_type="buy",
                    defaults={
                        "quantity": 200.0,
                        "unit_price": 100.0,
                        "transaction_date": datetime.strptime("2022-06-15", "%Y-%m-%d").date(),
                        "description": "Compra inicial de FII"
                    }
                )
            
            elif asset.asset_type == "criptomoeda":
                # Compra de cripto
                transaction, _ = get_or_create(
                    Transaction,
                    asset_id=asset.id,
                    transaction_type="buy",
                    defaults={
                        "quantity": 0.1,
                        "unit_price": 50000.0,
                        "transaction_date": datetime.strptime("2024-03-01", "%Y-%m-%d").date(),
                        "description": "Compra inicial de Bitcoin"
                    }
                )
            
            elif asset.asset_type == "moeda_estrangeira":
                # Compra de moeda estrangeira
                transaction, _ = get_or_create(
                    Transaction,
                    asset_id=asset.id,
                    transaction_type="buy",
                    defaults={
                        "quantity": 1000.0,
                        "unit_price": 5.0,
                        "transaction_date": datetime.strptime("2024-01-15", "%Y-%m-%d").date(),
                        "description": "Compra inicial de USD"
                    }
                )
    
    print(f"Transações de exemplo criadas para demonstrar cálculo de valores.")

def seed_quotes(families):
    """Cria cotações de exemplo para demonstrar análise de risco"""
    for fam in families:
        assets = Asset.query.filter_by(family_id=fam.id).all()
        
        for asset in assets:
            if asset.asset_type == "renda_variavel":
                # Cotação para ações
                quote, _ = get_or_create(
                    QuoteHistory,
                    asset_id=asset.id,
                    defaults={
                        "price": 28.50,
                        "currency": "BRL",
                        "source": "yahoo_finance"
                    }
                )
            
            elif asset.asset_type == "fundo_imobiliario":
                # Cotação para FII
                quote, _ = get_or_create(
                    QuoteHistory,
                    asset_id=asset.id,
                    defaults={
                        "price": 105.00,
                        "currency": "BRL",
                        "source": "yahoo_finance"
                    }
                )
            
            elif asset.asset_type == "criptomoeda":
                # Cotação para cripto
                quote, _ = get_or_create(
                    QuoteHistory,
                    asset_id=asset.id,
                    defaults={
                        "price": 52000.00,
                        "currency": "USD",
                        "source": "coingecko"
                    }
                )
    
    print(f"Cotações de exemplo criadas para análise de risco.")









def main():
    app = create_app()
    with app.app_context():
        print("🔧 Criando estrutura do banco de dados...")
        db.create_all()
        
        print("\n🔐 Configurando sistema de permissões...")
        seed_permissions()
        
        print("\n👑 Criando usuário administrador...")
        admin = seed_admin()
        
        print("\n👨‍👩‍👧‍👦 Criando famílias e usuários...")
        families, users = seed_families_and_users()
        
        print("\n💰 Criando ativos de exemplo...")
        seed_assets(families)
        
        print("\n📈 Criando transações de exemplo...")
        seed_transactions(families)  # Criar transações antes dos alertas
        
        print("\n📊 Criando cotações de exemplo...")
        seed_quotes(families)  # Criar cotações para análise de risco
        
        print("\n⚠️  Criando alertas do sistema...")
        seed_alerts(families)
        
        print("\n📋 Criando perfis de suitability...")
        seed_suitability_profiles(families)
        
        print("\n🎉 Seed concluído com sucesso!")
        print("=" * 50)
        print("📊 RESUMO DO QUE FOI CRIADO:")
        print(f"   👑 1 usuário administrador")
        print(f"   👨‍👩‍👧‍👦 {len(families)} famílias com perfis diferentes")
        print(f"   👤 {len(users)} usuários comuns")
        print(f"   💰 5 tipos de ativos por família (renda fixa, variável, FII, cripto, moeda)")
        print(f"   📈 Transações de exemplo para cálculo de valores")
        print(f"   📊 Cotações para análise de risco")
        print(f"   ⚠️  Alertas do sistema")
        print(f"   📋 Perfis de suitability personalizados")
        print("=" * 50)
        print("🔑 CREDENCIAIS DE ACESSO:")
        print("   👑 Admin: admin@seed.com / admin123")
        print("   👤 User1: user1@seed.com / senha123")
        print("   👤 User2: user2@seed.com / senha123")
        print("   👤 User3: user3@seed.com / senha123")
        print("=" * 50)

if __name__ == "__main__":
    print("🚀 Iniciando seed do sistema Family Office...")
    print("=" * 50)
    main()
    print("\n✨ Sistema pronto para uso!") 