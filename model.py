from pomegranate import *
import numpy as np


def hmm_model(n_states, sigma, trans_type=None):
    dists = []
    L = len(sigma)
    for i in range(n_states):
        rand = np.random.uniform(0.0, 1.0, size=(L,))
        rand /= rand.sum()
        d = {}
        for i, l in enumerate(sigma):
            d[l] = rand[i]

        dists.append(DiscreteDistribution(d))

    trans_mat = np.random.uniform(0.0, 1.0, size=(n_states, n_states))
    if trans_type == 'b':
        trans_mat = np.triu(trans_mat)
    elif trans_type == 'c':
        trans_mat = np.triu(trans_mat)
        trans_mat[-1][0] = np.random.uniform()
    elif trans_type == 'a':
        trans_mat = np.triu(trans_mat)
        trans_mat = np.tril(trans_mat, 1)

    trans_mat = trans_mat / trans_mat.sum(axis=1)[:, np.newaxis]
    # print(trans_mat)

    starts = np.array([1.0] + [0.0]*(n_states - 1))
    ends = np.array([0.0]*(n_states - 1) + [0.1])
    model = HiddenMarkovModel.from_matrix(trans_mat, dists, starts, ends)
    model.bake()
    return model
