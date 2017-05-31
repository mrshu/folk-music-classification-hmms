from mido import Message, MidiFile, MidiTrack
from operator import itemgetter
import numpy as np
import click
import sys
import pretty_midi


def program_of_track(track):
    for msg in track:
        if msg.type == 'program_change':
            return msg.program
    return 1024


def time_of_track(track):
    t = 0.0
    for msg in track:
        t += msg.time
    return t + 1.0


def max_velocity_of_track(track):
    velocities = [0]
    for msg in track:
        if msg.type in ('note_on', 'note_off'):
            velocities.append(msg.velocity)
    return max(velocities)


def min_note_of_track(track):
    notes = [10000.0]
    for msg in track:
        if msg.type in ('note_on', 'note_off'):
            notes.append(msg.note)
    return sum(notes)/len(notes)

mid = MidiFile(sys.argv[1])

new_mid = MidiFile()

tracks_metadata = []
for t in mid.tracks:
    tracks_metadata.append((program_of_track(t), len(t),
                            max_velocity_of_track(t), min_note_of_track(t)))

t = np.array(tracks_metadata).astype('float32')
print(t)
# t[:, 0] = np.exp(t[:, 0] / t[:, 0].max())
# t = t / t.sum(axis=0)
res = t[:, 2]  # * t[:, 3]
print(t)
print(res)
index = np.argmax(res)

print("Chose index {} for {}".format(index, sys.argv[1]))

new_mid.tracks.append(mid.tracks[index])
new_mid.ticks_per_beat = mid.ticks_per_beat
new_mid.save(sys.argv[1] + '.mono')
