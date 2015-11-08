import csv
import sys

with open('jetblue.csv', 'rb') as jetbluecvs:
    reader = csv.reader(jetbluecvs)
    expediaPackagePrice = sys.maxint
    jetbluePackagePrice = sys.maxint
    percentSavings = 0
    out = open('jetblueresults', 'w')
    destination = ''
    destinationBefore = ''
    for row in reader:
        origin = row[0]
        destination = row[1]
        if (destinationBefore == '' or destination == destinationBefore):
            destinationBefore = row[1]
            if (expediaPackagePrice > float(row[6])):
                expediaPackagePrice = row[6]
            if (jetbluePackagePrice > float(row[7])):
                jetbluePackagePrice = row[7]
            if (percentSavings < float(row[8][:-1])):
                percentSavings = row[8]
        else:
            out.write(' '.join([origin, destination, str(expediaPackagePrice), str(jetbluePackagePrice), str(percentSavings)]))
            out.write("\n")
            destination = ''
            destinationBefore = ''
            expediaPackagePrice = sys.maxint
            jetbluePackagePrice = sys.maxint
            percentSavings = 0
