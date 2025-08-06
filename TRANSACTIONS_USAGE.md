# Sistema de Transações - Guia de Uso

## Visão Geral

O sistema de transações permite controlar os valores dos ativos de forma dinâmica baseado em operações de compra e venda.

## Modelos

### Transaction
- `asset_id`: ID do ativo relacionado
- `transaction_type`: "buy" ou "sell" 
- `quantity`: Quantidade da transação
- `unit_price`: Preço unitário
- `total_value`: Valor total (calculado automaticamente)
- `transaction_date`: Data da transação
- `description`: Descrição opcional

### Asset (Propriedades Calculadas)
- `current_quantity`: Quantidade atual baseada em transações
- `current_value`: Valor atual (quantidade × custo médio)
- `average_cost`: Custo médio ponderado (FIFO)
- `total_invested`: Total investido em compras
- `total_divested`: Total recebido em vendas

## API Endpoints

### Criar Transação
```http
POST /transactions
Authorization: Bearer <token>
Content-Type: application/json

{
  "asset_id": 1,
  "transaction_type": "buy",
  "quantity": 100.0,
  "unit_price": 10.50,
  "transaction_date": "2024-01-15",
  "description": "Compra inicial"
}
```

### Listar Transações
```http
GET /transactions?asset_id=1&limit=50
Authorization: Bearer <token>
```

### Obter Transação
```http
GET /transactions/1
Authorization: Bearer <token>
```

### Atualizar Transação
```http
PUT /transactions/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "quantity": 150.0,
  "description": "Quantidade atualizada"
}
```

### Deletar Transação
```http
DELETE /transactions/1
Authorization: Bearer <token>
```

### Resumo de Transações por Ativo
```http
GET /transactions/asset/1/summary
Authorization: Bearer <token>
```

## Exemplo de Uso Python

```python
from app import create_app
from app.models import Asset, Transaction
from app.config.extensions import db

app = create_app()
with app.app_context():
    # Obter ativo
    asset = Asset.query.get(1)
    
    # Criar transação de compra
    buy_transaction = Transaction(
        asset_id=asset.id,
        transaction_type="buy",
        quantity=100.0,
        unit_price=10.0
    )
    db.session.add(buy_transaction)
    db.session.commit()
    
    # Verificar valores atualizados
    print(f"Quantidade atual: {asset.current_quantity}")  # 100.0
    print(f"Valor atual: {asset.current_value}")          # 1000.0
    print(f"Custo médio: {asset.average_cost}")           # 10.0
    
    # Criar transação de venda
    sell_transaction = Transaction(
        asset_id=asset.id,
        transaction_type="sell",
        quantity=30.0,
        unit_price=12.0
    )
    db.session.add(sell_transaction)
    db.session.commit()
    
    # Verificar novos valores
    print(f"Quantidade atual: {asset.current_quantity}")  # 70.0
    print(f"Valor atual: {asset.current_value}")          # 700.0
    print(f"Total investido: {asset.total_invested}")     # 1000.0
    print(f"Total recebido: {asset.total_divested}")      # 360.0
```

## Validações Automáticas

1. **Quantidade e preço positivos**: Valores devem ser > 0
2. **Tipo de transação válido**: Apenas "buy" ou "sell"
3. **Venda limitada**: Não é possível vender mais do que se possui
4. **Controle de acesso**: Usuário deve ter acesso à família do ativo

## Migração de Dados Existentes

Para migrar ativos existentes com valores estáticos para o sistema de transações:

```python
# Script de migração (exemplo)
assets = Asset.query.all()
for asset in assets:
    if asset.value and asset.value > 0:
        # Criar transação inicial baseada no valor existente
        initial_transaction = Transaction(
            asset_id=asset.id,
            transaction_type="buy",
            quantity=1.0,  # ou calcular baseado em informações adicionais
            unit_price=asset.value,
            transaction_date=asset.acquisition_date or date.today(),
            description="Migração de valor inicial"
        )
        db.session.add(initial_transaction)

db.session.commit()
```

## Considerações de Performance

- Valores são calculados em tempo real
- Para ativos com muitas transações, considere adicionar índices
- Cache pode ser implementado para dashboards com muitos ativos
- Use filtros nas consultas para otimizar performance

## Testes

Execute os testes do sistema de transações:

```bash
poetry run python -m pytest tests/transactions/ -v
```