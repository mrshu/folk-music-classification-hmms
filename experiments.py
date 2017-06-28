from pprint import pprint
from sklearn.model_selection import train_test_split
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import classification_report, accuracy_score
from utils import load_notes_from_dir, compute_sigma
from model import hmm_model
import numpy as np
import pandas as pd
np.random.seed(1234)


def run_test(subsets, data, n_states=3, trans_type='a'):
    hmms = {}
    sigmas = {}
    selector = None
    for s in subsets:
        if selector is None:
            selector = (data.type == s)
        else:
            selector |= (data.type == s)
    selected_data = data[selector]

    p = None

    accuracies = []
    X = selected_data['notes']
    y = selected_data['type']
    ss = ShuffleSplit(n_splits=17, test_size=0.3, random_state=42)
    for train, test in ss.split(X, y):
        X_train, y_train = X.iloc[train], y.iloc[train]
        X_test, y_test = X.iloc[test], y.iloc[test]

        # print(list(y_test))

        for c in subsets:
            notes = X_train[y_train == c]
            sigmas[c] = compute_sigma(notes)
            hmms[c] = hmm_model(n_states=n_states, sigma=sigmas[c],
                                trans_type=trans_type)
            hmms[c].fit(notes, verbose=0, n_jobs=64, max_iterations=100)

        results = []
        for (x, _) in zip(X_test, y_test):
            r = []
            for c in subsets:
                x_filtered = [z for z in x if z in sigmas[c]]
                r.append(hmms[c].viterbi(x_filtered)[0])
            results.append(subsets[np.argmax(r)])
        # print(classification_report(results, y_test))
        acc = accuracy_score(results, y_test)
        accuracies.append(acc)
        print(acc)
    return (np.mean(accuracies), np.std(accuracies))


def run_experiment(data_format, n_states, trans_type):
    dataset = []
    for type in ['irish', 'slovak', 'welsh', 'french', 'german', 'austrian']:
        suffix = '.{}'.format(data_format)
        notes = load_notes_from_dir('dataset/{}/{}/'.format(data_format, type),
                                    maxlen=12, suffix=suffix)
        sigmas[type] = compute_sigma(notes)
        for song in notes:
            dataset.append([song, type])

    data = pd.DataFrame(dataset, columns=['notes', 'type'])

    # big_data = data[(data.type == 'irish') | (data.type == 'german')]
    # small_data = data[(data.type != 'irish') & (data.type != 'german')]

    accuracies = []
    mean, std = run_test(['welsh', 'slovak', 'french'], data,
                         n_states=n_states, trans_type=trans_type)
    return (mean, std)


if __name__ == '__main__':
    sigmas = {}
    for data_format in ['notes', 'contours', 'intervals']:
        for n_states in [2, 3, 4, 6]:
            for trans_type in ['a', 'b', 'c', 'd']:
                mean, std = run_experiment(data_format, n_states, trans_type)
                print('{},{},{},{},{}'.format(data_format, n_states,
                                              trans_type, mean, std))
