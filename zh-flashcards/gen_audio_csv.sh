#!/bin/bash
#
#

DATA_FILE=$1
AUDIO_DIR=$2

#
function fetch() {
  HEADERS="-U=Mozilla"
  QUERY=$1
  OUTFILE=$2
  wget -O "$OUTFILE" $HEADERS 'https://code.responsivevoice.org/getvoice.php?t='$QUERY'&tl=zh-TW&sv=g1&vn=&pitch=0.5&rate=0.44&vol=1'
}




#
# check if AUDIO_DIR exists


#
# check if DATA_FILE exists, add audio column
if [ -r "$DATA_FILE" ]; then
  head -1 $DATA_FILE | grep audio
  if [ $? -eq 0 ]; then
    echo "audio already exists in $DATA_FILE, skipping"
  else
    echo `head -1 $DATA_FILE`",audio" > _TEMP
    audio_c=1
    sed 1d $DATA_FILE | while read -r line ; do
      arrIN=(${line//,/ })
      key=${arrIN[0]}
      echo "$line,$AUDIO_DIR/$audio_c.mp3" >> _TEMP
      ((audio_c++))
    done
    mv _TEMP $DATA_FILE
  fi
fi


#
# check if audio files exist, fetch if not
if [ -r "$DATA_FILE" ]; then
  csvtool namedcol key,audio $DATA_FILE | while read -r line ; do
    arrIN=(${line//,/ })
    key=${arrIN[0]}
    audio=${arrIN[1]}
    if [ "$audio" == "audio" ]; then
      echo "this file has audio"
    elif [ -r "audio/$audio" ]; then
      echo "$audio exists"
    else
      echo "fetch $key into audio/$audio"
      fetch "$key" "audio/$audio"
    fi
  done
fi


