import importlib
import gdown
import numpy as np


def _load_data(data_id):
    local_file = "%s.npz" % data_id
    gdown.download(id=data_id, output=local_file, quiet=True)
    return np.load(local_file)['arr_0']


def run(submission_id, test_id, data_id, precision):
    module = importlib.import_module(submission_id)
    func = getattr(module, test_id)
    data = _load_data(data_id)

    for i in range(len(data)):
        np.testing.assert_almost_equal(func(*data[i, :-1]), data[i, -1],
                                       decimal=precision)


def gen(submission_id, test_id, seed, num_data, prefix, low, high, hook_f=None):
    module = importlib.import_module(submission_id)
    func = getattr(module, test_id)

    input_dim = len(low)
    rng = np.random.default_rng(seed=seed)
    data = np.zeros((num_data, input_dim + 1))
    data[:, :input_dim] = rng.uniform(low=low, high=high,
                                      size=(num_data, input_dim))

    # apply hook if specified
    if hook_f is not None:
        data[:, :-1] = hook_f(data[:, :-1])

    # apply the function
    for i in range(num_data):
        data[i, -1] = func(*data[i, :-1])

    np.savez('%s_%016d_%04d.npz' % (prefix, seed, num_data), data)
    return data
