#!/usr/bin/env python3

import sys
import pandas as pd
import math
import logging as log
from utils import QUASI_IDENTIFIERS
from utils import QuasiIdHeaders as hd

# parameters used on normalization
DATE_FACTOR_DELTA    = 5
ZIP_FACTOR_DELTA     = 10
DEGREE_FACTOR_DELTA  = 2

# date format for input and output
DATE_FORMAT = '%d/%m/%Y'

def min_group_size(data: pd.DataFrame, cols : list[str]) -> int:
    return data.groupby(cols) \
               .count()       \
               .min()         \
               .iloc[0]

# functions used for normalization
def round_date(x, round_factor):
    if round_factor <= 20:
        value = 1 if round_factor == 20 else x.day - (x.day % round_factor)
        return x.replace(day = max(value, 1))
    elif round_factor <= 40:
        year_factor = int((round_factor - 20) / 5 * 10)
        new_year = x.year - (x.year % year_factor)
        return x.replace(day=1, month=1, year=new_year)
    else:
        return x

def rebase_degree(x, previous, current):
    factor = x / previous
    return int(round( factor * current, 0))

def calculate_init_degree(data : pd.DataFrame) -> int:
    max_value = data[hd.EDUCATION].max()
    log_value  = round(math.log2(max_value), 0)
    return 2 ** int(log_value)

# used to check k anonymity
def is_k_anomymous( data : pd.DataFrame, k : int ) -> bool:
    anonymity = min_group_size(data, QUASI_IDENTIFIERS)
    log.info("Testing for k-anonymity and got %d", anonymity)

    return anonymity >= k

# generalizes everything c:
def generalize_data(data : pd.DataFrame, k : int ) -> pd.DataFrame:
    data        = data.copy() # lets not alter the intial for some reason c:
    date_factor = 5
    zip_factor  = 10
    degree      = calculate_init_degree(data)
    new_degree  = degree / DEGREE_FACTOR_DELTA

    # print('init-degree:', degree)
    while min_group_size(data, [hd.BIRTHDAY]) < k:
        data[hd.BIRTHDAY] = data[hd.BIRTHDAY].apply(lambda x : round_date(x, date_factor))
        date_factor += DATE_FACTOR_DELTA

    while min_group_size(data, [hd.ZIP_CODE]) < k:
        data[hd.ZIP_CODE] = data[hd.ZIP_CODE].apply(lambda x : x - (x % zip_factor))
        zip_factor *= ZIP_FACTOR_DELTA

    while min_group_size(data, [hd.EDUCATION]) < k:
        data[hd.EDUCATION] = data[hd.EDUCATION].apply(lambda x : rebase_degree(x, degree, new_degree))
        degree     = max(new_degree, 1)
        new_degree = new_degree / DEGREE_FACTOR_DELTA

    date_group_size   = min_group_size(data, [hd.BIRTHDAY])
    degree_group_size = min_group_size(data, [hd.EDUCATION])
    zip_group_size    = min_group_size(data, [hd.ZIP_CODE])
    while not is_k_anomymous(data, k):

        smallest = min(date_group_size, degree_group_size, zip_group_size)
        print(date_group_size, degree_group_size, zip_group_size)
        if smallest == date_group_size:
            log.info("birth-date equals to min ... handling it")
            data[hd.BIRTHDAY] = data[hd.BIRTHDAY].apply(lambda x : round_date(x, date_factor))
            date_factor      += DATE_FACTOR_DELTA
            date_group_size   = min_group_size(data, [hd.BIRTHDAY])

        if smallest == zip_group_size:
            log.info("zip-code equals to min ... normalizing it")
            data[hd.ZIP_CODE] = data[hd.ZIP_CODE].apply(lambda x : x - (x % zip_factor))
            zip_factor       *= ZIP_FACTOR_DELTA
            zip_group_size    = min_group_size(data, [hd.ZIP_CODE])

        if smallest == degree_group_size:
            log.info("education equals to min ... normalizing it")
            data[hd.EDUCATION] = data[hd.EDUCATION].apply(lambda x : rebase_degree(x, degree, new_degree))
            degree             = max(new_degree, 1)
            new_degree         = new_degree / DEGREE_FACTOR_DELTA
            degree_group_size  = min_group_size(data, [hd.EDUCATION])

    return data

def eprint( msg : str ):
    print(msg, file=sys.stderr)

def main(args : list[str]):
    if len(args) < 4:
        eprint("Error: missing arguments")
        eprint(f"usage: {args[0]} <input-dataset> <k> <output-file>")
        sys.exit(1)

    log.basicConfig(level=log.INFO, format="%(levelname)s: %(message)s")

    filename = args[1]
    k = int(args[2])
    out_filename= args[3]

    data = pd.read_csv(
        filename, 
        parse_dates=[hd.BIRTHDAY], 
        date_format=DATE_FORMAT
    )

    generalized = generalize_data(data, k)
    generalized.to_csv(
        out_filename, 
        index=False, 
        date_format=DATE_FORMAT
    )

if __name__ == '__main__':
    main(sys.argv)
