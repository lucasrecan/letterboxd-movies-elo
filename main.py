import os
import random
import json
import update_elo_from_csv
import csv

elo_file = "elo.json"
csv_file = "letterboxd-ribou-data/watchedd..csv" 
default_elo = 1000

def has_csv_changed(movies, csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_movies = [row["Name"].strip() for row in reader if row["Name"].strip()]
    return not(len(movies) == len(csv_movies))


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
    # create elo.json if it doesn't exist
    if not os.path.exists(elo_file):
        update_elo_from_csv.update()

    if os.path.getsize(elo_file) == 0:
        print("No movies to rank. Initialize csv_file with the path of your file with a column titled 'Name'.")
        exit(1)

    with open(elo_file, "r", encoding="utf-8") as f:
        elo = json.load(f)

    movies = list(elo.keys())
        
    print("Système de duels ELO - Letterboxd\n")

    while True:
        a, b = random_duel(movies)
        print(f"Quel film préfères-tu ?")
        print(f"1: {a}  ({elo[a]})")
        print(f"2: {b}  ({elo[b]})")
        print(f"3: Passer")
        print("4: (voir classement)")
        print("q: quitter")

        choice = input("> ").strip().lower()

        if choice == "1":
            update_elo(elo, a, b)
        elif choice == "2":
            update_elo(elo, b, a)
        elif choice == "3":
            continue
        elif choice == "4":
            show_ranking(elo)
            continue
        elif choice == "q":
            break
        else:
            print("Choix invalide.")
            continue

        save_elo(elo)

    print("Progression sauvegardée. À bientôt !")
    exit(0)

if __name__ == "__main__":
    main()
