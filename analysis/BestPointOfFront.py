import math

def read_points_from_file(filename):
    """
    Čita točke (x, y) i njihov 'sequence' iz datoteke i vraća ih kao listu.
    :param filename: Naziv datoteke.
    :return: Lista točaka u formatu (sequence, x, y).
    """
    points = []
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                # Uklanja početni i završni razmak te dijeli sadržaj linije
                line = line.strip()

                # Pronalaženje pozicije gdje počinje sequence, x i y
                list_end = line.index(']') + 1  # Pozicija nakon liste chars

                # Ostatak linije (sequence, x i y)
                remainder = line[list_end:].strip()

                # Uklanjanje nepotrebnih znakova poput ')' sa kraja
                if remainder.endswith(')'):
                    remainder = remainder[:-1]  # Uklanja posljednji znak ')'

                # Razdvaja string na sequence, x i y
                parts = remainder.split(', ')

                # Uzimanje sequence i konvertiranje x, y u float
                sequence = parts[1].strip("'")
                x = float(parts[2])  # Pretvara u float
                y = float(parts[3])  # Pretvara u float

                points.append((sequence, x, y))

            except (ValueError, IndexError, SyntaxError) as e:
                print(f"Pogreška u retku {line_number}: {line} -> {e}")
    return points

def find_closest_point(points, target_x, target_y):
    """
    Pronalazi točku koja je najbliža točki (target_x, target_y) koristeći euclidsku udaljenost.
    :param points: Lista točaka u formatu (sequence, x, y).
    :param target_x: x koordinata ciljne točke.
    :param target_y: y koordinata ciljne točke.
    :return: Najbliža točka u formatu (sequence, x, y).
    """
    if not points:
        return None

    # Računa udaljenost i nalazi točku s najmanjom udaljenosti
    closest_point = min(points, key=lambda point: math.sqrt((point[1] - target_x) ** 2 + (point[2] - target_y) ** 2))
    return closest_point

# Testiranje funkcije
filename = "analysis/front.txt"
points = read_points_from_file(filename)

# Pronalaženje najvećeg x i y u listi točaka
max_x = max(points, key=lambda point: point[1])[1]
max_y = max(points, key=lambda point: point[2])[2]

# Pronalaženje točke koja je najbliža najvećem x i y
closest_point = find_closest_point(points, max_x, max_y)

if closest_point:
    print(f"Najbolja točka:  {closest_point}")
else:
    print("Nema točaka.")
