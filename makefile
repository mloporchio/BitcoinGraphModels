#
#	File:	makefile
#	Author:	Matteo Loporchio
#

CXX=g++
CXX_FLAGS=-O3 --std=c++11 -I /data/matteoL/igraph/include/igraph
LD_FLAGS=-L /data/matteoL/igraph/lib -ligraph -fopenmp
JC=javac
SRC_DIR=src
OBJ_DIR=obj
BIN_DIR=bin
CLUST_MODULE=BitcoinAddressClustering

# Create output directories
$(shell mkdir -p $(OBJ_DIR) $(OBJ_DIR)/$(CLUST_MODULE) $(BIN_DIR) $(BIN_DIR)/$(CLUST_MODULE))

.PHONY: classes clean all

classes:
	$(JC) -d $(BIN_DIR) $(SRC_DIR)/*.java

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXX_FLAGS) -c $< -o $@

$(BIN_DIR)/connectivity: $(OBJ_DIR)/connectivity.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

$(BIN_DIR)/degree: $(OBJ_DIR)/degree.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

$(BIN_DIR)/pagerank: $(OBJ_DIR)/pagerank.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

$(BIN_DIR)/pagerank_dag: $(OBJ_DIR)/pagerank_dag.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

# Rules for building the clustering module
$(OBJ_DIR)/$(CLUST_MODULE)/%.o: $(SRC_DIR)/$(CLUST_MODULE)/%.cpp
	$(CXX) $(CXX_FLAGS) -c $< -o $@

$(BIN_DIR)/$(CLUST_MODULE)/builder: $(OBJ_DIR)/$(CLUST_MODULE)/builder.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

$(BIN_DIR)/$(CLUST_MODULE)/clustering: $(OBJ_DIR)/$(CLUST_MODULE)/clustering.o
	$(CXX) $(CXX_FLAGS) $^ -o $@ $(LD_FLAGS)

all: $(BIN_DIR)/connectivity \
	$(BIN_DIR)/degree \
	$(BIN_DIR)/pagerank \
	$(BIN_DIR)/pagerank_dag \
	$(BIN_DIR)/$(CLUST_MODULE)/builder \
	$(BIN_DIR)/$(CLUST_MODULE)/clustering \
	classes

clean:
	$(RM) -rf $(OBJ_DIR) $(BIN_DIR)
