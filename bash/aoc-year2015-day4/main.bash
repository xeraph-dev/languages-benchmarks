#!/usr/bin/env bash

secret=$1
zeros_count=$2
zeros=""

for (( i=1; i<=$zeros_count; i++ )); do
  zeros="${zeros}0"
done

for (( i=1; i<=((2**32)); i++)); do (
  sum=`md5 -q -s "${secret}$i"`
  sum="${sum:0:$zeros_count}"
  if [[ "$sum" == "$zeros" ]]; then
    echo "$i"
    exit 0
  fi
) &
done
