'''
Description: 
Author:zzy  
Date: 2021-10-30 12:11:42
LastEditTime: 2021-11-01 18:06:26
LastEditors:  
'''
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy

import sys   
sys.setrecursionlimit(4000) #递归深度设置为十万

class Dir_Graph():
    def __init__(self,file_path):
        pd_data=pd.read_csv(file_path,index_col="id")#读取csv文件
        
        #构建点集
        node_list1=pd_data["source"].to_list()
        node_list2=pd_data["target"].to_list()
        node_set1=set(node_list1)
        node_set2=set(node_list2)
        self.node_set=node_set1|node_set2
        nodes_num=len(self.node_set)
        #print(len(node_set))
        
        #构建边集
        self.edge_list=[(source,target,cost) for source,target,cost in zip(pd_data["source"].to_list(),pd_data["target"].to_list(),pd_data["cost"].to_list())]

        #构建邻接矩阵
        self.adjacency_matrix=[[float("Inf") for n in range(nodes_num)] for n in range(nodes_num)]
        for s,d,w in self.edge_list: #有边的赋值为权重
            self.adjacency_matrix[s][d]=w   
        for i in range(nodes_num):
            self.adjacency_matrix[i][i]=0   #对角线设为0
        #print("邻接矩阵",adjacency_matrix)
        
        
class Bellman_ford():
    def __init__(self,node_set,edge_list,adjacency_matrix):
        
        self.node_set=node_set
        self.edge_list=edge_list
        self.adjacency_matrix=adjacency_matrix
        self.src=None
        self.node_num=len(node_set)
        self.dist=None
        self.pr=None
        
        
    #最初的bellman_ford算法，求单条最短路径，输入为源节点,返回值为disntance：表示最短距离  pre 表示前置节点
    def bellman_ford(self,src):
        #初始化
        self.src=src
        
        dist=self.adjacency_matrix[self.src]
        pr=[src for i in range(self.node_num)]
        #print(dist)
        #print(pr)
        for k in range(self.node_num):#多走一轮,看看是否相同
            dist_tem=copy.deepcopy(dist)#deep copy 复制出来的量需要临时修改不能影响原先的值
            
            for u in self.node_set:
                tem_sum=[]
                for v in self.node_set:#计算所有u+w
                    tem_sum.append(dist[v]+self.adjacency_matrix[v][u])
                    
                #print("当前轮次",k,"当前节点",u,tem_sum)

                dist_min=min(tem_sum)
                dist_tem[u]=dist_min
                if tem_sum.index(dist_min)!=u: #防止自身的循环，把前置节点设为自己
                    pr[u]=tem_sum.index(dist_min)
        
            if  k == self.node_num-2 and dist_tem == dist:
                print("单路径bellman ford算法最后两轮结果相同，无负圈")
        
            dist=copy.deepcopy(dist_tem)
            #print("轮次",k,dist)
        self.dist=dist
        self.pr=pr  
        return dist,pr

#根据pre前置节点找出路径 ，输入为目的节点，返回值为路径，也会打印出路径
    def shortest_path(self,destination):
        shortest_path_list_temp=[]
        
        def recursion_path(node,pre):#递归函数，用来构建最短路径
            if node == self.src or pre[node] == self.src:
                shortest_path_list_temp.append(self.src)
                return
            shortest_path_list_temp.append(pre[node])
            return recursion_path(pre[node],pre)
        
        recursion_path(destination,self.pr)
        print(shortest_path_list_temp)
        shortest_path_list_temp.reverse()
        shortest_path_list_temp.append(destination)
        
        print(self.src,"->",destination,"距离:",self.dist[destination],"   路径:",shortest_path_list_temp)
        return shortest_path_list_temp 
    
    
    #多路径贝尔曼算法
    def bellman_ford_multiple(self,src):
        
        #初始化
        self.src=src
        dist=self.adjacency_matrix[self.src]
        pr=[[src] for i in range(self.node_num)]  #储存多个前置节点。
        
        for k in range(self.node_num):#多走一轮,看看是否相同
            dist_tem=copy.deepcopy(dist)#deep copy 复制出来的量需要临时修改不能影响原先的值
            
            for u in self.node_set:
                tem_sum=[]
                for v in self.node_set:#计算所有u+w
                    tem_sum.append(dist[v]+self.adjacency_matrix[v][u])
                    
                #print("当前轮次",k,"当前节点",u,tem_sum)

                dist_min=min(tem_sum)
                dist_tem[u]=dist_min
                
                index = [i for i,temp in enumerate(tem_sum) if temp== dist_min and i!=u]#当有多个相同长度的前置节点的时候，找出来,并且不能是自己
                
                pr[u]=index
        
            if  k == self.node_num-2 and dist_tem == dist:
                print("多路径bellman ford算法最后两轮结果相同，无负圈")
        
            dist=copy.deepcopy(dist_tem)
            #print("轮次",k,dist)
        pr[src]=[src]
        self.dist=dist
        self.pr=pr  
        return dist,pr
    
    #根据pre前置节点找出路径 ，输入为目的节点，找出多条路径
    def shortest_paths(self,destination):
        # 从pr中找出路径的代码参考这里  https://blog.csdn.net/u013615687/article/details/69062803
        def getpaths(start,index,pre):
            childPaths=[[]]
            midPaths=[[]]
            if start != index:
                for i in range(len(pre[index])):
                    childPaths = getpaths(start,pre[index][i],pre)
                    for j in range(len(childPaths)):
                        childPaths[j].append(index)
                        
                    if midPaths ==[[]]:
                        midPaths=copy.deepcopy(childPaths)
                    else:
                        for h in range(len(childPaths)):
                            midPaths.append(childPaths[h])
            else:
                midPaths=[[start]]                
            return midPaths
        
        paths=getpaths(self.src,destination,self.pr)

        for i in paths:
            print(self.src,"->",destination,"距离:",self.dist[destination],"   路径:",i)
        return paths   

if __name__== "__main__":
    G=Dir_Graph("graph generated.csv")
    """ print(G.node_set)
    print(G.edge_list)
    print(G.adjacency_matrix) """

    B=Bellman_ford(G.node_set,G.edge_list,G.adjacency_matrix)
    
    #一条最短路径
    distance,pre=B.bellman_ford(0)
    path=B.shortest_path(6)
    
    #多条最短路径
    distance,pre=B.bellman_ford_multiple(0)
    paths=B.shortest_paths(6)
    