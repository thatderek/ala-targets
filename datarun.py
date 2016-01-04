#/usr/bin/python

import csv 
from collections import defaultdict
from operator import itemgetter
from prettytable import PrettyTable

def extractDonations(filename, zips):
    tempDonations = []
    with open(filename, 'rb') as itcont:
            itreader = csv.reader(itcont, delimiter='|')
            n = 0
            for x in itreader:
                n = n+1
                ## if the first five digits of the zip code 
                ## (negating the +4) match the ziplist
                if x[10][0:5] in zips:
                    tempDonations.append(x)
    return tempDonations

def extractCommittees(filename):
    committeeDict = defaultdict(list)

    with open(filename, 'rb') as cm:
        cmreader = csv.reader(cm, delimiter='|')
        for c in cmreader:
            committeeDict[c[0]].append(c)
    return committeeDict



def main():
    zips = []
    with open('./zips.txt', 'rb') as zipsfile:
        zips_temp = zipsfile.readlines()
        for z in zips_temp: 
            zips.append(z.rstrip('\n'))


    committeeDict = defaultdict(list)
    cmFilenames = [
            "./cm.txt", 
            "./cm12.txt",
            "./cm14.txt"
            ]
    for f in cmFilenames:
        committeeDict.update(extractCommittees(f))
           
    alachuaDonations = []

    filenameList = [
            "./itcont.txt",
            "./itcont12.txt",
            "./itcont14.txt"
            ]

    for f in filenameList: 
        alachuaDonations.extend(extractDonations(f, zips))

    
    donationsDict = defaultdict(list)

    for d in alachuaDonations:
        ## zipStripped + lastname
        zipPlusLastName = d[10][0:5]+ d[7].split(",")[0]
        donationsDict[zipPlusLastName].append(d)

    donationAmts = []

    for k in donationsDict.keys():
        subttl = 0
        for d in donationsDict[k]:
            subttl = subttl + int(d[14])
        tup = (k, subttl)
        donationAmts.append(tup)
    fecN = 1
    for tup in sorted(donationAmts, key=itemgetter(1), reverse=True):
        print "\nKey: FEC-ALA-" +str(fecN).zfill(4), " Total: ", tup[1], " FEC-Key: ", tup[0]
        fecN = fecN+1
        t = PrettyTable(["Amount", "Date", "Name", "City", "Occupation", "Employer", "Committee"]) 
        t.align["Amount"] = "r"
        t.padding_width = 1
        t.sortby = "Date"
        for d in donationsDict[tup[0]]:
            t.add_row([d[14], d[13][4:]+d[13][0:4], d[7], d[8], d[12], d[11],  committeeDict[d[0]][0][1]])
        print t.get_html_string()

if __name__ == '__main__':
    main()
