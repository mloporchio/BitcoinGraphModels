#
#	File:	makefile
#	Author:	Matteo Loporchio
#

CXX=g++
CXX_FLAGS=-O3 --std=c++11 -I /data/matteoL/igraph/include/igraph
LD_FLAGS=-L /data/matteoL/igraph/lib -ligraph -fopenmp

.PHONY: clean

%.o: %.cpp
	$(CXX) $(CXX_FLAGS) -c $^

connectivity: connectivity.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

degree: degree.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

pagerank: pagerank.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

pagerank_dag: pagerank_dag.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

all: connectivity degree pagerank pagerank_dag

clean:
	$(RM) *.o connectivity degree pagerank pagerank_dag
