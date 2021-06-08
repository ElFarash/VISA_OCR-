import cv2 
import pytesseract
from preprocessing import *
from pytesseract import Output
import re
from datetime import date

# date of today
today = date.today()

img = cv2.imread('image2.jpg')

gray = get_grayscale(img)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)

# Adding custom options
# custom_config = r'--oem 3 --psm 6'
output = pytesseract.image_to_string(thresh, config='config')
lst = output.split()

# detecing all dates in the visa
list_of_dates = []
for elemnt in lst:
	data_pattern = "^([1-9]|1[0-9]|2[A-Z]|2[0-9]|3[0-1])[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]$"

	is_date = re.search(data_pattern,elemnt)
	if (is_date):
		list_of_dates.append(elemnt)

# extracting the year of expiration date 
years= []
for date in list_of_dates:
	years.append(int(date[5:]))
expiration_date_year_index = years.index(max(years)) #the biggest date has to be the expiration date (not issue date or birthdate)

# extracting the month of the expiration date 
month_dic = {"JAN":"01",
			"FEB":"02",
			"MAR":"03",
			"APR":"04",
			"MAY":"05",
			"JUN":"06",
			"JUL":"07",
			"AUG":"08",
			"SEP":"09",
			"OCT":"10",
			"NOV":"11",
			"DEC":"12" }

months= []
for date in list_of_dates:
	months.append(date[2:5])

# extracting the day of the expiration date 
days= []
for date in list_of_dates:
	days.append(date[:2])

#getting the current date
year_of_today = str(today)[0:4]
month_of_today = str(today)[5:6]
day_of_today = str(today)[8:]


print("Expiration date:",years[expiration_date_year_index],"-",month_dic[months[expiration_date_year_index]],"-",days[expiration_date_year_index])
print("Today's date:",today)

if (years[expiration_date_year_index] > int(year_of_today)):
	print("VALID VISA")
elif (years[expiration_date_year_index] < int(year_of_today)):
	print("INVALID VISA")
elif( years[expiration_date_year_index] == int(year_of_today)):
	if (month_dic[months[expiration_date_year_index]] > int(month_of_today)):
		print("VALID VISA")
	elif (month_dic[months[expiration_date_year_index]] < int(month_of_today)):
		print("INVALID VISA")
	elif (month_dic[months[expiration_date_year_index]] == int(month_of_today)):
		if (days[expiration_date_year_index] > int(day_of_today)):
			print("VALID VISA")
		elif (days[expiration_date_year_index] < int(day_of_today)):
			print("INVALID VISA")
		elif (days[expiration_date_year_index]== int(day_of_today)):
			print("YOUR VISA WILL EXPIRE TODAY")
