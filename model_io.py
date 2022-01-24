import csv


def load_scoreboard():
    """
    Funckja ładująca dane z pliku scoreboard.csv.
    Zwraca je w postaci słownika {'nickanme': 'score'}
    """
    with open("scoreboard.csv", "r", newline="") as f:
        r = csv.DictReader(f)
        players = {}
        for row in r:
            players[row["nickname"]] = int(row["score"])
        return players


def save_score(nickname, score):
    """
    Funckcja dodająca danego gracza, po wpisaniu sowjego nicku na ekranie ENDGAME.
    Jeżeli już wcześniej grał gracz o takim nicku, to aktualizuję jego wynik.
    Jednocześnie sortuję wszystkich graczy w zależności od score.
    """
    nickname = nickname.rstrip()
    players = load_scoreboard()
    if nickname in players.keys():
        if players[nickname] < score:
            players[nickname] = score
    else:
        players[nickname] = score

    sorted_players = sort_players(players)

    with open("scoreboard.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, ["no.", "nickname", "score"])
        writer.writeheader()
        i = 1
        for nick, score in sorted_players.items():
            writer.writerow({"no.": i, "nickname": nick, "score": score})
            i += 1


def clear_scoreboard():
    """
    Funkcja czyszcząca plik socreboard.csv.
    Zapisuję w nim jedynie nagłówek.
    """
    with open("scoreboard.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, ["no.", "nickname", "score"])
        writer.writeheader()


def sort_players(players):
    """
    Funkcja sortujaca graczy (players).
    Zwraca posortowany słownik.
    """
    sorted_players = {}
    keys = list(players.keys())
    val = list(players.values())
    sorted_val = val.copy()
    sorted_val.sort()
    sorted_val.reverse()
    for value in sorted_val:
        idx = val.index(value)
        val[idx] = -1
        sorted_players[keys[idx]] = value
    return sorted_players


def read_readme():
    """
    Funckja odzcytująca zawrtość pliku readme.txt, potrzebna do funkcji main.help
    """
    with open("readme.txt", "r") as f:
        header = f.readline()
        text = ""
        for line in f:
            text += line
        return header, text
