import json
import os
import csv

csv_file = "letterboxd-ribou-data/watched.csv"
elo_file = "elo.json"
default_elo = 1000

def update():
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        movies = [row["Name"].strip() for row in reader if row["Name"].strip()]

    print(f"Importé {len(movies)} films depuis {csv_file}")

    if not os.path.exists(elo_file):
        with open(elo_file, "w", encoding="utf-8") as f:
            pass
        print("elo.json created")
        elo = {}
    else:
        with open(elo_file, "r", encoding="utf-8") as f:
            elo = json.load(f)
    added = 0
    for movie in movies:
        if movie not in elo:
            elo[movie] = default_elo
            added += 1
    with open(elo_file, "w", encoding="utf-8") as f:
        json.dump(elo, f, ensure_ascii=False, indent=2)
    
    print(f"{added} nouveaux films ajoutés.")
    print(f"Total : {len(elo)} films enregistrés dans {elo_file}")

if __name__ == '__main__':
    update()