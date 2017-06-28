from mido import Message, MidiFile, MidiTrack
import sys


def load_notes(file):
    with open(file, 'r') as f:
        line = f.readline()
        return list(map(int, line.split(', ')))


def notes_to_intervals(notes):
    prev = None
    out = []
    for n in notes:
        if prev is None:
            prev = n
        else:
            diff = n - prev
            if abs(diff) > 13:
                diff = 13
            out.append(str(diff))
    return out


def notes_to_contours(notes):
    prev = None
    out = []
    for n in notes:
        if prev is None:
            prev = n
        else:
            diff = n - prev
            if diff == 0:
                out.append('0')
            elif diff in [1, 2]:
                out.append('+')
            elif diff > 3:
                out.append('++')
            elif diff in [-1, -2]:
                out.append('-')
            elif diff < -3:
                out.append('--')
    return out


notes = load_notes(sys.argv[1])
# print(', '.join(notes_to_intervals(notes)))
print(', '.join(notes_to_contours(notes)))
