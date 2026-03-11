import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

/**
 * This class reads the Bitcoin transaction list and creates a file containing all transaction outputs.
 * The output file is in TSV format, and each line corresponds to a transaction output.
 * For each output, we record:
 * - the identifier of the transaction it belongs to;
 * - the position (offset) of the output within the list of outputs of the transaction;
 * - the address (i.e., the address being paid by the output).
 * 
 * @author Matteo Loporchio
 */
public class TxSplitter {
	public static void main(String[] args) {
		// Read and parse arguments from the command line.
        if (args.length < 2) {
            System.err.printf("Usage: %s <txFile> <txOutputFile>\n", TxSplitter.class.getName());
            System.exit(1);
        }
        final String txFile = args[0];
        //final String txInputFile = args[1];
        final String txOutputFile = args[1];
        // Open the input and output files.
        try (
            BufferedReader txReader = new BufferedReader(new InputStreamReader(new FileInputStream(txFile)));
            //PrintWriter inputWriter = new PrintWriter(txInputFile);
            PrintWriter outputWriter = new PrintWriter(txOutputFile);
        ) {
            String line = null;
            while ((line = txReader.readLine()) != null) {
                // Split the current line.
                String[] parts = line.split(":");
                // Obtain the current transaction identifier.
                String[] infos = parts[0].split(",");
                String txId = infos[2];
                // Parse TX inputs.
                // if (!parts[1].equals("")) {
                //     String[] inputs = parts[1].split(";");
                //     for (int i = 0; i < inputs.length; i++) {
                //         // addrId','amount','prevTxSpending',' position_of_output_in_prevTxSpending
                //         String[] inputParts = inputs[i].split(",");
                //     	inputWriter.printf("%s\t%d\t%s\t%s\t%s\n", txId, i, inputParts[0], inputParts[2], inputParts[3]);
                //     }
                // }
                // Parse TX outputs.
                if (!parts[2].equals("")) {
                    String[] outputs = parts[2].split(";");
                    for (int i = 0; i < outputs.length; i++) {
                        // addrId, amount, scriptType
                        String[] outputParts = outputs[i].split(",");
                    	outputWriter.printf("%s\t%d\t%s\n", txId, i, outputParts[0]);
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
