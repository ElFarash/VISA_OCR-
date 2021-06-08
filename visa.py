import cv2 
import pytesseract
from preprocessing import *
from pytesseract import Output
import re
from datetime import date

# date of today
today = date.today()

# loading the image
img = cv2.imread('image1.jpg')

# doing some preprocessing to the image to improve the text dection.
gray = get_grayscale(img)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)

# ocr
data = pytesseract.image_to_data(thresh,output_type=Output.DICT, config='config') # to get the confidence score 
n_words = len(data['text'])

# detecing the confidence score of the expiration date
data_pattern = "^([1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]$" #get any dates like: 24AUG2028
list_of_dates_scores = []
list_of_dates = []
for i in range(n_words):
	is_date = re.search(data_pattern,data['text'][i])
	if(is_date):
		list_of_dates.append(data['text'][i])
		list_of_dates_scores.append(data['conf'][i])

# detecting which date is the expiration date and extracting its year 
years= []
for date in list_of_dates:
	years.append(int(date[5:]))
expiration_date_year_index = years.index(max(years))

# setting the thershold of the confidence score to 65 but we can make it higher if we want.
if (list_of_dates_scores[expiration_date_year_index] > 65): 
	confidence = 'with high confidence'
else:
	confidence = "not sure"

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
	print("VALID VISA", confidence)
elif (years[expiration_date_year_index] < int(year_of_today)):
	print("INVALID VISA", confidence)
elif( years[expiration_date_year_index] == int(year_of_today)):
	if (month_dic[months[expiration_date_year_index]] > int(month_of_today)):
		print("VALID VISA", confidence)
	elif (month_dic[months[expiration_date_year_index]] < int(month_of_today)):
		print("INVALID VISA", confidence)
	elif (month_dic[months[expiration_date_year_index]] == int(month_of_today)):
		if (days[expiration_date_year_index] > int(day_of_today)):
			print("VALID VISA", confidence)
		elif (days[expiration_date_year_index] < int(day_of_today)):
			print("INVALID VISA", confidence)
		elif (days[expiration_date_year_index]== int(day_of_today)):
			print("YOUR VISA WILL EXPIRE TODAY", confidence)
