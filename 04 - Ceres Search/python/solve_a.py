from loader import input_as_strings

def mark(input, board, points):
    for [i, j] in points:
        board[i][j] = input[i][j]
    return board

if __name__ == "__main__":
    input = input_as_strings()

    target = "XMAS"
    max_i = len(input) - 1
    max_j = len(input[0]) - 1

    points = []
    for i in range(0, max_i + 1):
        line = []
        for j in range(0, max_j):
            line.append(".")
        points.append(line)

    start_points = []
    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            if input[i][j] == target[0]:
                start_points.append([i, j])

    matches = 0
    for [i,j] in start_points:
        if j + len(target) - 1 <= max_j:
            i_s = [ i for _ in range(0, len(target))]
            j_s = range(j, j + len(target))
            forward = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(forward) == len(target)
            if forward == target:
                matches = matches + 1
                points = mark(input, points, zip(i_s, j_s))
        if j - len(target) + 1 >= 0:
            i_s = [ i for _ in range(0, len(target))]
            j_s = range(j, j - len(target), -1)
            backward = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(backward) == len(target)
            if backward == target:
                matches = matches + 1
                points = mark(input, points, zip(i_s, j_s))
        if i + len(target) - 1 <= max_i:
            i_s = range(i, i + len(target))
            j_s = [ j for _ in range(0, len(target))]
            down = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(down) == len(target)
            if down == target:
                matches = matches + 1
                points = mark(input, points, zip(i_s, j_s))
        if i - len(target) + 1 >= 0:
            i_s = range(i, i - len(target), -1)
            j_s = [j for _ in range(0, len(target))]
            up = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(up) == len(target)
            if up == target:
                matches = matches + 1
                points = mark(input, points, zip(i_s, j_s))
        if i + len(target) - 1 <= max_i and j + len(target) - 1 <= max_j:
            i_s = range(i, i + len(target))
            j_s = range(j, j + len(target))
            down_right = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(down_right) == len(target)
            if down_right == target:
                matches = matches + 1
                points = mark(input, points, zip(i_s, j_s))
        if i + len(target) - 1 <= max_i and j - len(target) + 1 >= 0:
            i_s = range(i, i + len(target))
            j_s = range(j, j - len(target), -1)
            down_left = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(down_left) == len(target)
            if down_left == target:
                matches = matches + 1
                points = mark(input, points, zip(i_s, j_s))
        if i - len(target) + 1 >= 0 and j + len(target) - 1 <= max_j:
            i_s = range(i, i - len(target), -1)
            j_s = range(j, j + len(target))
            up_right = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(up_right) == len(target)
            if up_right == target:
                matches = matches + 1
                points = mark(input, points, zip(i_s, j_s))
        if i - len(target) + 1 >= 0 and j - len(target) + 1 >= 0:
            i_s = range(i, i - len(target), -1)
            j_s = range(j, j - len(target), -1)
            up_left = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(up_left) == len(target)
            if up_left == target:
                matches = matches + 1
                points = mark(input, points, zip(i_s, j_s))

    for line in points:
        print("".join(line))

    print(matches)