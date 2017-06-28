import os


def load_notes(file, maxlen=32, suffix='.notes'):
    with open(file, 'r') as f:
        line = f.readline()
        return line.split(', ')[:maxlen]


def load_notes_from_dir(dir, maxlen=32, suffix='.notes'):
    notes = []
    for (dirpath, _, filenames) in os.walk(dir):
        for file in filenames:
            if file.endswith(suffix):
                notes.append(load_notes(os.sep.join([dirpath, file]),
                                        maxlen=maxlen))
    return notes


def compute_sigma(notes):
    sigma = set()
    for x in notes:
        for l in x:
            sigma.add(l)
    return sigma
