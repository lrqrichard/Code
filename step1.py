import csv
import datetime

csvfile1 = open('jan2may.csv','w',newline='')
csvfile2 = open('june.csv','w',newline='')
fieldnames = ['User_id','Merchant_id','Coupon_id','Discount_req','Discount_rate','Distance','Date_received','Use']
writer1 = csv.DictWriter(csvfile1,fieldnames=fieldnames)
writer2 = csv.DictWriter(csvfile2,fieldnames=fieldnames)
f = open('offline_train.csv','r')
for line in f:
	User_id,Merchant_id,Coupon_id,Discount_rate,Distance,Date_received,Date = line.split(",")
	User_id = User_id.strip()
	Merchant_id = Merchant_id.strip()
	Coupon_id = Coupon_id.strip()
	Discount_rate = Discount_rate.strip()
	Distance = Distance.strip()
	Date_received = Date_received.strip()
	Date = Date.strip()
	if Coupon_id != 'null':
		flag = 0
		for i in range(len(Discount_rate)):
			if Discount_rate[i] == ':':
				Discount_req = Discount_rate[:i]
				Discount_val = Discount_rate[i+1:]
				req = int(Discount_req)
				val = int(Discount_val)
				rate = 1-val/req
				Discount_r = str('%.3f'%rate)
				flag = 1
				if req < 15:
					Discount_req = '(0-15)'
				elif req < 25:
					Discount_req = '[15-25)'
				elif req < 40:
					Discount_req = '[25-40)'
				elif req < 75:
					Discount_req = '[40-75)'
				elif req < 125:
					Discount_req = '[75-125)'
				elif req < 250:
					Discount_req = '[125-250)'
				else:
					Discount_req = '[250-MAX)'
		if flag == 0:
			Discount_r = Discount_rate
			Discount_req = 'discount'
		if Distance == 'null':
			Distance = '?'
		Use = '0'
		if Date != 'null':		
			date_rec = datetime.datetime.strptime(Date_received,'%Y%m%d')
			date_use = datetime.datetime.strptime(Date,'%Y%m%d')
			delta = date_use-date_rec
			if delta.days <= 15:
				Use = '1'
		dat = int(Date_received[-3:-2])
		if dat < 6:
			writer1.writerow({'User_id':User_id,'Merchant_id':Merchant_id,'Coupon_id':Coupon_id,'Discount_req':Discount_req,'Discount_rate':Discount_r,'Distance':Distance,'Date_received':Date_received,'Use':Use})			
		if dat == 6:
			writer2.writerow({'User_id':User_id,'Merchant_id':Merchant_id,'Coupon_id':Coupon_id,'Discount_req':Discount_req,'Discount_rate':Discount_r,'Distance':Distance,'Date_received':Date_received,'Use':Use})
csvfile1.close()
csvfile2.close()
f.close()