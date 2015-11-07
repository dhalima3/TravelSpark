import csv

with open('jetblue.csv', 'rb') as jetbluecvs:
    reader = csv.reader(jetbluecvs)
    expediaPackagePrice = []
    jetbluePackagePrice = []
    percentSavings = []
    out = open('jetblueresults', 'w')
    destination = ''
    destinationBefore = ''
    for row in reader:
        origin = row[0]
        destination = row[1]
        if (destinationBefore == '' or destination == destinationBefore):
            destinationBefore = row[1]
            expediaPackagePrice.append(float(row[6]))
            jetbluePackagePrice.append(float(row[7]))
            percentSavings.append(float(row[8][:-1]))
        else:
            averageExpediaPackagePrice = round(sum(expediaPackagePrice) / float(len(expediaPackagePrice)), 2)
            averageJetbluePackagePrice = round(sum(jetbluePackagePrice) / float(len(jetbluePackagePrice)), 2)
            averagePercentSavings = round(sum(percentSavings) / float(len(percentSavings)), 2)
            out.write(' '.join([origin, destination, str(averageExpediaPackagePrice), str(averageJetbluePackagePrice), str(averagePercentSavings)]))
            out.write("\n")
            destination = ''
            destinationBefore = ''
            expediaPackagePrice[:] = []
            jetbluePackagePrice[:] = []
            percentSavings[:] = []
