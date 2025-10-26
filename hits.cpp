/**
 * @file hits.cpp
 * @author Matteo Loporchio
 * @date 2025-05-21
 *
 * This program reads the edge list of a directed graph from a text file (in TSV format)
 * and computes the Hub and Authority scores for all nodes.
 *
 * The output is written to a TSV file.
 *
 *  INPUT:
 *  The edge list for the collapsed graph (in TSV format).
 *
 *  OUTPUT:
 *  A TSV file summarizing the Hub and Authority scores for each node.
 *  The output file contains one line for each node and each line includes the following fields:
 *      - numeric identifier of the node;
 *      - Hub score of the node;
 *      - Authority score of the node;
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

    // Compute Hub and Authority scores.
    igraph_vector_t hub, auth;
    igraph_vector_init(&hub, num_nodes);
    igraph_vector_init(&auth, num_nodes);
    igraph_hub_and_authority_scores(&graph, &hub, &auth, NULL, 0, NULL, NULL);
 
    // Write the results to the output TSV file.
    // FILE *output_file = fopen(argv[2], "w");
    // if (!output_file) {
    //     cerr << "Error: could not open output file!\n";
    //     return 1;
    // }
    // fprintf(output_file, "node_id\thub_score\tauthority_score\n");
    // for (int i = 0; i < num_nodes; i++) {
    //     double h = VECTOR(hub)[i];
    //     double a = VECTOR(auth)[i];
    //     fprintf(output_file, "%d\t%.15f\t%.15f\n", i, h, a);
    // }
    // fclose(output_file);

    // Free the memory occupied by the graph.
    igraph_destroy(&graph);
    igraph_vector_destroy(&hub);
    igraph_vector_destroy(&auth);

    auto end = high_resolution_clock::now();
    auto elapsed = duration_cast<nanoseconds>(end - start);

    // Print information about the program execution. 
    cout << num_nodes << '\t' << num_edges << '\t' << elapsed.count() << '\n';
    return 0;
}

