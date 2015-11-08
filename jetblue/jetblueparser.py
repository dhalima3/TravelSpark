f = open("jetblueresults", 'r')
lowest_prices = []

first_line = f.readline().split(',')
current_lowest_city_price = first_line[1]
current_lowest_city_percentage = first_line[1]
current_lowest_price = float(first_line[4])
print first_line[5].rstrip('%')
current_lowest_percentage = float(first_line[5].replace('%', ""))

for line in f:
	split_line = line.split(',')
	if(float(split_line[4]) < current_lowest_price and split_line[1] != "CUR" and split_line[1] != "SXM"):
		current_lowest_price = float(split_line[4])
		current_lowest_city_price = split_line[1]

	if(float(split_line[5].replace('%', '')) > current_lowest_percentage):
		current_lowest_percentage = float(split_line[5].replace('%',''))
		current_lowest_city_percentage = split_line[1]

print "Lowest Price"
print current_lowest_city_price
print current_lowest_price
print "Highest Percentage Savings"
print current_lowest_city_percentage
print current_lowest_percentage