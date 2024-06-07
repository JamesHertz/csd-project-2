#!/usr/bin/env python3


import sys
import pandas as pd
from os import path


def print_stats( marriage : pd.DataFrame, nif_occurences : pd.Series ):
    print('--------------------------------------')
    print('Some interstings status about NIFs :')
    print('--------------------------------------')
    original_size       = marriage['NIF'].value_counts().size
    unique_individuals  = nif_occurences[ nif_occurences == 1].size
    success             = nif_occurences[ nif_occurences <= 3].size

    print('Original NIF number                                   :', original_size)
    print('Uniquely identified NIFs                              : %d (%.2f%%)' % (unique_individuals, unique_individuals / original_size * 100) )
    print('Successfully identified NIFs (occurrence of NIF <= 3) : %d (%.2f%%)'  % (success, success / original_size * 100) )
    print()

def filename_for_unique_nifs( original_output_file : str ) -> str:
    dirname  = path.dirname(original_output_file)
    basename = path.basename(original_output_file)

    filename = 'unique-nifs-' + basename
    return filename if dirname == '' else dirname + path.sep + filename


def main( args : list[str] ):
    if len(args) < 5:
        print(
            f"usage: {args[0]} <initial-dataset> <marriage-dataset> <earnings-dataset> <output-file>", file=sys.stderr
        )
        sys.exit(1)

    data     = pd.read_csv(args[1])
    marriage = pd.read_csv(args[2])
    earnings = pd.read_csv(args[3])

    output_file = args[4]


    linked = pd.merge(
        # join marriage and earnings on 'Date of Birth' and 'Education Status'
        marriage, pd.merge(data, earnings, on = ['Date of Birth', 'Education Status' ], how = 'outer' ), 
        # Then join the result of the previous with this on 'Postal Code' and 'Occupation'
        on = ['Postal Code', 'Occupation'], how = 'inner' 
    )


    nif_occurences = linked['NIF'].value_counts()
    print_stats(marriage, nif_occurences)

    linked.to_csv(output_file, index=False)
    print(f"Saved linked data in '{output_file}'.")

    unique_filename = filename_for_unique_nifs(output_file)
    unique_data    = linked[ 
        linked['NIF'].isin(
            nif_occurences[ nif_occurences == 1].index.to_list()
        )
    ]

    unique_data.to_csv(unique_filename, index=False)
    print(f"Saved filtered data of uniquely identifed nifs '{unique_filename}'.")

if __name__ == '__main__':
    main(sys.argv)
