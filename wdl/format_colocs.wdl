workflow format_coloc {

    Array[File] input_files
    Boolean add_displayname
    Boolean reorder_columns
    Boolean remove_pvals_from_vars_info_column

    scatter ( f1 in input_files ){

        # add displayname if specified
        if (add_displayname) {
            call add_displayname_column {
                input:  file = f1
            }
        }
        File f2 = select_first([add_displayname_column.out, f1]) 

        # reorder columns if specified
        if (reorder_columns) {
            call reorder {
                input:  file = f2
            }
        }
        File f3 = select_first([reorder.out_reordered, f2]) 

        # remove pvals from vars info column if specified
        if (remove_pvals_from_vars_info_column) {
            call remove_pvals {
                input:  file = f3
            }
        }
        File f4 = select_first([remove_pvals.out_removed_pvals, f3]) 
    }

    output{
        Array[File] formatted_coloc_files =  f4
    }
    
}


task add_displayname_column {
    
    File file
    File src2_displayname_map
    String fout = basename(file)
    Int disk_size = ceil(size(file, "GB")) * 5 + 10

    command <<<

    echo "`date` start"
    zcat "${file}" | cut -f 2 | gzip > "source2_col.gz"

    echo "`date` map"
    python << CODE 

    import pandas as pd

    ## read data
    data = pd.read_csv("source2_col.gz", compression = "infer")

    ## read displayname mapping file
    displayname = pd.read_csv("${src2_displayname_map}",sep = "\t")

    ## if some sources are missing from the displayname map, leave source2 value
    d = list(set(data['source2']).difference(set(displayname['source2'])))
    src_add = pd.DataFrame(list(zip(d, d)), columns=['source2', 'source2_displayname'])
    mapdata = pd.concat([displayname, src_add])

    if len(d) > 0:
        print("Sources not mapped: ", d, " - use value from source2 column as is")

    ## reindex mapping data frame
    mapdata.index = mapdata['source2']

    ## match prepared data
    data['source2_displayname'] = mapdata.loc[data['source2']]['source2_displayname'].values
    data['source2_displayname'].to_csv("mapped_col.gz", sep = "\t", index = False, compression='gzip')

    CODE

    echo "`date` combine columns"

    ## add a column to the input file
    paste <(zcat "${file}") <(zcat "mapped_col.gz") | gzip > "${fout}"

    echo "`date` done"

    >>>

    output {
        File out = "${fout}"
    }

    runtime {
        docker: "amancevice/pandas:slim"
        cpu: "1"
        memory: "8 GB"
        disks: "local-disk ${disk_size} HDD"
        zones: "europe-west1-b europe-west1-c europe-west1-d"
        preemptible: "1"
    }
}


task reorder {

    File file
    String cols_order
    String fout = basename(file)
    Int disk_size = ceil(size(file, "GB")) * 5 + 10

    command <<<

        fields="";
        for col in $(echo ${cols_order} | tr ',' '\t')
        do
            colnumb=$(zcat ${file} | head -1 | tr '\t' '\n' | grep -w $col -n | cut -f 1 -d':');
            [ -z "$colnumb" ] || fields=$(echo $fields)"\$$colnumb,";
        done
        fields=$(echo "$fields" | sed 's/.$//');
        
        zcat ${file} | awk -v fields=fields -v OFS="\t" -F"\t" '{print '$fields'}' | gzip > ${fout};
        
    >>>

    output {
        File out_reordered =  "${fout}"
    }
    
    runtime {
        docker: "ubuntu:latest"
        cpu: "1"
        memory: "2 GB"
        disks: "local-disk ${disk_size} HDD"
        zones: "europe-west1-b europe-west1-c europe-west1-d"
        preemptible: "1"
    }
}


task remove_pvals {

    File file
    String fout = basename(file)
    Int disk_size = ceil(size(file, "GB")) * 5 + 10

    command <<<

    zcat ${file} | awk '
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
    } ' | gzip > "${fout}";

    >>>

    output {
        File out_removed_pvals = "${fout}"
    }

    runtime {
        docker: "ubuntu:latest"
        cpu: "1"
        memory: "8 GB"
        disks: "local-disk ${disk_size} HDD"
        zones: "europe-west1-b europe-west1-c europe-west1-d"
        preemptible: "1"
    }

}
