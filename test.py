

def countNegatives(grid: list[list[int]]) -> int:
    return sum(i < 0 for row in grid for i in row)
    # from more_itertools import flatten, ilen
    # return ilen(filter(lambda i : i < 0, flatten(grid)))

if __name__ == '__main__':
    print(countNegatives([[1, 2], [-1, 4]]))