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
        self.Mat = np.zeros(shape=(self.n_vertices, len(self.edges) ), dtype=float)

        for index, item in enumerate(self.edges):
            edge_from, edge_to, bound, cost = item

            if edge_from not in marked_vertices:
                self.Mat[edge_from, index] += 1

            if edge_to not in marked_vertices:
                self.Mat[edge_to, index] -= 1
        self.Mat = self.Mat.astype(float)


    def gauss_transform(self):

        self.Mat_backup = np.copy(self.Mat)

        current_line = 0
        one_columns = []

        for column in range(self.Mat.shape[1]):
            # print('column:', column)

            # Find not zero element
            index = current_line

            while index < self.Mat.shape[0]:
                if self.Mat[index, column] != 0:
                    break;
                else:
                    index += 1
            # print(index)

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


            # print(self.Mat)
            current_line += 1


        for i in range(self.Mat.shape[0] - 1, -1, -1):
            if np.linalg.norm(self.Mat[i], ord=1) == 0:
                self.Mat = np.delete(self.Mat, i, 0)

        self.ones = one_columns

        # print("Ones:", one_columns)
        # print(self.Mat)


    def build_fundamental_solution(self):

        M1 = np.delete(self.Mat, self.ones, axis=1)
        print(self.Mat.shape[1] - len(self.ones))
        M2 = -np.identity(self.Mat.shape[1] - len(self.ones), dtype=float)

        self.fundamental = np.zeros(shape=(self.Mat.shape[1], self.Mat.shape[1] - len(self.ones)), dtype=float)

        ptr_m1 = 0
        ptr_m2 = 0

        for i in range(self.fundamental.shape[0]):
            if i in self.ones:
                self.fundamental[i] = M1[ptr_m1]
                ptr_m1 += 1
            else:
                self.fundamental[i] = M2[ptr_m2]
                ptr_m2 += 1

        # print(fundamental)
        # print(self.Mat_backup)
        # print(np.matrix(self.Mat_backup) * np.matrix(fundamental))


if __name__ == "__main__":
    g = Graph(4, [(0, 3, 1, 1), \
                  (0, 1, 2, 1), \
                  (3, 1, 0, 1), \
                  (3, 2, 1, 2), \
                  (1, 2, 1, 4)])
    g.build_equation_matrix([0, 2])
    g.gauss_transform()
    g.build_fundamental_solution()

