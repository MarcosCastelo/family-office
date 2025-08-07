import os
from app import create_app
from app.config.extensions import db
from app.models.user import User
from app.models.family import Family
from app.models.permission import Permission
from app.models.asset import Asset
from app.models.alert import Alert
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
    created = 0
    for perm in ALL_PERMISSIONS:
        _, was_created = get_or_create(Permission, name=perm)
        if was_created:
            created += 1
    print(f"Permissões seed: {created} criadas, {len(ALL_PERMISSIONS)-created} já existiam.")

def seed_admin():
    admin_email = "admin@seed.com"
    admin_password = "admin123"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(email=admin_email, password_hash=generate_password_hash(admin_password), active=True)
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
    print(f"Usuário admin: {admin.email} (senha: {admin_password})")
    return admin

def seed_families_and_users():
    families = []
    users = []
    for i in range(1, 4):
        fam, _ = get_or_create(Family, name=f"Família Exemplo {i}", defaults={"cash_balance": 50000.0})
        families.append(fam)
    # Usuários comuns
    for i in range(1, 4):
        email = f"user{i}@seed.com"
        user, created = get_or_create(User, email=email)
        if created or not user.check_password("senha123"):
            user.password_hash = generate_password_hash("senha123")
            user.active = True
            db.session.commit()
        # Associa a uma família
        fam = families[i % len(families)]
        if fam not in user.families:
            user.families.append(fam)
            db.session.commit()
        users.append(user)
    print(f"Famílias e usuários comuns criados/atualizados.")
    return families, users

def seed_assets(families):
    asset_data = [
        {"name": "Tesouro Selic", "asset_type": "renda_fixa", "value": 10000.0, "acquisition_date": "2024-01-01", "details": {"indexador": "SELIC"}},
        {"name": "Ação XPTO", "asset_type": "renda_variavel", "value": 5000.0, "acquisition_date": "2023-12-01", "details": {"ticker": "XPTO3"}},
        {"name": "FII Alpha", "asset_type": "fundo_imobiliario", "value": 20000.0, "acquisition_date": "2022-06-15", "details": {"ticker": "ALPHA11"}},
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
                    "value": data["value"],
                    "acquisition_date": acq_date,
                    "details": data["details"]
                }
            )
    print(f"Ativos criados para cada família.")

def seed_alerts(families):
    for fam in families:
        alert, _ = get_or_create(
            Alert,
            family_id=fam.id,
            tipo="risco",
            mensagem="Exemplo de alerta de risco",
            severidade="warning"
        )
    print(f"Alertas de exemplo criados para cada família.")

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_permissions()
        admin = seed_admin()
        families, users = seed_families_and_users()
        seed_assets(families)
        seed_alerts(families)
        print("Seed concluído com sucesso.")

if __name__ == "__main__":
    main() 