import unittest

graph_1 = [['s', 'a', 14],['s', 'b', 7],['s', 'c', 9],['a', 'c', 2],['c', 'b', 10],['b', 'd', 15], ['c', 'd', 11],['a', 't', 9],['d', 't', 6]]
graph_2 = [['s', 'a', 10],['s', 'd', 3],['a', 'd', 6],['a', 'b', 6],['a', 'c', 2],['d', 'c', 7], ['d', 'e', 1],['e', 'c', 4],['b', 'c', 8],['b', 'e', 10],['b', 't', 9],['e', 't', 20]]
graph_3 = [['s', 'a', 2],['s', 'b', 4],['b', 'd', 6],['a', 't', 7],['a', 'f', 8],['f', 't', 1], ['d', 't', 1]]

def occurances(key: str, LoL: list) -> int:
  x = 0
  for L in LoL:
    x += L.count(key)
  return x   

def stcut(graph: list, L: list) -> list:
    M = []
    for edge in graph:
      if edge[0] in L:
        if not(edge[1] in L):
          M = M + [edge]
      if edge[1] in L:
        if not(edge[0] in L):
          M = M + [edge]
    return M

def shortestpath(graph: list) -> list:
    U = ['s']
    widths = []
    active = []

    while not('t' in U):
      current_cut = stcut(graph,U)

      # Find cheapest path
      min_num = current_cut[0][2]
      for L in current_cut:
        if L[2] > 0:
          if L[2] < min_num:
            min_num = L[2]
      widths = widths + [min_num]

      # Add new edge to U
      for L in current_cut:
        if L[2] == min_num:
          if not(L[0] in U):
            U = U + [L[0]]
          if not(L[1] in U):
            U = U + [L[1]]
          active = active + [L[0:2]]

      # Update paths with width
      for L in current_cut:
        graph[graph.index(L)][2] = graph[graph.index(L)][2] - min_num
    
    # Find shortest path
    shortest = ['s']
    while not('t' in shortest):
      x = 0
      while x < len(active):
        if active[x][0] == shortest[-1]:
          if active[x][1] == 't':
            shortest = shortest + ['t']
            active.pop(x)
          elif occurances(active[x][1], active) >= 2:
            shortest = shortest + [active[x][1]]
            active.pop(x)
        elif active[x][1] == shortest[-1]:
          if active[x][0] == 't':
            shortest = shortest + ['t']
            active.pop(x)
          elif occurances(active[x][0], active) >= 2:
            shortest = shortest + [active[x][0]]
            active.pop(x)
        x += 1
    return [shortest, sum(widths)]

class test(unittest.TestCase):
    def test_stcut_1_s(self):
        actual = stcut([['s', 'a', 14],['s', 'b', 7],['s', 'c', 9],['a', 'c', 2],['c', 'b', 10],['b', 'd', 15], ['c', 'd', 11],['a', 't', 9],['d', 't', 6]],['s'])
        expected = [['s', 'a', 14],['s', 'b', 7],['s', 'c', 9]]
        self.assertEqual(actual, expected)

    def test_stcut_1_sa(self):
        actual = stcut([['s', 'a', 14],['s', 'b', 7],['s', 'c', 9],['a', 'c', 2],['c', 'b', 10],['b', 'd', 15], ['c', 'd', 11],['a', 't', 9],['d', 't', 6]],['s','a'])
        expected = [['s', 'b', 7],['s', 'c', 9],['a', 'c', 2],['a', 't', 9]]
        self.assertEqual(actual, expected)

    def test_stcut_2_sd(self):
        actual = stcut([['s', 'a', 10],['s', 'd', 3],['a', 'd', 6],['a', 'b', 6],['a', 'c', 2],['d', 'c', 7], ['d', 'e', 1],['e', 'c', 4],['b', 'c', 8],['b', 'e', 10],['b', 't', 9],['e', 't', 20]],['s','d'])
        expected = [['s', 'a', 10], ['a', 'd', 6], ['d', 'c', 7], ['d', 'e', 1]]
        self.assertEqual(actual, expected)

    def test_path_1(self):
        actual = shortestpath([['s', 'a', 14],['s', 'b', 7],['s', 'c', 9],['a', 'c', 2],['c', 'b', 10],['b', 'd', 15], ['c', 'd', 11],['a', 't', 9],['d', 't', 6]])
        expected = [['s','c','a','t'], 20]
        self.assertEqual(actual, expected)

    def test_path_2(self):
        actual = shortestpath([['s', 'a', 10],['s', 'd', 3],['a', 'd', 6],['a', 'b', 6],['a', 'c', 2],['d', 'c', 7], ['d', 'e', 1],['e', 'c', 4],['b', 'c', 8],['b', 'e', 10],['b', 't', 9],['e', 't', 20]])
        expected = [['s', 'd', 'e', 'b', 't'], 23]
        self.assertEqual(actual, expected)
    
    def test_patj_3(self):
       actual = shortestpath([['s', 'a', 2],['s', 'b', 4],['b', 'd', 6],['a', 't', 7],['a', 'f', 8],['f', 't', 1], ['d', 't', 1]])
       expected = [['s', 'a', 't'], 9]
       self.assertEqual(actual, expected)

print(unittest.main())