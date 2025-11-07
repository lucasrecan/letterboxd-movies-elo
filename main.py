import random
import json
import update_elo_from_csv

elo_file = "elo.json"      # fichier de scores Elo

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
    with open(elo_file, "r", encoding="utf-8") as f:
        elo = json.load(f)
    
    if len(elo) == 0:
        update_elo_from_csv.update()

    movies = list(elo.keys())
    # print(movies)
    print("Système de duels ELO - Letterboxd\n")

    while True:
        a, b = random_duel(movies)
        print(f"Quel film préfères-tu ?")
        print(f"1: {a}  ({elo[a]})")
        print(f"2: {b}  ({elo[b]})")
        print(f"3: Égalité ou passer")
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

if __name__ == "__main__":
    main()
