import numpy as np


class Graph:

    # Vertices is ints from 0 to n_vertices - 1
    # edge = [from, to, bound, cost]
    def __init__(self, n_vertices, edges):

        self.arr_from = [[] for i in range(n_vertices)]
        self.arr_to   = [[] for i in range(n_vertices)]
        self.n_vertices = n_vertices

        for edge_from, edge_to, bound, cost in edges:
            self.arr_from[edge_from].append([edge_to, bound, cost])
            self.arr_to[edge_to].append([edge_from, bound, cost])

        self.edges = np.copy(np.array(edges))


    def build_equation_matrix(self, marked_vertices):
        self.Mat = np.zeros(shape=(self.n_vertices, len(self.edges) ))

        for index, item in enumerate(self.edges):
            edge_from, edge_to, bound, cost = item

            if edge_from not in marked_vertices:
                self.Mat[edge_from, index] += 1

            if edge_to not in marked_vertices:
                self.Mat[edge_to, index] -= 1

        print(self.Mat)


    def gauss_transform(self):

        current_line = 0
        one_columns = []

        for column in range(self.Mat.shape[1]):
            print('column:', column)

            # Find not zero element
            index = current_line

            while index < self.Mat.shape[0]:
                if self.Mat[index, column] != 0:
                    break;
                else:
                    index += 1
            print(index)

            if index == self.Mat.shape[0]:
                continue

            # swap lines
            for tmp_column in range(self.Mat.shape[1]):
                self.Mat[current_line, tmp_column], self.Mat[index, tmp_column] = \
                    self.Mat[index, tmp_column], self.Mat[current_line, tmp_column]

            current_element = self.Mat[current_line, column]

            for tmp_column in range(column, self.Mat.shape[1]):
                self.Mat[current_line, tmp_column] /= current_element

            for tmp_line in range(0, self.Mat.shape[0]):
                if tmp_line != current_line:
                    self.Mat[tmp_line] -= \
                        self.Mat[current_line] * self.Mat[tmp_line, column]

            one_columns.append(column)


            print(self.Mat)
            current_line += 1

        print("Ones:", one_columns)



if __name__ == "__main__":
    g = Graph(4, [(0, 3, 1, 1), \
                  (0, 1, 2, 1), \
                  (3, 1, 0, 1), \
                  (3, 2, 1, 2), \
                  (1, 2, 1, 4)])
    g.build_equation_matrix([0, 2])
    g.Mat = np.array( [  [1, -1,   1,  0],
                         [0,  0,  -1,  1],
                         [1,  -1,  0,  1]
                      ]   )
    g.gauss_transform()

