import os
import random
import json
import update_elo_from_csv
import csv

elo_file = "elo.json"
csv_file = "letterboxd-ribou-data/watched.csv" 
default_elo = 1000
max_elo_difference = 25
elo_factor = 32

def has_csv_changed(movies, csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_movies = [row["Name"].strip() for row in reader if row["Name"].strip()]
    return not(len(movies) == len(csv_movies))


# Saving the new score in elo.json
def save_elo(elo, filename=elo_file):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(elo, f, ensure_ascii=False, indent=2)

# Random selection of two movies
def random_duel(movies):
    return random.sample(movies, 2)

def select_duel(movies, elo, max_diff=max_elo_difference):
    movie_a = random.choice(movies)
    rating_a = elo[movie_a]
    close_movies = []
    for m in movies:
        if m != movie_a:
            diff = abs(elo[m] - rating_a)
            if diff <= max_diff:
                close_movies.append(m)

    if len(close_movies) == 0:
        print(f"No movie with a elo difference lower than {max_diff}, random movie selected")
        movie_b = random.choice([m for m in movies if m != movie_a])
    else:
        movie_b = random.choice(close_movies)
    return movie_a, movie_b

def calculate_elo_change(elo, movie_a, movie_b, k=elo_factor):
    Ra = elo[movie_a]
    Rb = elo[movie_b]

    # Probabilités de victoire attendues
    Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
    Eb = 1 - Ea
    
    possible_results = [1, 0, 0.5]
    deltas = []

    for result in possible_results:
        deltas.append(round(k * (result - Ea), 1))

    return {
        "win": deltas[0],
        "lose": deltas[1],
        "draw": deltas[2]
    }

# Calculate and update the new elo for both movies
# result = 1 if movie_a wins,
# result = 0 if movie_b wins,
# result = 0.5 if draw
def update_elo(elo, movie_a, movie_b, result, k=32):
    a_elo_change = calculate_elo_change(elo, movie_a, movie_b, k)
    if result == 1:
        delta_a = a_elo_change["win"]
    elif result == 0:
        delta_a = a_elo_change["lose"]
    else:  # 0.5
        delta_a = a_elo_change["draw"]

    elo[movie_a] = round(elo[movie_a] + delta_a)
    elo[movie_b] = round(elo[movie_b] - delta_a)

# Display ranking
def show_ranking(elo, n):
    print("\nClassement actuel :")
    ranked = sorted(elo.items(), key=lambda x: x[1], reverse=True)[:n]
    for i, (movie, rating) in enumerate(ranked, 1):
        print(f"{i:2d}. {movie:35s} ({rating})")
    input("Press Enter to continue...")

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
        a, b = select_duel(movies, elo)
        a_elo_change = calculate_elo_change(elo, a, b)
        b_elo_change = calculate_elo_change(elo, b, a)
        print(f"Quel film préfères-tu ?")
        print(f"1: {a}  ({elo[a]})")
        print(f"win: {a_elo_change['win']} | lose: {a_elo_change['lose']} | draw: {a_elo_change['draw']}")
        print(f"2: {b}  ({elo[b]})")
        print(f"win: {b_elo_change['win']} | lose: {b_elo_change['lose']} | draw: {b_elo_change['draw']}")
        print(f"3: Égalité")
        print(f"4: Passer")
        print("5: (voir classement)")
        print("q: quitter")

        choice = input("> ").strip().lower()

        if choice == "1":
            update_elo(elo, a, b, result=1)
        elif choice == "2":
            update_elo(elo, a, b, result=0)
        elif choice == "3":
            update_elo(elo, a, b, result=0.5)
        elif choice == "4":
            continue
        elif choice == "5":
            print(f"Afficher les n premiers éléments (nombre de films : {len(elo)}) avec n : ")
            nb = input("> ")
            show_ranking(elo, nb)
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
