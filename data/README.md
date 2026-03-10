# data

This folder contains the data used for the experiments.

For space reasons, the data used for the experiments is not included. 
However, such data can be obtained from the following Zenodo repository: 

https://doi.org/10.5281/zenodo.18938800 

Please note that all downloaded information should be placed in this folder and decompressed.

Files are compressed using the XZ format, which can be decompressed using the following command:

```
xz -d <file_name>.xz
```

Please note that the decompressed files can be quite large (tens of GB), so make sure to have enough storage space available.

## Content

- `tx_list.txt.xz`: This file contains the list of transactions.
- `addr_id_map.csv.xz`: This file contains the mapping between addresses and the corresponding numeric identifiers used within `tx_list.txt.xz`.
- `txhash_id_map.csv.xz`: This file contains the mapping between transaction hashes and the corresponding numeric identifiers used within `tx_list.txt.xz`.