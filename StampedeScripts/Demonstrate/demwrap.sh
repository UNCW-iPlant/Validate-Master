#!/bin/bash

WRAPPERDIR=$( cd "$( dirname "$0" )" && pwd)

#Load the required arguments
DIRECTORY=${directory}
if [[ ! -e "$DIRECTORY" ]]; then
    echo "Input directory was not found" >&2
    exit 1
fi

settings=${settingsFile}
if [[ -n "$settings" ]]; then
    SETTINGS="--settings ${settings}"
fi

out=${output}
if [[ -n "$out" ]]; then
    OUTPUT="--output ${out}"
fi

mode=${mode}
if [[ "$mode" == "demonstrate" ]]; then
    xauc=${xauc}
    if [[ -n "$xauc" ]]; then
        XAUC="--xauc"
    fi
    auctitle=${auctitle}
    if [[ -n "$auctitle" ]]; then
        AUCTITLE="--auctitle ${auctitle}"
    fi
    xmae=${xmae}
    if [[ -n "$xmae" ]]; then
        XMAE="--XMAE"
    fi
    maetitle=${maetitle}
    if [[ -n "$maetitle" ]]; then
        MAETITLE="--maetitle ${maetitle}"
    fi
    heritstring=${heritstring}
    if [[ -n "$heritstring" ]]; then
        HERITSTRING="--heritstring ${heritstring}"
    fi
    heritvalue=${heritvalue}
    if [[ -n "$heritvalue" ]]; then
        HERITVALUE="--heritvalue ${heritvalue}"
    fi
    structstring=${structstring}
    if [[ -n "$structstring" ]]; then
        STRUCTTSTRING="--structstring ${structstring}"
    fi
    structvalue=${structvalue}
    if [[ -n "$structvalue" ]]; then
        STRUCTVALUE="--structvalue ${structvalue}"
    fi
    # start demo1
    # add verbose option
    if [[ ! -d "$WRAPPERDIR/dempy" ]]; then
        tar xzvf demonstrate.tgz
    fi
    python $WRAPPERDIR/dempy/demonstrate.py "${DIRECTORY} ${OUTPUT} ${SETTINGS} ${mode} ${XAUC} ${AUCTITLE} ${XMAE} ${MAETITLE} ${HERITSTRING} ${HERITVALUE} ${STRUCTTSTRING} ${STRUCTVALUE}"
elif [[ "$mode" == "demonstrate2" ]]; then
    xpos=${xpos}
    if [[ -n "$xpos" ]]; then
        XPOS="--xpos"
    fi
    postitle=${postitle}
    if [[ -n "$postitle" ]]; then
        POSTITLE="--postitle ${postitle}"
    fi
    xerror=${xerror}
    if [[ -n "$xerror" ]]; then
        XERROR="--xerror"
    fi
    errortitle=${errortitle}
    if [[ -n "$errortitle" ]]; then
        ERRORTITLE="--errortitle ${errortitle}"
    fi
    extraplots=${extraplots}
    if [[ ! -n "$extraplots" ]]; then
        EXTRA="--extraplots"
    fi
    aucmin=${aucmin}
    if [[ -n "$aucmin" ]]; then
        AUCMIN="--aucmin ${aucmin}"
    fi
    aucmax=${aucmax}
    if [[ -n "$aucmax" ]]; then
        AUCMAX="--aucmax ${aucmax}"
    fi
    maemin=${maemin}
    if [[ -n "$maemin" ]]; then
        MAEMIN="--maemin ${maemin}"
    fi
    maemax=${maemax}
    if [[ -n "$maemax" ]]; then
        MAEMAX="--maemax ${maemax}"
    fi
    #start demo2
    #add verbose option
    if [[ ! -d "$WRAPPERDIR/dempy" ]]; then
        tar xzvf demonstrate.tgz
    fi
    python $WRAPPERDIR/dempy/demonstrate.py "${DIRECTORY} ${OUTPUT} ${SETTINGS} ${mode} ${XPOS} ${POSTITLE} ${XERROR} ${ERRORTITLE} ${EXTRA} ${AUCMIN} ${AUCMAX} ${MAEMIN} ${MAEMAX}"
else
    echo "Only demonstrate and demonstrate2 are supported" >&2
    exit 1
fi
