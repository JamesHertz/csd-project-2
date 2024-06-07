#!/usr/bin/env python3

import sys
import pandas as pd



def eprint( msg : str ):
    print(msg, file=sys.stderr)

def generalize_data( data : pd.DataFrame, k : int ):


    pass

def main(args : list[str]):
    if len(args) < 3:
        eprint("Error: missing arguments")
        eprint(f"usage: {args[0]} <input-dataset> <k> <output-file>")
        sys.exit(1)

    filename = args[1]
    k = int(args[2])


    data = pd.read_csv(
        filename, 
        parse_dates=[Qi.BIRTH_DAY], 
        date_format='%d/%m/%Y'
    )

    generalize_data(data, k)



    # print(
    #     data[Qi.BIRTH_DAY].dt.month
    # )
    
    # print('This tests assumes that quasi identifiers are:\n-', '\n- '.join(QUASI_IDENTIFIERS))
    # print()
    #
    # groups = data.groupby( QUASI_IDENTIFIERS ).count()
    # min_group_size = groups.min().iloc[0]
    #
    # if min_group_size < k:
    #     print(f'This dataset is not k anonymous for k = {k}')
    #     print('Here is a small sample of the groups size (look at the last row): ')
    #     print(groups.head().iloc[:, 0])
    # else:
    #     max_group_size = groups.max().iloc[0]
    #     print(f'This dataset is not k anonymous for k = {k} groups size ranging in [{min_group_size}, {max_group_size}]')
    # # print(min_group_size)
    # # print(groups)
    # print(groups.min()[0])

    




if __name__ == '__main__':
    main(sys.argv)