# Data description

## General information

This repository contains data regarding Bitcoin dust transactions. In particular, it comprises all transactions included in the first 479,970 blocks of the Bitcoin blockchain, thus covering the time period between January 3rd, 2009 18:15 GMT and August 10th, 2017 18:03 GMT.

## Dataset description

The repository comprises three files, compressed using the XZ utility (https://tukaani.org/xz/).

- `tx_list.txt.xz`: This text file contains the list of transactions, according to the format described in the next section.

- `addr_id_map.csv.xz`: This CSV file contains the mapping between Bitcoin addresses and the corresponding numeric identifiers used within `tx_list.txt.xz`. Specifically, each line corresponds to an address and is made up of two comma-separated fields: the first field represents the full Bitcoin address, while the second field represents the corresponding numeric identifier.

- `txhash_id_map.csv.xz`: This CSV file contains the mapping between transaction hashes and the corresponding numeric identifiers used within `tx_list.txt.xz`. In particular, each line represents a transaction and includes two comma-separated fields: the first field represents the hash of the transaction, while the second field denotes the corresponding numeric identifier.

## Transaction representation

The `tx_list.txt.xz` file contains a textual representation of dust transactions in the Bitcoin blockchain. Each row of the file corresponds to a transaction and is represented as a sequence of fields

```info:inputs:outputs```

with the following meaning.

The `info` section contains general information about the transaction. It is represented as a list of comma-separated fields, namely: 

```timestamp,blockId,txId,isCoinbase,fee,approxSize```

The meaning of the fields is the following:
        
- `timestamp` represents the Unix timestamp of the block containing the transaction.
- `blockId` represents the height of the block containing the transaction.
- `txId` is a numeric value that univocally identifies the transaction.
- `isCoinbase` is equal to 1 if the transaction is a coinbase transaction, 0 otherwise.
- `fee` denotes the transaction fee, expressed in satoshis (i.e., the smallest bitcoin denomination).
- `approximateSize` denotes the approximate size of the transaction (expressed in bytes).

The inputs section contains a sequence of (0 or more) transaction inputs separated by a semicolon. Each input, in turn, is represented as a comma-separated string 

```addrId,amount,prevTxId,offset```

where:

- `addrId` represents the numeric identifier of the spending address;
- `amount` is the amount of value associated with the input (expressed in satoshis);
- `prevTxId` represents the numeric identifier of the transaction that created the output that is currently being spent;
- `offset` represents the position, among all outputs of `prevTxId`, of the output that is currently being spent.
         
The outputs section contains a sequence of (1 or more) transaction outputs separated by a semicolon. Each output, in turn, is represented as a comma-separated string 

```addrId,amount,scriptType``` 

where:
     
- `addrId` represents the numeric identifier of the receiving address;
- `amount` is the amount of value associated with the output (expressed in satoshis);
- `scriptType` is a numeric identifier representing the type of the script associated with the output (i.e., 0=UNKNOWN; 1=P2PK; 2=P2PKH; 3=P2SH; 4=RETURN; 5=EMPTY).
