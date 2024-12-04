from loader import input_as_strings

def mark(input, board, points):
    for [a, b] in points:
        if input[a][b] == "A":
            board[a][b] = board[a][b] + 1
    return board

if __name__ == "__main__":
    input = input_as_strings()

    target = "MAS"
    max_i = len(input) - 1
    max_j = len(input[0]) - 1

    points = []
    for i in range(0, max_i + 1):
        line = []
        for j in range(0, max_j):
            line.append(0)
        points.append(line)

    start_points = []
    for i in range(0, len(input)):
        for j in range(0, len(input[i])):
            if input[i][j] == target[0]:
                start_points.append([i, j])

    for [i,j] in start_points:
        if i + len(target) - 1 <= max_i and j + len(target) - 1 <= max_j:
            i_s = range(i, i + len(target))
            j_s = range(j, j + len(target))
            down_right = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(down_right) == len(target)
            if down_right == target:
                points = mark(input, points, zip(i_s, j_s))
        if i + len(target) - 1 <= max_i and j - len(target) + 1 >= 0:
            i_s = range(i, i + len(target))
            j_s = range(j, j - len(target), -1)
            down_left = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(down_left) == len(target)
            if down_left == target:
                points = mark(input, points, zip(i_s, j_s))
        if i - len(target) + 1 >= 0 and j + len(target) - 1 <= max_j:
            i_s = range(i, i - len(target), -1)
            j_s = range(j, j + len(target))
            up_right = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(up_right) == len(target)
            if up_right == target:
                points = mark(input, points, zip(i_s, j_s))
        if i - len(target) + 1 >= 0 and j - len(target) + 1 >= 0:
            i_s = range(i, i - len(target), -1)
            j_s = range(j, j - len(target), -1)
            up_left = "".join(input[x][y] for [x,y] in zip(i_s, j_s))
            assert len(up_left) == len(target)
            if up_left == target:
                points = mark(input, points, zip(i_s, j_s))

    # for line in points:
    #     print("".join([str(x) for x in line]))

    xmas_count = 0
    for line in points:
        for elem in line:
            if elem > 1:
                xmas_count += 1

    print(xmas_count)