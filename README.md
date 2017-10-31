Python is chosen to solve this challenge. 

The code is designed to create the medianvals_by_zip.txt while the data is streaming in. And the medianvals_by_date.txt is generated at the end section of the code.

The code design will be explained below, and the pseudo code will be used when necessary:

0. Framework

One for loop is used to get the data line by line and generate the values for output at the same time:

    for loop:
      write to medianvals_by_zip.txt if valid,
      cumulate the values for medianvals_by_date.txt
    
    output the medianvals_by_date.txt after sorting. 

1. Data structure

Two dictionaries (zip_dict, date_dict) are built to store the output data,  

    zip_dict = {(ID, zip) : [num, amount, A, B]}
    ID:     CMTE_ID of current record
    zip:    ZIP_CODE of current record
    num:    cumulated records number of this combination (ID, zip)
    amount: cumulated transaction value of this combination (ID, zip)
    A:      the heap contains the TRANSACTION_AMT less than the median
    B:      the heap contains the TRANSACTION_AMT larger than the median

date_dict has the same design as zip_dict.

1. Modules

Several modules are imported in this code:

    from sys import argv                # get the name of input and output files
    import heapq                        # use to calculate the median
    from datetime import datetime       # check the validity of TRANSACTION_DT 
    from operator import itemgetter     # sort the output for medianvals_by_date.txt
    import re                           # check the validity of CMTE_ID 
    
2. Input

The data is read by streaming as following:

    with open(infile) as datafile:
      for line in datafile:             # during this loop, medianvals_by_zip.txt is generated. medianvals_by_date.txt is output after this loop. 

While the data is streaming in line by line, the following five fields are picked by change the field separator to '|'.

    CMTE_ID: identity of the recipient, which is field[0],
    ZIP_CODE: zip code of the contributor (we only want the first five digits/characters), which is field[10][0:5],
    TRANSACTION_DT: date of the transaction, which is field[13],
    TRANSACTION_AMT: amount of the transaction, which is field[14],
    OTHER_ID: a field that denotes whether contribution came from a person or an entity, which is field[15].

3. Functions

Two functions are defined as follows to check the number validity and date validity:

    def number_check(x):
      try:
          float(x)
          return True
      except ValueError:
          return False

    def date_check(x):
      try:
          if x!=datetime.strptime(x,'%m%d%Y').strftime('%m%d%Y'):
              raise ValueError
          return True
      except ValueError:
          return False

4. Data clean

The entire record will be ignored if one of the following situation happens:

    OTHER_ID is not NULL,
    CMTE_ID does not match the specific format, (e.g. 'C00177436')
    TRANSACTION_AMT is not a valid number.

which can be done through one if command:

    if(other_ID or not ID_temp.match(ID) or not number_check(fields[14])): continue   # if ignored, go to the next iteration of the for loop.

If the ZIP_CODE is valid, this record will be used for medianvals_by_zip.txt. However, it is still used in medianvals_by_date.txt if it is not valid. 

    if(number_check(zip_curr) and len(zip_curr.strip())==5):
    
If the TRANSACTION_DT is valid, this record will be used for medianvals_by_date.txt. However, it is still used in medianvals_by_zip.txt if it is not valid. 

    if(date_check(date_curr)):

5. Calculating runnning median

Two heaps A and B are generated in which A contains the TRANSACTION_AMT less than the median and B contains the TRANSACTION_AMT larger than the median. Two restrictions are used to build heaps:

    All values in A must less than values in B.
    len(B) - len(A) = 0 or 1

The above requirements can be fulfilled through insertion process of new data:

    Insert the new data in B
    Move the minimum of B into A
    if(len(B)<len(A)):
      Move the maximum of A into B

After the insertion of each new data, the running median is computed:

    if(len(B)>len(A)):
      median = minimum of B
    if(len(B)==len(A)):
      median = (minimum of B + maximum of A)/2

Above process can be performed with heapq module. 

6. Output the sorted medianvals_by_date.txt through for loop

    for line in sorted(date_dict, key=itemgetter(0,1)):
