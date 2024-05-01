import sys
import os
import pandas as pd
import ast
import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import numpy as np

evolution = sys.argv[1]

class Graph:
    nodes = []
    adj_list = {}              #this is the adjacency list as dictionary
    edges = []                  #list of tuples (u,v,w) where (u,v) is an edge of weight w
    G = nx.DiGraph()
    def __init__(self):
        print ("initializing a graph")
    
    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            self.adj_list[node]=[]
            #print (self.nodes)
        else:
            print ("The node is already existing.")
        
    def add_edge(self, edge):           #the edge is a tuple (u,v)
        u = edge[0]
        v = edge[1]
        w = edge[2]
        self.edges.append(edge)
        
    
    def print_graph(self):
        print (self.nodes)
        print (self.adj_list)
        print (self.edges)
    
    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)
    
    def add_edges(self,list_of_edges):
        for edge in list_of_edges:
            self.add_edge(edge)
            
    def delete_edge(self, edge):
        u = edge[0]
        v = edge[1]
        self.adj_list[u].remove[v]
    
    def delete_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            for key, value in self.adj_list.items():
                if key == node:                         #
                    del self.adj_list[node]
                if node in value:
                    value.remove(node)
                    
    def delete_nodes(self, nodes):
        for node in nodes:
            delete_node(self, node)
    
    def delete_edges(self, edges):
        for edge in edges:
            delete_edge(self, edge)
            
    def add_dict(self, nodes, dictionary, weight):
        self.nodes.extend(nodes)
        self.nodes.reverse()
        for key, values in dictionary.items():
            if key not in self.nodes:
                self.nodes.append(key)
            self.adj_list[key]=values
            
            for value in values:
                if value not in self.nodes:
                    
                    self.nodes.append(value)
                    self.adj_list[value]=[]
            
            i=0
            for i in range(0, len(values)):
                if values[i] != 'root':
                    self.add_edge((values[i], key, weight[key][i]))             #adding edges
            
        self.nodes.remove("root")
        
        
    def generate_random_color(self):
        r=random.randint(0, 255)
        g=random.randint(0, 255)
        b=random.randint(0, 255)
        rgb_normalized = (r/255, g/255, b/255)
        return rgb_normalized
    
    def generate_n_random_colors(self, n):
        colors=[]
        for _ in range(n):
            color = self.generate_random_color()
            colors.append(color)
        return colors
        
            
        
    def draw_graph(self, figure, lineage_groups):
        rgb_colors=self.generate_n_random_colors(len(lineage_groups))
        print (len(lineage_groups))
        nodes_by_colors={}
        i=0
        for key, value in lineage_groups.items():
            nodes_by_colors[rgb_colors[i]] = value
            i=i+1
        
        
        colors_by_nodes=[]
        colors_list={}
        for key, value in nodes_by_colors.items():
            for item in value:
                colors_list[item]=key
        
            
        for node in self.nodes:
            colors_by_nodes.append(colors_list[node])
        
        self.G.add_nodes_from(self.nodes)
        
        plt.figure(figsize=(20,20))
        self.G.add_weighted_edges_from(self.edges)
        #pos = nx.planar_layout(self.G)          #seed=#of nodes +1
        pos = graphviz_layout(self.G, prog='dot')
        
        nx.draw_networkx_nodes(self.G, pos, nodelist=self.nodes, node_color=colors_by_nodes)
        nx.draw_networkx_labels(self.G, pos, font_size=8)
        nx.draw_networkx_edges(self.G, pos, edgelist=self.edges, arrows=True, arrowstyle='-|>')
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels, label_pos=0.5, font_size=8)
        
        plt.show()
        plt.savefig(figure)
        
    
    def get_adj_matrix(self, adj_matrix_file):
        df = pd.DataFrame(0, index=self.nodes, columns=self.nodes)
        for u, v, w in self.edges:
            df.loc[u, v] = w
        #print (df)
        df.to_csv(adj_matrix_file)
        return