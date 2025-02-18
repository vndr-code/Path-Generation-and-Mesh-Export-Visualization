import csv


def load_path(filename):
    points = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            points.append((float(row['x']), float(row['y']), float(row['z'])))
    return points