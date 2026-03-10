import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.LinkedHashSet;
import java.util.Set;

/**
 *  Builds an edge list for the Bitcoin Address-Transaction Graph starting from the transaction list.
 *  Note that the output file is not sorted, and may contain duplicate edges. Self loops are ignored.
 * 
 *  @author Matteo Loporchio
 */
public class AddressTxGraphEdgeListBuilder {
	//public static int currentTxNodeId = 0;

	public static void main(String[] args) {
		// Read and parse arguments from the command line.
        if (args.length < 3) {
            System.err.printf("Usage: %s <inputFile> <outputFile> <baseTxNodeId>\n", AddressTxGraphEdgeListBuilder.class.getName());
            System.exit(1);
        }
        final String inputFile = args[0];
        final String outputFile = args[1];
        final int baseTxNodeId = Integer.parseInt(args[2]);
        // Open the input and output files.
        try (
            BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(inputFile)));
            PrintWriter out = new PrintWriter(outputFile);
        ) {
            String line = null;
            while ((line = in.readLine()) != null) {
                // Split the line and obtain info and inputs.
                String[] parts = line.split(":"),
                infos = parts[0].split(","),
                inputs = parts[1].split(";"),
                outputs = parts[2].split(";");

                // Obtain the current transaction id.
                int currentTxNodeId = Integer.parseInt(infos[2]);

                // For each unique input address, create an edge between the address and the transaction node.
                if (!parts[1].equals("")) {
                    Set<String> inputAddresses = new LinkedHashSet<>();
                    for (int offset = 0; offset < inputs.length; offset++) {
                        String[] inputParts = inputs[offset].split(",");
                        String address = inputParts[0];
                        inputAddresses.add(address);
                    }
                    for (String address : inputAddresses) 
                        out.printf("%s\t%d\n", address, baseTxNodeId + currentTxNodeId);
                }

                if (!parts[2].equals("")) {
                    Set<String> outputAddresses = new LinkedHashSet<>();
                    for (int offset = 0; offset < outputs.length; offset++) {
                        String[] outputParts = outputs[offset].split(",");
                        String address = outputParts[0];
                        outputAddresses.add(address);
                    }
                    for (String address : outputAddresses)
                        out.printf("%d\t%s\n", baseTxNodeId + currentTxNodeId, address);
                }
                //currentTxNodeId++;
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }

	}

}
