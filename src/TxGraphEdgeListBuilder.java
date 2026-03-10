import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.LinkedHashSet;
import java.util.Set;

/**
 * @author Matteo Loporchio
 */
public class TxGraphEdgeListBuilder {
	public static void main(String[] args) {
		// Read and parse arguments from the command line.
        if (args.length < 2) {
            System.err.printf("Usage: %s <inputFile> <outputFile>\n", TxGraphEdgeListBuilder.class.getName());
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

                // Obtain the current transaction id.
                String currentTxId = infos[2];

                // Collect all unique transaction identifiers from the inputs.
                // These identifiers represent the transactions whose outputs 
                // are being consumed by the current transaction.
                Set<String> previousTxIds = new LinkedHashSet<>();
                if (!parts[1].equals("")) {
                    for (int offset = 0; offset < inputs.length; offset++) {
                        String[] inputParts = inputs[offset].split(",");
                        String prevTxId = inputParts[2];
                        previousTxIds.add(prevTxId);
                    }
                }

                for (String prevTxId : previousTxIds) {
                    if (!prevTxId.equals(currentTxId)) out.printf("%s\t%s\n", prevTxId, currentTxId);
                }
            }
        }
        catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
	}
}
