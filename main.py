import random
import json
import os
import math
import csv

csv_file = "letterboxd-ribou-data/watched.csv"     # ton export Letterboxd
elo_file = "elo.json"      # fichier de scores Elo
default_elo = 1000         # valeur par défaut pour les nouveaux films

def load_movies():
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        movies = [row["Name"].strip() for row in reader if row["Name"].strip()]
    print(f"Importé {len(movies)} films depuis {csv_file}")
    return movies

# Loading of Elo scores
def load_elo(movies, elo_file):
    if os.path.exists(elo_file):
        with open(elo_file, "r", encoding="utf-8") as f:
            elo = json.load(f)
    else:
        elo = {}
    added = 0
    for movie in movies:
        if movie not in elo:
            elo[movie] = default_elo
            added += 1
    with open(elo_file, "w", encoding="utf-8") as f:
        json.dump(elo, f, ensure_ascii=False, indent=2)
    
    print(f"{added} nouveaux films ajoutés.")
    print(f"Total : {len(elo)} films enregistrés dans {elo_file}")
    return elo

# Saving the new score in elo.json
def save_elo(elo, filename="elo.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(elo, f, ensure_ascii=False, indent=2)

# Random selection of two movies
def random_duel(movies):
    return random.sample(movies, 2)

# Calculate and update the new elo for both mobies
def update_elo(elo, winner, loser, k=32): # je choisis un k standard mais plus tard je peux faire un k progressif en fonction du nombre de duels pour accélerer le départ ?
    Ra = elo[winner]
    Rb = elo[loser]
    # E : probabilité de victoire attendue
    Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
    Eb = 1 - Ea

    elo[winner] = round(Ra + k * (1 - Ea))
    elo[loser] = round(Rb + k * (0 - Eb))

# Display ranking
def show_ranking(elo):
    print("\nClassement actuel :")
    ranked = sorted(elo.items(), key=lambda x: x[1], reverse=True)
    for i, (movie, rating) in enumerate(ranked, 1):
        print(f"{i:2d}. {movie:25s} ({rating})")

def main():
    movies = load_movies()
    print(movies)
    elo = load_elo(movies, elo_file)

    print("Système de duels ELO - Letterboxd\n")

    while True:
        a, b = random_duel(movies)
        print(f"\nQuel film préfères-tu ?")
        print(f"1: {a}  ({elo[a]})")
        print(f"2: {b}  ({elo[b]})")
        print("3: (voir classement)")
        print("q: quitter")

        choice = input("> ").strip().lower()

        if choice == "1":
            update_elo(elo, a, b)
        elif choice == "2":
            update_elo(elo, b, a)
        elif choice == "3":
            show_ranking(elo)
            continue
        elif choice == "q":
            break
        else:
            print("Choix invalide.")
            continue

        save_elo(elo)

    print("Progression sauvegardée. À bientôt !")

if __name__ == "__main__":
    main()
