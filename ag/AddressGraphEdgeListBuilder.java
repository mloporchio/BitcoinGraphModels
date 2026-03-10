import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.LinkedHashSet;
import java.util.Set;

/**
 * Builds an edge list for the Bitcoin Address Graph starting from the transaction list.
 * Note that the output file is not sorted, and may contain duplicate edges. Self loops are ignored.
 * 
 * @author Matteo Loporchio
 */
public class AddressGraphEdgeListBuilder {
	public static void main(String[] args) {
		// Read and parse arguments from the command line.
        if (args.length < 2) {
            System.err.println("Usage: AddressGraphEdgeListBuilder <inputFile> <outputFile>");
            System.exit(1);
        }
        final String inputFile = args[0];
        final String outputFile = args[1];
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

                Set<String> inputAddresses = new LinkedHashSet<>();
                Set<String> outputAddresses = new LinkedHashSet<>();

                // Collect all unique input addresses.
                if (!parts[1].equals("")) {
                    for (int offset = 0; offset < inputs.length; offset++) {
                        String[] inputParts = inputs[offset].split(",");
                        String address = inputParts[0];
                        inputAddresses.add(address);
                    }
                }

                // Collect all unique output addresses.
                if (!parts[2].equals("")) {
                    for (int offset = 0; offset < outputs.length; offset++) {
                        String[] outputParts = outputs[offset].split(",");
                        String address = outputParts[0];
                        outputAddresses.add(address);
                    }
                }

                // Connect each output address to all input addresses (self loops are ignored).
                for (String outputAddress : outputAddresses) {
                    for (String inputAddress : inputAddresses) {
                        if (!inputAddress.equals(outputAddress)) {
                            out.println(inputAddress + "\t" + outputAddress);
                        }
                    }
                }
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
	}
}
