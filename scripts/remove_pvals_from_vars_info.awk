#!/bin/awk -f

BEGIN{FS=OFS="\t"}
NR==1 {
    for(i = 1; i <= NF; i++) {
        h[$i]=i;
    }
    print;
}
NR>1 {
    vlen = split($h["vars1_info"], vars1_info, ";");
    newv = "";
    for(i = 1; i <= vlen; i++) {
        split(vars1_info[i], v ,",");
        if (newv == "") {
            newv = v[1] "," v[2] "," v[3];
        } else {
            newv = newv ";" v[1] "," v[2] "," v[3];
        }
    }
    $h["vars1_info"] = newv;

    vlen = split($h["vars2_info"], vars2_info, ";");
    newv = "";
    for(i = 1; i <= vlen; i++) {
        split(vars2_info[i], v ,",");
        if (newv == "") {
            newv = v[1] "," v[2] "," v[3];
        } else {
            newv = newv ";" v[1] "," v[2] "," v[3];
        }
    }
    $h["vars2_info"] = newv;
    print;
}