import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

/**
 * @author Matteo Loporchio
 */
public class PaymentGraphEdgeListBuilder {
	public static int nextId = 0;
	public static Map<String, Integer> nodes = new LinkedHashMap<>();

    public static int getOrCreateId(String key) {
        if (!nodes.containsKey(key)) {
            nodes.put(key, nextId);
            nextId++;
        }
        return nodes.get(key);
    }

	public static void main(String[] args) {
		// Read and parse arguments from the command line.
        if (args.length < 3) {
            System.err.printf("Usage: %s <inputFile> <nodeFile> <edgeFile>\n", PaymentGraphEdgeListBuilder.class.getName());
            System.exit(1);
        }
        final String inputFile = args[0];
        final String nodeFile = args[1];
        final String edgeFile = args[2];
        // Open the input and output files.
        try (
            BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(inputFile)));
            PrintWriter nodeWriter = new PrintWriter(nodeFile);
        	PrintWriter edgeWriter = new PrintWriter(edgeFile);
        ) {
            String line = null;
            while ((line = in.readLine()) != null) {
                // Split the line and obtain info and inputs.
                String[] parts = line.split(":"),
                infos = parts[0].split(","),
                inputs = parts[1].split(";"),
                outputs = parts[2].split(";");
                // Obtain the current transaction identifier.
                String txId = infos[2];
                // Create a node for each output.
                List<Integer> currentOutputNodeIds = new ArrayList<>();
                if (!parts[2].equals("")) {
                    for (int offset = 0; offset < outputs.length; offset++) {
                    	String nodeStr = txId + ":" + offset;
                        int nodeId = getOrCreateId(nodeStr);
                    	currentOutputNodeIds.add(nodeId);
                    }
                }
                // For each input, create an edge between the input node and each output node.
                if (!parts[1].equals("")) {
                    for (int offset = 0; offset < inputs.length; offset++) {
                        String[] inputParts = inputs[offset].split(",");
                        String prevTxId = inputParts[2];
                        String prevTxOffset = inputParts[3];
                        int sourceNodeId = nodes.get(prevTxId + ":" + prevTxOffset);
                        // Create an edge between the input node and each output node.
                        for (int targetNodeId : currentOutputNodeIds) {
                            edgeWriter.printf("%d\t%d\n", sourceNodeId, targetNodeId);
                        }
                    }
                }
            }
            // Write nodes to the corresponding file.
            for (String key : nodes.keySet()) {
            	int value = nodes.get(key);
           		nodeWriter.printf("%s\t%d\n", key, value);
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }

	}

}
