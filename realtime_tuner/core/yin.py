import numpy as np


def difference_function(signal):

    N = len(signal)

    d = np.zeros(N)

    for tau in range(1, N):

        diff = signal[:-tau] - signal[tau:]

        d[tau] = np.sum(diff**2)

    return d

def cumulative_mean_normalized(d):

    cmnd = np.zeros_like(d)

    cmnd[0] = 1

    running_sum = 0

    for tau in range(1, len(d)):

        running_sum += d[tau]

        cmnd[tau] = d[tau] * tau / running_sum

    return cmnd

def absolute_threshold(cmnd, threshold=0.1):

    for tau in range(2, len(cmnd)):

        if cmnd[tau] < threshold:

            while tau+1 < len(cmnd) and cmnd[tau+1] < cmnd[tau]:
                tau += 1

            return tau

    return None


def parabolic_interpolation(cmnd, tau):

    if tau < 1 or tau + 1 >= len(cmnd):
        return tau

    s0 = cmnd[tau - 1]
    s1 = cmnd[tau]
    s2 = cmnd[tau + 1]

    denom = (2 * s1 - s2 - s0)

    if denom == 0:
        return tau

    return tau + (s2 - s0) / (2 * denom)