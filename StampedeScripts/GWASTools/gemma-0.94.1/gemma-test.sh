#!/bin/bash
#set -x
WRAPPERDIR=$( cd "$( dirname "$0" )" && pwd )
chmod +x gemma
#Test the relatedness matrix calculation
PLINK=true
inputBED="$WRAPPERDIR/test/mouse_hs1940.bed"
inputBIM="$WRAPPERDIR/test/mouse_hs1940.bim"
inputFAM="$WRAPPERDIR/test/mouse_hs1940.fam"
Type=1
output="gemma-test1"
gk=1
#Call the wrapper script here
. ./gemma-wrap.sh