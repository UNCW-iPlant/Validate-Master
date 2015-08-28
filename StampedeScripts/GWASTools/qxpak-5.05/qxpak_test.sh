#!/bin/bash
WRAPPERDIR="$( cd "$( dirname "$0" )" && pwd )"
cd ./test
pedigree_file="qxpak_1.ped"
marker_file="qxpak_1.mkr"
data_file="qxpak_1.dat"
parameter_file="qxpak_1.par"
output="Test"
mv -t . $WRAPPERDIR/qxpak_wrapper.sh $WRAPPERDIR/qxpakwrapper.py $WRAPPERDIR/qxpak.linux64
. ./qxpak_wrapper.sh
