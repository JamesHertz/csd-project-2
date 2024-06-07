# Privacy CSD project option 1

## Part-1
Please go to the folder named `part-1/` and you will find a python program and a jupyter notebook. The jupyter notebook has some charts if you want to check them up. As for the python program, its pretty much straight forward. Please just run the script provinding no argument at all and it will tel you what it is expecting.

## Part 2
Regarding testing and checking for k-anonymity you can find the programs that does that in the folder `part-2/`. Just run the scripts with no arguments and they will tell you what they expected. Please if some error pops up be sure you passed the parameters well (I didn't do validations for the sake of time).

As stated in the project assignment I performed the checks and the normalization and the results I got were:
```bash
$ ./check-k-anonymity.py ../data/sti_data.csv 2
This tests assumes that quasi identifiers are:
- Date of Birth
- Postal Code
- Education Status

This dataset is not k anonymous for k = 2
Here is a small sample of the groups size (look at the last row):
Date of Birth  Postal Code  Education Status
01/01/1954     1900         10                  1
01/01/1955     2367         7                   1
01/01/1957     1364         9                   1
01/01/1958     1358         9                   1
01/01/1959     1428         9                   1
Name: Chlamydia, dtype: int64

$ ./normalize-for-k.py ../data/sti_data.csv 2 k-anonymous-data/for-k-2.csv
... bunch of unimportant stuffs ...
$ ./check-k-anonymity.py k-anonymous-data/for-k-2.csv 2
This tests assumes that quasi identifiers are:
- Date of Birth
- Postal Code
- Education Status

This dataset is k anonymous for k = 2, with groups size ranging in [3, 305]

$ ./normalize-for-k.py k-anonymous-data/for-k-2.csv 4 k-anonymous-data/for-k-4.csv
... bunch of unimportant stuffs ...
$ ./check-k-anonymity.py k-anonymous-data/for-k-4.csv 4
This tests assumes that quasi identifiers are:
- Date of Birth
- Postal Code
- Education Status

This dataset is k anonymous for k = 4, with groups size ranging in [88, 2725]
```

And so I finished having a dataset normalized with for k = 88 c:
