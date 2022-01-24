import random


def get_middle_scr(stdscr):
    """
    Funckja zwracająca wymniary ekranu (screen)
    """
    my, mx = stdscr.getmaxyx()
    return my // 2, mx // 2


def place_symetrically(
    y, x, amount, ycentric=False, xcentric=True, width=1, heigth=0
) -> dict:
    """
    Funckja wyliczająca współrzędne rozmieszczone symetrycznie na podanej osi x, y.
    Ilośc takich punktów jest zależna od parametru amount.
    Paramtery ycentric i xcentrix odpowiadają za wyśrodkowanie danego obiektu względem osi.
    W przypadku wartości False, funkcja wyliczy gdzie powinny się znajdować lewe-górne rogi obiektów o wymairach width i height.
    W przypadku wartości True funckja wylicza matematyczny środek
    Współrzędne zwracane są w postaci słownika. {1: (y0, x0), 2: (y1, x1), ...}
    """
    placement = {}
    x += width
    rest_x = x % (amount + 1)
    x -= rest_x
    if ycentric is True:
        y -= heigth
        y //= 2
        y -= heigth // 2
    interval = x / (amount + 1)
    if xcentric is False:
        x = interval + rest_x // 2 - 2 * width // 2
    else:
        x = interval + rest_x // 2 - width // 2
    placement[0] = (int(y), int(x))
    for i in range(1, amount):
        x += interval
        placement[i] = (int(y), int(x))
    return placement


def draw_object(scr, obj, cordinates, color, center=False):
    """
    Funkcja rysuję obiekt (jego atrybut body) w miejscu podanym przez prametr cordinates.
    center działa w ten sam sposób co centric w place_symetrically (fun).
    Dodakowo zwraca hitbox narysowanych obiektów.
    """
    body = obj.body()

    mock_hitbox = {}
    if body[-1] == "\n":
        body = body[:-1]
    body_ls = body.splitlines()
    y, x = cordinates
    length = [len(line) for line in body_ls]
    if center is True:
        x -= max(length) // 2
    i = 0
    scr.attron(color)
    for line in body_ls:
        scr.addstr(y + i, x, line)
        for index, char in enumerate(line):
            if char != " ":
                mock_hitbox[(y + i, x + index)] = (obj, char)
        i += 1
    scr.attroff(color)
    scr.refresh()
    return mock_hitbox


def objclear(obj):
    """
    Funckja czyszcząca dany obiekt z ekranu, uwaga nie usuwa jego hitbox'u
    """
    body = obj.body()
    y, x = obj.keys_mock_hitbox()[0]
    body_ls = body.splitlines()
    i = 0
    for line in body_ls:
        line = len(line) * " "
        obj.scr().addstr(y + i, x, line)
        i += 1
    return True


def move_obj_yx(obj, down=None, right=None, distance=1):
    """
    Funkcja przesuwjąca obiekt w którą kolwiek z 4 stron.
    Paramter distance definiuje odległość o jaką zostanie przesunięty obiekt.
    """
    index = len(obj.keys_mock_hitbox()) // 2
    y, x = obj.keys_mock_hitbox()[index]
    scr = obj.scr()
    maxy, maxx = scr.getmaxyx()
    if maxy == 1:
        maxx -= 1
    if down is True and y + distance < maxy - 1:
        y += distance
    elif down is False and y - distance > 0:
        y -= distance

    if right is True and obj.keys_mock_hitbox()[-1][1] < maxx - 1:
        x += distance
    elif right is False and obj.keys_mock_hitbox()[0][1] > 0:
        x -= distance

    obj.draw((y, x))


def time_to_die(
    scr, bullets, score, run, distance=1
):  # function which move bullets
    """
    Funckja odpowiadająca za logikę pocisków.
    Przesuwa wszystkie pociski znajdujące sie w liscie z paramteru bullets.
    Dodakowo zlicza ilość pocisków którę trafiły w danym wywołąniu ale jedynie tych lecących w konkretną storne.
    Jest w stanie przesuwać pociski o więcej niż jeden (distance) w jednym wywołaniu.
    Zwraca score.
    """
    if run:
        for bullet in bullets:
            sm = bullet.space_management()
            y, x = bullet.keys_hitbox()[0]
            body = bullet.vals_hitbox()[0][1]
            scr.addstr(y, x, " ")
            if y <= 0 or y >= scr.getmaxyx()[0] - 1:
                bullets.remove(bullet)
            elif (y, x) in sm.keys():
                obj = sm[(y, x)][0]
                if bullet.direction() and obj.body() == "@":
                    score += 1
                elif not bullet.direction() and obj.body() == "|o|":
                    obj.take_damage()
                obj.remove()
                bullets.remove(bullet)
                bullet.new_assigment_sm(delate={(y, x): None})
            else:
                if bullet.direction():
                    move = -1
                else:
                    move = 1
                scr.addstr(y + move, x, body)
                bullet.tick((y, x), distance)
            scr.refresh()
    return score


def move_enemies(scr, allenemies, flag, right, run):
    """
    Przesuwa wszysktich wrogów znajdujących się w dwuwymairowym słowniku allenemies, w zależności od flagi przesuwa ich w górę lub w dół.
    W zaleznosci od right w prawo lub w lewo.
    Zwraca falg, right.
    """
    if run:
        y, x = scr.getmaxyx()
        last_x = 0
        first_x = x
        enemies = []

        for column in allenemies:
            for enemy in column.values():
                x0 = enemy.keys_mock_hitbox()[0][1]
                x1 = enemy.keys_mock_hitbox()[-1][1]
                enemies.append(enemy)
                if first_x > x0:
                    first_x = x0
                if last_x < x1:
                    last_x = x1

        enemies.reverse()

        if flag is False:
            for enemy in enemies:
                if last_x >= x - 1:
                    objclear(enemy)
                    move_obj_yx(enemy, down=True)
                    right = False
                    flag = True
                elif first_x <= 1:
                    objclear(enemy)
                    move_obj_yx(enemy, down=True)
                    right = True
                    flag = True
                else:
                    objclear(enemy)
                    move_obj_yx(enemy, right=right)
        elif flag is True:
            for enemy in enemies:
                objclear(enemy)
                move_obj_yx(enemy, right=right)
                flag = False
    return flag, right


def random_enemy_shot(scr, columns, intense):
    """
    Funckja znajdująca przeciwników znajdujacych sie we frontowym rzędzie w słownikach przekazanych za pomocą parametru columns (dwuwymiarowy słownik).
    Parametr instnse odpowiada za częstotliwośc strzelania przeciwników. Zalecane wartości [30, 100] - można w ten sposób regulwoać trudnośc rozgrywki.
    """
    intense *= 10000
    front_row = []
    for column in columns:
        if column:
            max_row = max(column.keys())
            front_row.append(column[max_row])
    if random.randint(0, 100000000) < intense:
        enemy = random.choice(front_row)
        enemy.shot(scr, direction=False)
    return front_row


def check_endgame(front_row, endgame):
    """
    Funckja sprawdzająca czy któryś z przeciwników nie znajduję się już w rogu enemieswin (ekranu wrogów).
    Jeśli się któryś znajduję, kończy rozgrywkę.
    """
    for enemy in front_row:
        y, x = enemy.scr().getmaxyx()
        if enemy.keys_mock_hitbox()[-1] == (y - 2, x - 1):
            endgame = True
    return endgame
