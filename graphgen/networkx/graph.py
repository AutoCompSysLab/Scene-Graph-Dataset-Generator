import networkx as nx
import matplotlib.pyplot as plt

g1 = nx.Graph()
g2 = nx.MultiDiGraph()

g1.add_node(1)
g1.add_node("a")
g1.add_nodes_from([2,7,3])

g1.add_edge(1, "a")
g1.add_edge(2,7)
g1.add_edges_from([(2,7), (1, "a")])

# G2 ------------------------------------
v_lst = range(10)

g2.add_nodes_from(v_lst)
g2.add_edge(0,1, name="test1")
g2.add_edge(0,2, name="test2")
g2.add_edge(1,2, name="test3")
g2.add_edge(4,2, name="test4")
g2.add_edge(6,5, name="test5")
g2.add_edge(9,3, name="test6")
g2.add_edge(2,1, name="test7")
g2.add_edge(3,2, name="test8")
g2.add_edge(4,5, name="test9")

# 각 node들의 위치를 생성하는 함수
pos = {}
for i in range(10):
    if i%2 == 0:
        pos_lst = [i,10 - i]
    else:
        pos_lst = [i, i]
    pos[i]=pos_lst

print(g2.nodes)
print(pos)
# edge attribute 지정 (여기서는 name으로)
labels = nx.get_edge_attributes(g2, "name")
# 만들어진 위치 생성 pos dict로 각 노드에 지정 (첫번째 인자 : 그래프, 두번째 position, 세번째 edge labels)
# https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pylab.draw_networkx_edge_labels.html
# draw_networkx_edge_labels does not support multiedges.
nx.draw(g2, pos, with_labels=True, connectionstyle='arc3, rad = 0.1')
edge_labels=labels
nx.draw_networkx_edge_labels(g2, pos, edge_labels=labels, verticalalignment='top')

plt.show()



