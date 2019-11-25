from statistics import mean, median, stdev, variance


def generate_statistics(data):
    data_mean = "NULL"
    data_median = "NULL"
    data_stdev = "NULL"
    data_variance = "NULL"

    if len(data) >= 1:
        data_mean = mean(data)
        data_median = median(data)

    if len(data) >= 2:
        data_stdev = stdev(data, data_mean)
        data_variance = variance(data, data_mean)

    return "{},{},{},{}".format(data_mean, data_median, data_stdev, data_variance)
