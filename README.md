# letterboxd-movies-elo

**A Python tool to rank your watched movies on Letterboxd using an ELO-based duel system.**

Instead of manually ranking hundreds of films, this script lets you perform **pairwise duels** between movies you've watched. Your choices dynamically update each movie’s ELO score, gradually creating a personalized ranking of your collection.



## Features

- Import your watched movies from a CSV export from Letterboxd.
- Perform duels between two movies, or declare a tie.
- ELO system updates scores after every duel.
- Optional “skip” and “view ranking” options during the session.
- Automatically saves your progress to `elo.json`.
- Designed to prioritize **balanced duels** between movies with similar ELO scores.



## Installation

1. Clone this repository:  
```bash
git clone https://github.com/lucasrecan/letterboxd-movies-elo.git
cd letterboxd-movies-elo
```

2. Make sure you have Python 3 installed.

3. Prepare your CSV file exported from Letterboxd with a column named `Name`. Update the path in `main.py` if necessary:  
```python
csv_file = "data/watched.csv"
```



## Usage

1. Initialize or update your `elo_file` (`elo.json` by default) from the CSV:  
```bash
python update_elo_from_csv.py
```

2. Run the duel ranking interface:  
```bash
python main.py
```

3. During the session:  
- Choose the movie you prefer (`1` or `2`), or declare a tie (`3`).  
- Skip a duel (`4`).  
- View the current ranking (`5`).  
- Quit anytime with `q`.  

4. Your scores are automatically saved in `elo_file` after each session.



## How it Works

- Each movie starts with a default ELO of 1000.
- Duels are selected to be **between movies with similar ELO** (configurable with `max_elo_difference` in `main.py`).
- After each duel, ELO scores are updated using a standard formula:
  ```
  NewElo = OldElo + K * (Score - ExpectedScore)
  ```
- Tie results are also supported (`Score = 0.5`).



## Configuration

- `elo_file` : name of the file saving the ranks of the movies and their elo.
- `csv_file` : name of the csv file from which the watched movies are loaded.
- `default_elo` : initial ELO for new movies (default: 1000).  
- `max_elo_difference` : maximum allowed difference between movies in a duel (default: 25)
- `elo_factor` : ELO adjustment factor (default: 32).

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

