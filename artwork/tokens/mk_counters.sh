COUNTER=$1

if [[ "x$COUNTER" == "x" ]]; then
    echo "Insert counter file name"
    exit
fi

OUT=$(basename $COUNTER)

if [[ "$COUNTER" == "$OUT" ]]; then
    echo "Counter $COUNTER can not be in this very directory"
    exit
fi

gm convert -size 285x400 xc:white $OUT
gm composite $COUNTER -geometry +16+11 $OUT $OUT
gm composite $COUNTER -geometry +151+11 $OUT $OUT
gm composite $COUNTER -geometry +16+141 $OUT $OUT
gm composite $COUNTER -geometry +151+141 $OUT $OUT
gm composite $COUNTER -geometry +16+271 $OUT $OUT
gm composite $COUNTER -geometry +151+271 $OUT $OUT
