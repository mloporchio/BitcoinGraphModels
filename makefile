#
#	File:	makefile
#	Author:	Matteo Loporchio
#

CXX=g++
CXX_FLAGS=-O3 --std=c++11 -I /data/matteoL/igraph/include/igraph
LD_FLAGS=-L /data/matteoL/igraph/lib -ligraph -fopenmp
JC=javac
JC_FLAGS=-cp ".:lib/*"

.PHONY: clean

classes:
	$(JC) $(JC_FLAGS) *.java

%.o: %.cpp
	$(CXX) $(CXX_FLAGS) -c $^

clustering: clustering.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

connectivity: connectivity.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

degree: degree.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

pagerank: pagerank.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

pagerank_dag: pagerank_dag.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

all: clustering connectivity degree hits pagerank pagerank_dag

clean:
	$(RM) *.class *.o clustering connectivity degree hits pagerank pagerank_dag
