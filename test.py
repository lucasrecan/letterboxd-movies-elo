import csv
with open("letterboxd-ribou-data/ratings.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    print(reader.fieldnames)
    for row in reader:
        print(repr(row["Rating"]))
        break