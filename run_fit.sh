#!/bin/bash
#
#   This script fits a power law function to the degree and component size distributions of each graph model.
#   The script requires the plfit tool to be installed (see: https://github.com/ntamas/plfit).
#
#   Author: Matteo Loporchio
#

compute_comp_size() {
    python3 - <<END
import polars as pl
df = pl.read_csv('${1}/connectivity.tsv', separator="\t")
data = df['${2}_id'].value_counts(name="comp_size")
data.select("comp_size").write_csv('${3}', include_header=False)
END
}

MODELS=("ag" "tg" "atg" "ug" "pg")
METRICS=("in_degree" "out_degree" "scc" "wcc")
PLFIT_EXEC="~/plfit-1.0.1/build/src/plfit"
TEMP_DIR="tmp"
OUTPUT_FILE="results/fit.tsv"

mkdir -p $TEMP_DIR

printf "model\tmetric\talpha\tx_min\tL\tD\tp_value\telapsed_time\n" > $OUTPUT_FILE
for MODEL in "${MODELS[@]}"; do
    for METRIC in "${METRICS[@]}"; do
        TEMP_FILE="${TEMP_DIR}/${MODEL}_${METRIC}.txt"
        echo "Preparing data for model $MODEL and metric $METRIC..."
        START_TIME=$EPOCHSECONDS
        case $METRIC in
            "in_degree")
                cat $MODEL/degree.tsv | cut -d$'\t' -f2 | tail -n +2 > $TEMP_FILE
                ;;
            "out_degree")
                cat $MODEL/degree.tsv | cut -d$'\t' -f3 | tail -n +2 > $TEMP_FILE
                ;;
            "scc" | "wcc")
                compute_comp_size $MODEL $METRIC $TEMP_FILE
                ;;
            *)
                echo "Error: unsupported metric $METRIC."
                rm -rf $TEMP_DIR
                exit 1
                ;;
        esac
        echo "Done in $((EPOCHSECONDS - START_TIME)) seconds."
        echo "Fitting power law for model $MODEL and metric $METRIC..."
        START_TIME=$EPOCHSECONDS
        if PLFIT_OUT=$((eval ${PLFIT_EXEC} -p approximate -b ${TEMP_FILE}) 2>/dev/null); then
            echo "Done in $((EPOCHSECONDS - START_TIME)) seconds."
            echo "Result: ${PLFIT_OUT}"
            # Fitted exponent, minimum X value, log-likelihood (L), Kolmogorov-Smirnov statistic (D) and p-value (p)
            ELAPSED_TIME=$((EPOCHSECONDS - START_TIME))
            ALPHA=$(echo $PLFIT_OUT | cut -d' ' -f3)
            X_MIN=$(echo $PLFIT_OUT | cut -d' ' -f4)
            LL=$(echo $PLFIT_OUT | cut -d' ' -f5)
            KS=$(echo $PLFIT_OUT | cut -d' ' -f6)
            P_VALUE=$(echo $PLFIT_OUT | cut -d' ' -f7)
            printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$MODEL" "$METRIC" "$ALPHA" "$X_MIN" "$LL" "$KS" "$P_VALUE" "$ELAPSED_TIME" >> $OUTPUT_FILE
        else
            echo "Error: fitting failure for model $MODEL and metric $METRIC."
            rm -rf $TEMP_DIR
            exit 1
        fi
        rm -f $TEMP_FILE
    done
done

echo "Done. All models and metrics processed successfully!"
rm -rf $TEMP_DIR
exit 0
