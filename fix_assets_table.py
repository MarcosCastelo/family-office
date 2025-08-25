#!/usr/bin/env python3
"""Script para forçar a remoção do campo value da tabela assets"""

import sqlite3
import os
import json

def fix_assets_table():
    """Remove o campo value da tabela assets"""
    
    # Caminho para o banco SQLite
    db_path = 'instance/local.db'
    
    if not os.path.exists(db_path):
        print(f"Banco de dados não encontrado em: {db_path}")
        return
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Verificando estrutura atual da tabela assets...")
        
        # Verificar colunas atuais
        cursor.execute("PRAGMA table_info(assets)")
        columns = cursor.fetchall()
        
        print("Colunas atuais:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULLABLE'}")
        
        # Verificar se o campo value existe
        value_column = [col for col in columns if col[1] == 'value']
        
        if not value_column:
            print("✅ Campo 'value' não existe na tabela. Nada a fazer.")
            return
        
        print(f"\n🚨 Campo 'value' encontrado: {value_column[0]}")
        
        # Verificar se há dados na tabela
        cursor.execute("SELECT COUNT(*) FROM assets")
        count = cursor.fetchone()[0]
        print(f"📊 Total de registros na tabela: {count}")
        
        if count > 0:
            print("⚠️  ATENÇÃO: Existem dados na tabela. Fazendo backup...")
            
            # Fazer backup dos dados
            cursor.execute("SELECT * FROM assets")
            rows = cursor.fetchall()
            
            # Salvar backup
            backup_file = 'assets_backup.json'
            backup_data = []
            
            for row in rows:
                row_data = {
                    'id': row[0],
                    'name': row[1],
                    'asset_type': row[2],
                    'acquisition_date': row[3],
                    'details': row[4],
                    'family_id': row[5],
                    'created_at': row[6]
                }
                backup_data.append(row_data)
            
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2, default=str)
            
            print(f"💾 Backup salvo em: {backup_file}")
        
        print("\n🔧 Recriando tabela sem o campo 'value'...")
        
        # Criar nova tabela sem o campo value
        cursor.execute("""
            CREATE TABLE assets_new (
                id INTEGER NOT NULL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                asset_type VARCHAR(50) NOT NULL,
                acquisition_date DATE,
                details JSON,
                family_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(family_id) REFERENCES family (id)
            )
        """)
        
        # Copiar dados da tabela antiga para a nova
        if count > 0:
            cursor.execute("""
                INSERT INTO assets_new (id, name, asset_type, acquisition_date, details, family_id, created_at)
                SELECT id, name, asset_type, acquisition_date, details, family_id, created_at
                FROM assets
            """)
            print(f"📋 Dados copiados: {cursor.rowcount} registros")
        
        # Remover tabela antiga
        cursor.execute("DROP TABLE assets")
        print("🗑️  Tabela antiga removida")
        
        # Renomear nova tabela
        cursor.execute("ALTER TABLE assets_new RENAME TO assets")
        print("🔄 Nova tabela renomeada para 'assets'")
        
        # Verificar estrutura final
        cursor.execute("PRAGMA table_info(assets)")
        final_columns = cursor.fetchall()
        
        print("\n✅ Estrutura final da tabela:")
        for col in final_columns:
            print(f"  - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULLABLE'}")
        
        # Commit das mudanças
        conn.commit()
        print("\n🎉 Tabela assets corrigida com sucesso!")
        
        if count > 0:
            print(f"📊 Total de registros preservados: {count}")
            print(f"💾 Backup disponível em: {backup_file}")
        
    except Exception as e:
        print(f"❌ Erro ao corrigir tabela: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Iniciando correção da tabela assets...")
    fix_assets_table()
    print("✅ Processo concluído!")
