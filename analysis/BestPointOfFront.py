import math

def read_points_from_file(filename):
    """
    Reads points (x, y) and their 'sequence' from a file and returns them as a list.
    :param filename: Name of the file.
    :return: List of points in the format (sequence, x, y).
    """
    points = []
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                # Removes leading and trailing spaces and splits the line content
                line = line.strip()

                # Finds the position where the sequence, x, and y start
                list_end = line.index(']') + 1  # Position after the list of chars

                # Remaining part of the line (sequence, x, y)
                remainder = line[list_end:].strip()

                # Removes unnecessary characters like ')' at the end
                if remainder.endswith(')'):
                    remainder = remainder[:-1]  # Removes the last character ')'

                # Splits the string into sequence, x, and y
                parts = remainder.split(', ')

                # Extracts the sequence and converts x, y to float
                sequence = parts[1].strip("'")
                x = float(parts[2])  # Converts to float
                y = float(parts[3])  # Converts to float

                points.append((sequence, x, y))

            except (ValueError, IndexError, SyntaxError) as e:
                print(f"Error in line {line_number}: {line} -> {e}")
    return points

def find_closest_point(points, target_x, target_y):
    """
    Finds the point closest to (target_x, target_y) using Euclidean distance.
    :param points: List of points in the format (sequence, x, y).
    :param target_x: x coordinate of the target point.
    :param target_y: y coordinate of the target point.
    :return: Closest point in the format (sequence, x, y).
    """
    if not points:
        return None

    # Calculates distance and finds the point with the smallest distance
    closest_point = min(points, key=lambda point: math.sqrt((point[1] - target_x) ** 2 + (point[2] - target_y) ** 2))
    return closest_point

# Testing the function
filename = "analysis/front.txt"
points = read_points_from_file(filename)

# Finding the maximum x and y in the list of points
max_x = max(points, key=lambda point: point[1])[1]
max_y = max(points, key=lambda point: point[2])[2]

# Finding the point closest to the maximum x and y
closest_point = find_closest_point(points, max_x, max_y)

if closest_point:
    print(f"Best point:  {closest_point}")
else:
    print("No points found.")
