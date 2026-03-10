/**
 * @file pagerank.cpp
 * @author Matteo Loporchio
 * @date 2025-05-15
 *
 * This program reads the edge list of a directed graph from a text file (in TSV format)
 * and computes the PageRank for all nodes.
 *
 * The PageRank is computed with a default damping factor of 0.85.
 * The output is written to a TSV file.
 *
 *  INPUT:
 *  The edge list for the collapsed graph (in TSV format).
 *
 *  OUTPUT:
 *  A TSV file summarizing the PageRank for each node.
 *  The output file contains one line for each node and each line includes the following fields:
 *      - numeric identifier of the node;
 *      - PageRank of the node;
 *
 *  PRINT:
 *  The program prints the following information to stdout:
 *      - number of graph nodes;
 *      - number of graph edges;
 *      - elapsed time (in nanoseconds).
 */

#include <chrono>
#include <iostream>
#include <igraph.h>

#define DAMPING_FACTOR 0.85 // default damping factor for PageRank

using namespace std;
using namespace std::chrono;

int main(int argc, char **argv) {
    if (argc < 3) {
        cerr << "Usage: " << argv[0] << " <input_file> <output_file>\n";
        return 1;
    }
    
    auto start = high_resolution_clock::now();
    
    // Load the graph from the corresponding file.
    FILE *input_file = fopen(argv[1], "r");
    if (!input_file) {
        cerr << "Error: could not open input file!\n";
        return 1;
    }
    igraph_t graph;
    igraph_read_graph_edgelist(&graph, input_file, 0, IGRAPH_DIRECTED);
    fclose(input_file);

    // Obtain the number of nodes and edges.
    igraph_integer_t num_nodes = igraph_vcount(&graph);
    igraph_integer_t num_edges = igraph_ecount(&graph);

    // Compute PageRank.
    igraph_vector_t pagerank;
    igraph_vector_init(&pagerank, num_nodes);
    igraph_pagerank(&graph, IGRAPH_PAGERANK_ALGO_PRPACK, &pagerank, NULL, igraph_vss_all(), IGRAPH_DIRECTED, DAMPING_FACTOR, NULL, NULL);
 
    // Write the results to the output TSV file.
    FILE *output_file = fopen(argv[2], "w");
    if (!output_file) {
        cerr << "Error: could not open output file!\n";
        return 1;
    }
    fprintf(output_file, "node_id\tpagerank\n");
    for (int i = 0; i < num_nodes; i++) {
        double p = VECTOR(pagerank)[i];
        fprintf(output_file, "%d\t%.15f\n", i, p); 
    }
    fclose(output_file);

    // Free the memory occupied by the graph.
    igraph_destroy(&graph);
    igraph_vector_destroy(&pagerank);
    
    auto end = high_resolution_clock::now();
    auto elapsed = duration_cast<nanoseconds>(end - start);

    // Print information about the program execution. 
    cout << num_nodes << '\t' << num_edges << '\t' << elapsed.count() << '\n';
    return 0;
}

