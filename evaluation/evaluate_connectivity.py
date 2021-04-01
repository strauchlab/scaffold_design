import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns
import math
import numpy as np
import numpy as numpy
import pandas as pd
import networkx as nx
import math as math
from rosetta.core.scoring.sasa import SasaCalc
#from multiprocessing import Pool
from pyrosetta import *
from rosetta import *
print "Init Rosetta and Reading Rosetta Database, be patient"
#-constant_seed
init(options="-beta_nov15 -ex1 -ex2aro -relax:constrain_relax_to_start_coords -relax:coord_constrain_sidechains -relax:ramp_constraints false  -detect_disulf True -mute all ", #-ex2
             extra_options="", 
             set_logging_handler=True)

indir = './'

""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
"""

class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary Gwill be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


    def vertex_degree(self, vertex):
        """ The degree of a vertex is the number of edges connecting
            it, i.e. the number of adjacent vertices. Loops are counted 
            double, i.e. every occurence of vertex in the list 
            of adjacent vertices. """ 
        adj_vertices =  self.__graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex)
        return degree
    
    def density(self):
        """ method to calculate the density of a graph """
        g = self.__graph_dict
        V = len(g.keys())
        E = len(self.edges())
        return 2.0 * E / (V *(V - 1))

    def is_connected(self, 
                     vertices_encountered = None, 
                     start_vertex=None):
        """ determines if the graph is connected """
        if vertices_encountered is None:
            vertices_encountered = set()
        gdict = self.__graph_dict        
        vertices = list(gdict.keys()) # "list" necessary in Python 3 
        if not start_vertex:
            # chosse a vertex from graph as a starting point
            start_vertex = vertices[0]
        vertices_encountered.add(start_vertex)
        if len(vertices_encountered) != len(vertices):
            for vertex in gdict[start_vertex]:
                if vertex not in vertices_encountered:
                    if self.is_connected(vertices_encountered, vertex):
                        return True
        else:
            return True
        return False
    
    def diameter(self):
        """ calculates the diameter of the graph """
        
        v = self.vertices() 
        pairs = [ (v[i],v[j]) for i in range(len(v)-1) for j in range(i+1, len(v))]
        smallest_paths = []
        for (s,e) in pairs:
            paths = self.find_all_paths(s,e)
            smallest = sorted(paths, key=len)[0]
            smallest_paths.append(smallest)

        smallest_paths.sort(key=len)

        # longest path is at the end of list, 
        # i.e. diameter corresponds to the length of this path
        diameter = len(smallest_paths[-1]) - 1
        return diameter

    
    @staticmethod
    def is_degree_sequence(sequence):
        """ Method returns True, if the sequence "sequence" is a 
            degree sequence, i.e. a non-increasing sequence. 
            Otherwise False is returned.
        """
        # check if the sequence sequence is non-increasing:
        return all( x>=y for x, y in zip(sequence, sequence[1:]))
    
    
    def degree_sequence(self):
        """ calculates the degree sequence """
        seq = []
        for vertex in self.__graph_dict:
            seq.append(self.vertex_degree(vertex))
        seq.sort(reverse=True)
        return tuple(seq)
    
    def find_isolated_vertices(self):
        """ returns a list of isolated vertices. """
        graph = self.__graph_dict
        isolated = []
        for vertex in graph:
            print(isolated, vertex)
            if not graph[vertex]:
                isolated += [vertex]
        return isolated  
    
    def delta(self):
        """ the minimum degree of the vertices """
        min = 100000000
        for vertex in self.__graph_dict:
            vertex_degree = self.vertex_degree(vertex)
            if vertex_degree < min:
                min = vertex_degree
        return min
        
    def Delta(self):
        """ the maximum degree of the vertices """
        max = 0
        for vertex in self.__graph_dict:
            vertex_degree = self.vertex_degree(vertex)
            if vertex_degree > max:
                max = vertex_degree
        return max
    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        graph = self.__graph_dict 
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex, 
                                                     end_vertex, 
                                                     path)
                for p in extended_paths: 
                    paths.append(p)
        return paths
    
    @staticmethod
    def erdoes_gallai(dsequence):
        """ Checks if the condition of the Erdoes-Gallai inequality 
            is fullfilled 
        """
        if sum(dsequence) % 2:
            # sum of sequence is odd
            return False
        if Graph.is_degree_sequence(dsequence):
            for k in range(1,len(dsequence) + 1):
                left = sum(dsequence[:k])
                right =  k * (k-1) + sum([min(x,k) for x in dsequence[k:]])
                if left > right:
                    return False
        else:
            # sequence is increasing
            return False
        return True
    
### start main code ###
pdbs = []

for f in os.listdir(indir):
    if '.pdb' in str(f) :
        pdbs.append( f)

print "reading in",len(pdbs),"pdbs..."

design_scores = {}
count = 0
for pdb in pdbs: 
    if count > 0 and count % 50 == 0: print >>sys.stderr, 'read', count, 'of', len(pdbs)
    count += 1

    scores = []
    #print pdb
    pose = pose_from_pdb(indir + pdb)
    name = pdb.rstrip('.pdb')
    scorefxn = get_fa_scorefxn()

    total_res =  pose.total_residue()
    cons = []
    con = {}
    distance_cutoff = 6
    for i in range(1,total_res+1):
        #print i
        a = []
        for j in range(1,total_res):
            r1 = pose.residue(i)
            r2 = pose.residue(j)
            distance = r1.xyz(r1.nbr_atom()).distance(r2.xyz(r1.nbr_atom()))
            if distance < distance_cutoff and distance > 0:
                #print i,j, " .  " ,distance
                a.append(j)
        a.sort()
        cons.append(a)
        con[i] = a

    longest = 0 
    most_connected = 0
    for residue in con:
        if len(con[residue]) > longest:
            longest = len(con[residue])
            most_connected = residue

    #print most_connected, "is most connected with ",longest, "neighbors"
   
    sasa = SasaCalc()
    sasa.calculate(pose)

    scorefxn(pose)
    energies = pose.energies()
    most_connected_energies = energies.residue_total_energies(most_connected)[core.scoring.total_score]

    #print "most_connected_energies", most_connected_energies
    #print "most_connected_energies norm", most_connected_energies/most_connected

    #threshold for bad score? how many contacts?
    #how do I get the burial number? because that would be beautiful. The most connected one needs to be very buried 
    #apparently that is not given...

    sasas = []
    res_e = []
    connectivity = []
    norm_con =[]
    threshold_for_connectivity = 6 # 5.5 #version one : 4
    score_well_connected_residues = 0
    score_well_connected_residues_norm = 0
    penalty_badlyscoring_hubs = 0

    num_bad_res = 0
    
    total_res = pose.total_residue()
    
    for res in range(1,total_res+1):

        
        resi_e = energies.residue_total_energies(res)[core.scoring.total_score]
        
        res_e.append(energies.residue_total_energies(res)[core.scoring.total_score])
        sasas.append(sasa.get_residue_sasa()[res])
        connectivity.append(len(con[res]))
        if len(con[res])== 0:
            norm_con.append(energies.residue_total_energies(res)[core.scoring.total_score])
        else:
            norm_con.append(energies.residue_total_energies(res)[core.scoring.total_score]/len(con[res]))    

        if len(con[res]) == 0:
            norm_res_e  = energies.residue_total_energies(res)[core.scoring.total_score]
        else:
            norm_res_e  = energies.residue_total_energies(res)[core.scoring.total_score]/len(con[res])
            
        res_sasa = sasa.get_residue_sasa()[res]

        if resi_e > -0.25:
            #print "res energy:", resi_e, "with" ,len(con[res]), "connections!!!!"
            num_bad_res += 1
            
        num_connections_resi = len(con[res])

    ### parameters to report:

    #above a connectvity the normalized score needs to be < -0.25
    #penalize everything above that 
        if num_connections_resi > threshold_for_connectivity and resi_e > -0.25:
            if resi_e < 0:
                penalty_badlyscoring_hubs +=  resi_e * -1.0
            elif resi_e > 0:
                penalty_badlyscoring_hubs += resi_e + 0.25

    #buried residues should be well connected -> penalties


    #sum of score of all residues connected above 4 - normalized by the residues
    #sum score of top 4 most connected residues
        if num_connections_resi > threshold_for_connectivity:
            score_well_connected_residues += resi_e
            score_well_connected_residues_norm += norm_res_e


    # score of the 4 most connected residues
    res_connectivity = {}
    a = []
    for key in con:
        res_connectivity[ key] =  len(con[key])
        a.append(len(con[key]))

    a.sort()
    thresh =  a[-3]
    scores_top_connected = []
    scores_norm_top_connected = []
    #average of the most 4 in res energy
    for k in res_connectivity:
        if res_connectivity > thresh:
            scores_top_connected.append(energies.residue_total_energies(k)[core.scoring.total_score])
            if len(con[k]) !=  0:
                scores_norm_top_connected.append(energies.residue_total_energies(k)[core.scoring.total_score]/len(con[k]))
        
    average_scores_top_connected = np.array(scores_top_connected).mean()
    average_scores_norm_top_connected = np.array(scores_norm_top_connected).mean()

    #connectivity density
    newgraph = Graph(con)
    connections = np.array(cons)
    connections = np.unique(connections)
    connections
    connectedness =[]
    

    for i in connections:
        connectedness.append(len(i))
    connectedness = np.array(connectedness)

    design_scores[pdb] = [most_connected_energies,most_connected_energies/most_connected,newgraph.density(),
               penalty_badlyscoring_hubs,score_well_connected_residues,score_well_connected_residues/total_res,score_well_connected_residues_norm,score_well_connected_residues_norm/total_res,average_scores_top_connected,
              average_scores_norm_top_connected,connectedness.mean(),np.median(connectedness),connectedness.max(),num_bad_res]
    
   
header = ['most_conRE','most_conREn','graph_density','bad_hub_penalty','highly_conREsum','highly_conREsum_pres','highly_conREsumNorm','highly_conREsumNorm_pres','avgE_top_conResidues',
         'avgE_top_conResiduesNorm','avg_con','median_con','max_con','num_bad_res']
print len(header)

scores = pd.DataFrame.from_dict(design_scores,orient='index')#,columns=header)
scores.columns = header
scores.to_csv('score3_simple.csv')

    
