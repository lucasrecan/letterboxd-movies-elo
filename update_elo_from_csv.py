import json
import os
import csv
from statistics import mean

csv_file = "letterboxd-ribou-data/ratings.csv"
elo_file = "elo.json"
default_elo = 1000
standard_deviation = 200
average_note = 3
elo_by_note = False
overwrite = False

def update():
    if os.path.exists(csv_file):
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            movies = [row["Name"].strip() for row in reader if row["Name"].strip()]
            print(f"Importé {len(movies)} films depuis {csv_file}")
            ratings = [float(row["Rating"].strip()) for row in reader if row["Rating"].strip()]
            average_note = round(mean(ratings) * 2) / 2 # round to the half-star
            print(average_note)
    else:
        movies = []
        print(f"{csv_file} n'existe pas.")

    if not os.path.exists(elo_file):
        with open(elo_file, "w", encoding="utf-8") as f:
            pass
        print("elo.json created")
        elo = {}
    else:
        with open(elo_file, "r", encoding="utf-8") as f:
            elo = json.load(f)
    added = 0
    init_by_note = input("Initialize default elo by letterboxd note? (y/n) > ")
    overwrite = input("Overwrite elo.json? (y/n) > ")
    if init_by_note == "y":
        elo_by_note = True
    if overwrite == "y":
        overwrite = True
    for i in range(len(movies)): 
        if movies[i] not in elo or overwrite:
            if elo_by_note:
                elo[movies[i]] = default_elo + standard_deviation * (ratings[i] - average_note)
            else:
                elo[movies[i]] = default_elo
            added += 1
    with open(elo_file, "w", encoding="utf-8") as f:
        json.dump(elo, f, ensure_ascii=False, indent=2)
    
    print(f"{added} nouveaux films ajoutés.")
    print(f"Total : {len(elo)} films enregistrés dans {elo_file}")

if __name__ == '__main__':
    update()