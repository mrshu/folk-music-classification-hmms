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
    return -1


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


def range_of_track(track):
    notes = []
    for msg in track:
        if msg.type in ('note_on', 'note_off'):
            notes.append(msg.note)
    if len(notes) == 0:
        return 0
    return max(notes)-min(notes)


def bass_penalty(track):
    program = program_of_track(track)
    bass_programs = [-1, 6, 7, 77, 52, 58] + list(range(81, 128))
    if program in bass_programs:
        return 0
    return 1

mid = MidiFile(sys.argv[1])

new_mid = MidiFile()

tracks_metadata = []
for t in mid.tracks:
    tracks_metadata.append((program_of_track(t), len(t),
                            max_velocity_of_track(t), min_note_of_track(t),
                            range_of_track(t), bass_penalty(t)))

t = np.array(tracks_metadata).astype('float32')
# print(t)
# t[:, 0] = np.exp(t[:, 0] / t[:, 0].max())
# t = t / t.sum(axis=0)
res = t[:, 2] * t[:, 4] * t[:, 5]
# print(t)
# print(t[:, 0])
print(res)
index = np.argmax(res)
program = int(t[index, 0])
if program != -1:
    chosen_instrument = pretty_midi.program_to_instrument_name(program)
else:
    chosen_instrument = 'Unknown (Probabily Piano)'
print("Chose index {} ({} - {}) for {}".format(index, program,
                                               chosen_instrument,
                                               sys.argv[1]))

new_mid.tracks.append(mid.tracks[index])
new_mid.ticks_per_beat = mid.ticks_per_beat
new_mid.save(sys.argv[1] + '.mono')
