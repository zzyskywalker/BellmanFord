复现了bellman-ford的基本算法
首先是构造有向图，找出了其点集、边集和邻接矩阵
接着复现bellman ford最短路径算法bellman_ford()，输入为源节点,返回值为disntance：表示最短距离  pre 表示前置节点
然后使用shortest_path()根据pr前置节点来复原最短路径

然后是返回多条最短路径的bellman_ford_multiple()，返回值为dist，表示最短距离，pr表示前置节点。
然后使用shortest_paths()根据pr前置节点来复原最短路径