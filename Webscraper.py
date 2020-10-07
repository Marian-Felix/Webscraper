import re
import xlwt
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime


# set up .xls - sheet with xlwt module
wb = xlwt.Workbook()
sheet1 = wb.add_sheet('Sheet Nr 1')
first_col = sheet1.col(0)
first_col.width = 256 * 5 # ~5 characters wide
first_col.width
second_col = sheet1.col(1)
second_col.width = 256 * 100 # ~100 characters wide

style1 = xlwt.easyxf('font: bold 1, color green;') 
style2 = xlwt.easyxf('font: bold 1, color blue;') 
style3 = xlwt.easyxf('font: bold 1, color black;') 
style4 = xlwt.easyxf('font: italic 1, color black;') 

sheet1.write(0, 0, "Reduzierte Bücher zum Thema \'Softwareentwicklung\' von www.medimops.de", style1)
sheet1.write(1, 0, "https://www.medimops.de/buecher-fachbuecher-informatik-praktische-informatik-software-entwicklung-C0655742/", style4)
sheet1.write(3,1, "Titel", style2)
sheet1.write(3, 2, "Preis [€]", style2)
sheet1.write(3, 3, "Rabatt [%]", style2)


# URL of bargain book store, product section "software development"
my_url = "https://www.medimops.de/buecher-fachbuecher-informatik-praktische-informatik-software-entwicklung-C0655742/"

# website forbids access, but it works with added user agent and extended timeout:
# source: https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
req = Request(my_url, headers={'User-Agent': 'XYZ/3.0'})
webpage = urlopen(req, timeout=10).read()

# parse html
page_soup = BeautifulSoup(webpage, "html.parser")

# grab list of product containers
products = page_soup.findAll("div",{"class":"mx-product-list-item clearfix"})

# helper functions to extract number values from string
def get_priceNew(priceNew_container):
	priceNew_string = priceNew_container[0].text.strip()
	priceNew_string_numbers = re.findall(r'\b\d+\b', priceNew_string)
	priceNew_floatEuro = float(priceNew_string_numbers[0]+"."+priceNew_string_numbers[1])
	return priceNew_floatEuro

def get_discount(discount_container):
	discount_string = discount_container[0].text.strip()
	discount_string_numbers = re.findall(r'\b\d+\b', discount_string)
	discount_floatEuro = float(discount_string_numbers[0]+"."+discount_string_numbers[1])
	return discount_floatEuro

def get_discount_perCent(discount_container):
	discount_string = discount_container[0].text.strip()
	discount_string_numbers = re.findall(r'\b\d+\b', discount_string)
	discount_perCent = int(discount_string_numbers[2])
	return discount_perCent


# iterate through product containers, access information of individual products
i = 0
row = 4

for product in products:
	i += 1
	data_list = []
	title_container = product.findAll("div",{"class":"mx-product-list-item-title"})
	title = title_container[0].text.strip()
	
	priceNew_container = product.findAll("div", {"class": "mx-product-list-item-save"})
	priceNew = get_priceNew(priceNew_container)

	discount_container = product.findAll("div", {"class": "mx-product-list-item-discount-bottom mx-product-list-item-save"})
	discount_floatEuro = get_discount(discount_container)
	discount_perCent = get_discount_perCent(discount_container)
	# <span> object (html) of final price could not be accessed. Workaround with new price minus discount price
	priceFinal = round((priceNew-discount_floatEuro), 2)

	data_list.extend([i, title, priceFinal, discount_perCent])
	
	print("({}): {}\n      {} Euro (- {} %)".format(i, title, priceFinal, discount_perCent))
	
	# write gathered information of each book (stored in data_list) to .xls-table
	column = 0
	for column_value in data_list:
		if column == 1:
			sheet1.write(row, column, column_value, style3)
		else:
			sheet1.write(row, column, column_value)
		column += 1
	row += 1

	# state number of products being retrieved
	if i > 19:
		break

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y %H-%M-%S")

# save .xls-file with current date&time stamp
wb.save("Bücher-Discount   {}.xls".format(dt_string))
