def travers_cost_matrix(cost, idx, jdx):
    """
    travers the cost matrix and yield the operation for transform from i,j to
    i-1, j-1
    operation jump is cost zero
    """
    while idx != 0 or jdx != 0:
        min = cost[idx - 1][jdx - 1]
        line = idx - 1
        column = jdx - 1
        """
        modification operation
        """
        operation = (idx + 1, jdx + 1, 'M')
        if cost[idx - 1][jdx] < min:
            """
            delete operation
            """
            min = cost[idx - 1][jdx]
            line = idx - 1
            column = jdx
            operation = (idx + 1, jdx + 1, 'D')
        if cost[idx][jdx - 1] < min:
            """
            apend operation
            """
            min = cost[idx][jdx - 1]
            line = idx
            column = jdx - 1
            operation = (idx + 1, jdx + 1, 'A')
        if cost[idx][jdx] == min:
            """
            this is cost zero start_word[idx] == end_word[jdx]
            J from jump
            """
            operation = (idx + 1, jdx + 1, 'J')
        yield operation
        idx = line
        jdx = column


def calculate_cost(start_word, end_word):
    """
    calculate the cost matrix
    cost(i,j) = cost(i-1, j-1) if  start_word[i] == end_word[j] ==> jump(zero cost)
                1 + min(cost(i-1, j-1), cost(i, j-1) , cost(i-1, j)
    """
    sw = len(start_word) + 1
    ew = len(end_word) + 1

    cost = [[0 for idx in range(ew)]
            for jdx in range(sw)]
    for idx in range(1, ew):
        cost[0][idx] = idx

    for idx in range(1, sw):
        cost[idx][0] = idx

    for jdx in range(1, ew):
        for idx in range(1, sw):
            """
            start_word[idx - 1] because start_word is 0 base index
            """
            if start_word[idx - 1] == end_word[jdx - 1]:
                cost[idx][jdx] = cost[idx - 1][jdx - 1]
            else:
                min = cost[idx - 1][jdx - 1]
                if cost[idx - 1][jdx] < min:
                    min = cost[idx - 1][jdx]
                if cost[idx][jdx - 1] < min:
                    min = cost[idx][jdx - 1]
                cost[idx][jdx] = 1 + min
    return cost

if __name__ == '__main__':
    with open('input.txt', 'r') as input, open('output.txt', 'r') as output:
        while True:
            line = input.readline().strip()
            if line == '':
                break
            start_word, end_word = line.split()
            cost = calculate_cost(start_word, end_word)
            trv = travers_cost_matrix(cost, len(start_word), len(end_word))
            try:
                solution = []
                while True:
                    step = trv.next()
                    if step[2] != 'J':
                        solution.append(step[2])
            except StopIteration:
                pass
            solution.reverse()
            expected_result = output.readline().strip()
            assert(expected_result == str(solution))
