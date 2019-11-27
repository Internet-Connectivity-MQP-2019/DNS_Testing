from statistics import mean, median, stdev, variance


def generate_statistics(data):
    data_mean = "NULL"
    data_median = "NULL"
    data_stdev = "NULL"
    data_variance = "NULL"

    if len(data) >= 1:
        data_mean = "{:.2f}".format(mean(data))
        data_median = "{:.2f}".format(median(data))

    if len(data) >= 2:
        data_stdev = "{:.2f}".format(stdev(data))
        data_variance = "{:.2f}".format(variance(data))

    return "{},{},{},{}".format(data_mean, data_median, data_stdev, data_variance)


def calculate_coefficient_of_variation(mean, stdev):
    return stdev/mean
