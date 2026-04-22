import os
import sqlalchemy
from sqlalchemy import text
from database import get_engine
from dotenv import load_dotenv

load_dotenv()

def run_migrations():
    print("--- Inizio Migrazione Database ---")
    engine = get_engine()
    sql_dir = os.path.join(os.path.dirname(__file__), '..', 'sql')
    
    # Lista i file SQL in ordine alfabetico
    sql_files = sorted([f for f in os.listdir(sql_dir) if f.endswith('.sql')])
    
    if not sql_files:
        print("Nessun file SQL trovato nella cartella sql/")
        return

    with engine.connect() as connection:
        # Usiamo una transazione per assicurarci che tutto vada a buon fine
        trans = connection.begin()
        try:
            for sql_file in sql_files:
                print(f"Esecuzione di {sql_file}...")
                file_path = os.path.join(sql_dir, sql_file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                    
                    # Suddividiamo il contenuto per punto e virgola per eseguire un comando alla volta
                    # (SQLAlchemy non sempre gestisce bene script multipli in una singola chiamata execute)
                    commands = sql_content.split(';')
                    for command in commands:
                        cmd = command.strip()
                        if cmd:
                            connection.execute(text(cmd))
                
                print(f"Completato: {sql_file}")
            
            trans.commit()
            print("--- Migrazione completata con successo! ---")
        except Exception as e:
            trans.rollback()
            print(f"ERRORE durante la migrazione: {e}")
            raise e

if __name__ == "__main__":
    run_migrations()
