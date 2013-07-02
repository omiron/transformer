

class CostMatrix(object):
    def __init__(self, cost, len_start_word, len_second_word):
        self.cost = cost
        #Observation: the cost is max between lenght start word, lenght second word
        self.max_cost = max(len_start_word, len_second_word)

    def get_cost_operation(self, idx, jdx):
        if idx < 0 or jdx < 0:
            return self.max_cost
        else:
            return self.cost[idx][jdx]


def travers_cost_matrix(cost, idx, jdx):
    """
    travers the cost matrix and yield the operation for transform from i,j to
    i-1, j-1
    operation jump is cost zero
    """
    while idx != 0 or jdx != 0:
        min = cost.get_cost_operation(idx - 1, jdx - 1)
        line = idx - 1
        column = jdx - 1
        """
        move operation
        """
        operation = (idx + 1, jdx + 1, 'M')
        if cost.get_cost_operation(idx - 1, jdx) < min:
            """
            delete operation
            """
            min = cost.get_cost_operation(idx - 1, jdx)
            line = idx - 1
            column = jdx
            operation = (idx + 1, jdx + 1, 'D')
        if cost.get_cost_operation(idx, jdx - 1) < min:
            """
            insert operation
            """
            min = cost.get_cost_operation(idx, jdx - 1)
            line = idx
            column = jdx - 1
            operation = (idx + 1, jdx + 1, 'I')
        if cost.get_cost_operation(idx, jdx) == min:
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

    cost = [[0 for idx in range(ew)] for jdx in range(sw)]

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
    with open('input.txt', 'r') as input, open('output.txt', 'w') as output:
        while True:
            line = input.readline().strip()
            if line == '':
                break
            start_word, end_word = line.split()
            cost = CostMatrix(calculate_cost(start_word, end_word),
                              len(start_word), len(end_word))
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
            output.write("{0}\n".format(str(solution)))
