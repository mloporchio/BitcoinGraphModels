/**
 * @file degree.cpp
 * @author Matteo Loporchio
 * @date 2025-05-15
 *
 * This program reads the edge list of a directed graph from a text file (in TSV format)
 * and computes the in- and out-degree for all nodes.
 *
 *  INPUT:
 *  The edge list for the collapsed graph (in TSV format).
 *
 *  OUTPUT:
 *  A TSV file summarizing the degree for each node.
 *  The output file contains one line for each node and each line includes the following fields:
 *      - numeric identifier of the node;
 *      - in-degree of the node;
 *      - out-degree of the node;
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

    // Compute in-degree and out-degree.
    igraph_vector_int_t in_degree, out_degree;
    igraph_vector_int_init(&in_degree, num_nodes);
    igraph_vector_int_init(&out_degree, num_nodes);
    igraph_degree(&graph, &in_degree, igraph_vss_all(), IGRAPH_IN, 1);
    igraph_degree(&graph, &out_degree, igraph_vss_all(), IGRAPH_OUT, 1);

    // Write the results to the output TSV file.
    FILE *output_file = fopen(argv[2], "w");
    if (!output_file) {
        cerr << "Error: could not open output file!\n";
        return 1;
    }
    fprintf(output_file, "node_id\tin_degree\tout_degree\n");
    for (int i = 0; i < num_nodes; i++) {
        int in = VECTOR(in_degree)[i];
        int out = VECTOR(out_degree)[i];
        fprintf(output_file, "%d\t%d\t%d\n", i, in, out);
    }
    fclose(output_file);

    // Free the memory occupied by the graph.
    igraph_destroy(&graph);
    igraph_vector_int_destroy(&in_degree);
    igraph_vector_int_destroy(&out_degree);

    auto end = high_resolution_clock::now();
    auto elapsed = duration_cast<nanoseconds>(end - start);

    // Print information about the program execution. 
    cout << num_nodes << '\t' << num_edges << '\t' << elapsed.count() << '\n';
    return 0;
}

