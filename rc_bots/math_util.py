__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2021/7/11 19:41'


def find_a_dissimilar(pos0, pos1, pos2):
    var1 = sum(list(map(lambda x: abs(x[0] - x[1]), zip(pos0, pos1))))
    var2 = sum(list(map(lambda x: abs(x[0] - x[1]), zip(pos0, pos2))))
    return pos1 if var1 > var2 else pos2


def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)