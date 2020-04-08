import math
import scipy.stats
import matplotlib.pyplot as plt
import numpy
import os


confidence = 0.95


def s_mean_value(samples):
    mean = 0
    for sample in samples:
        mean += sample
    mean /= len(samples)
    return mean


def s_variance(samples):
    mean = s_mean_value(samples)
    variance = 0
    for sample in samples:
        variance += (sample - mean)**2
    variance /= (len(samples) - 1)
    return variance


def s_lorenz_curve_gap(samples):
    mean = s_mean_value(samples)
    gap = 0
    for sample in samples:
        gap += abs(sample - mean)
    gap /= len(samples)
    gap /= 2*mean
    return gap


def s_percentile(samples, percentile):
    sorted_samples = samples[:]
    sorted_samples.sort()
    return sorted_samples[math.ceil(len(samples)*percentile) - 1]


def normal_dist_percentile(p):
    # percentile = 4.9*p*(p**0.14 - (1-p)**0.14)
    percentile = scipy.stats.norm.ppf(p)
    return percentile


def s_mean_confidence_interval(samples):
    mean = s_mean_value(samples)
    variance = s_variance(samples)
    percentile = normal_dist_percentile(1-(1-confidence)/2)
    radius = percentile * math.sqrt(variance/len(samples))
    return [mean-radius, mean+radius]


def sample_autocorrelation(samples, lag):
    mean = s_mean_value(samples)
    variance = s_variance(samples)
    n = len(samples)
    value = 0

    for i in range(0, n-lag):
        value += ((samples[i]-mean)*(samples[i+lag]-mean))

    if value == 0:
        return 0

    value /= n
    value /= variance

    return value


def plot_correlogram(samples, scenario, name):
    x = range(1, len(samples))
    y = []

    for lag in x:
        y.append(sample_autocorrelation(samples, lag))

    plt.scatter(x, y, s=5, label="autocorrelation")

    # plot confidence intervals
    percentile = normal_dist_percentile(1-(1-confidence)/2)

    cix = numpy.arange(0.0, len(samples), 0.1)
    ly = []
    hy = []
    for i in cix:
        ly.append(-percentile / math.sqrt(len(samples)))
        hy.append(percentile / math.sqrt(len(samples)))

    plt.plot(cix, ly, label="confidence intervals' lower boundary")
    plt.plot(cix, hy, label="confidence intervals' upper boundary")

    # plot graph's decorations
    plt.grid(True)
    plt.xlabel("Lag")
    plt.ylabel("Autocorrelation")
    plt.title(scenario + ":" + name)

    if not os.path.exists("correlograms\\" + scenario.split("\\")[-1]):
        os.makedirs("correlograms\\" + scenario.split("\\")[-1])

    plt.savefig("correlograms\\" + scenario.split("\\")[-1] + "\\" + name + ".png")
    plt.close()
