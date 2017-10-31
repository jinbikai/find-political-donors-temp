from sys import argv
import heapq
from datetime import datetime
from operator import itemgetter
import re

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


infile = argv[1]
zip_out = argv[2]
date_out = argv[3]
ID_temp = re.compile("C[0-9]{8}")

out_zip = open(zip_out,'w')
out_date = open(date_out,'w')

zip_dict = {}
date_dict = {}

with open(infile) as datafile:

    for line in datafile:
        fields=line.split('|')
        ID = fields[0]
        zip_curr = fields[10][0:5]
        date_curr = fields[13]
        other_ID = fields[15]
        if(other_ID or not ID_temp.match(ID) or 
                not number_check(fields[14])): continue
        amount = float(fields[14])

        if(number_check(zip_curr) and len(zip_curr.strip())==5):
            if( (ID,zip_curr) not in zip_dict):
                zip_dict[ID,zip_curr] = [1, amount, [], [amount]]
                # since round(0.5)==0 in my python version, 
                # the rounded up is done by int()
                print(ID, zip_curr, int(amount+0.5), 1, 
                        int(amount+0.5), sep=('|'), file=out_zip) 
            else:
                zip_dict[ID,zip_curr][0] += 1
                zip_dict[ID,zip_curr][1] += amount
                heapq.heappush(zip_dict[ID,zip_curr][2], 
                        heapq.heappushpop(zip_dict[ID,zip_curr][3],amount))
                if(len(zip_dict[ID,zip_curr][2])>len(zip_dict[ID,zip_curr][3])):
                    heapq.heappush(zip_dict[ID,zip_curr][3], 
                            heapq.nlargest(1,zip_dict[ID,zip_curr][2])[0])
                if(len(zip_dict[ID,zip_curr][2])<len(zip_dict[ID,zip_curr][3])):
                    zip_m = heapq.nsmallest(1,zip_dict[ID,zip_curr][3])[0]
                if(len(zip_dict[ID,zip_curr][2])==len(zip_dict[ID,zip_curr][3])):
                    zip_m = (heapq.nsmallest(1,zip_dict[ID,zip_curr][3])[0] + 
                            heapq.nlargest(1,zip_dict[ID,zip_curr][2])[0])/2
                print(ID, zip_curr, int(zip_m+0.5), zip_dict[ID,zip_curr][0], 
                        int(zip_dict[ID,zip_curr][1]+0.5), sep='|', file=out_zip)

        if(date_check(date_curr)):
            if( (ID,date_curr) not in date_dict):
                date_dict[ID,date_curr] = [1, amount, [], [amount]]
            else:
                date_dict[ID,date_curr][0] += 1
                date_dict[ID,date_curr][1] += amount
                heapq.heappush(date_dict[ID,date_curr][2], 
                        heapq.heappushpop(date_dict[ID,date_curr][3],amount))
                if(len(date_dict[ID,date_curr][2])>len(date_dict[ID,date_curr][3])):
                    heapq.heappush(date_dict[ID,date_curr][3], 
                            heapq.nlargest(1,date_dict[ID,date_curr][2])[0])


for line in sorted(date_dict, key=itemgetter(0,1)):
    if(len(date_dict[line][2])<len(date_dict[line][3])):
        date_m = heapq.nsmallest(1,date_dict[line][3])[0]
    if(len(date_dict[line][2])==len(date_dict[line][3])):
        date_m = (heapq.nsmallest(1,date_dict[line][3])[0] + 
                heapq.nlargest(1,date_dict[line][2])[0])/2
    print(line[0], line[1], int(date_m+0.5), date_dict[line][0],
            int(date_dict[line][1]+0.5), sep='|', file=out_date)

out_zip.close()
out_date.close()
