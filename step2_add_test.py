import csv
import datetime
import math

class User:
	def __init__(self):
		self.id = 0
		self.record = []
	def addrecord(self,dat,mer_id,get,buy):
		self.record.append((dat,mer_id,get,buy))

class Merchant:
	def __init__(self):
		self.id = 0
		self.record = []
	def addrecord(self,dat,user_id):
		self.record.append((dat,user_id))
		
p = [User() for x in range(0,8000000)]
m = [Merchant() for x in range(0,9000)]

f = open('offline_train.csv.','r')
for line in f:
	User_id,Merchant_id,Coupon_id,Discount_rate,Distance,Date_received,Date = line.split(",")
	User_id = User_id.strip()
	Merchant_id = Merchant_id.strip()
	Coupon_id = Coupon_id.strip()
	Date_received = Date_received.strip()
	Date = Date.strip()
	dat_r = 999
	dat_b = 999
	user_id = int(User_id)
	mer_id = int(Merchant_id)
	if Date_received != 'null':
		dat_r = int(Date_received[-3:])
	if Date != 'null':
		dat_b = int(Date[-3:])
	if p[user_id].id == '0':
		p[user_id].id = user_id	
	if Date != 'null':
		if m[mer_id].id == '0':
			m[mer_id].id = mer_id
		m[mer_id].addrecord(dat_b,user_id)	
	if Coupon_id == 'null':
		p[user_id].addrecord(dat_b,mer_id,0,1)
	if Coupon_id != 'null':
		flag = 0
		if Date != 'null':		
			date_rec = datetime.datetime.strptime(Date_received,'%Y%m%d')
			date_use = datetime.datetime.strptime(Date,'%Y%m%d')
			delta = date_use-date_rec
			if delta.days <= 15:
				p[user_id].addrecord(dat_b,mer_id,1,1)
				flag = 1
		if flag == 0:
			p[user_id].addrecord(dat_r,mer_id,1,0)
f.close()

csvfile = open('jan2june_3.csv','w',newline='')
fieldnames = ['User_id','Merchant_id','Coupon_id','Use_rate','Merchant_times','Other_times','Discount_req','Discount_rate','Distance','Date_received','Use']
writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
f = open('jan2june.csv')
for line in f:
	User_id,Merchant_id,Coupon_id,Discount_req,Discount_rate,Distance,Date_received,Use = line.split(",")
	User_id = User_id.strip()
	Merchant_id = Merchant_id.strip()
	Coupon_id = Coupon_id.strip()	
	Date_received = Date_received.strip()
	Use = Use.strip()
	user_id = int(User_id)
	mer_id = int(Merchant_id)
	dat = int(Date_received[-3:])
	if p[user_id].id == '0':
		Use_rate = '?'
		Merchant_times = '0'
		Other_times = '0'
	else:
		get_num = 0
		use_num = 0
		mer_num = 0
		for i in range(len(p[user_id].record)):
			if p[user_id].record[i][1] == mer_id and p[user_id].record[i][0] < dat and p[user_id].record[i][3] == 1:
				mer_num += 1
			if p[user_id].record[i][0] < dat and p[user_id].record[i][2] == 1:
				get_num += 1
				if p[user_id].record[i][3] == 1:
					use_num += 1
		if get_num == 0:
			Use_rate = '?'
		else:
			rate = use_num/get_num
			Use_rate = str('%.3f'%rate)
		if mer_num > 1:
			log_mer_num = round(math.log(mer_num))
		else:
			log_mer_num = mer_num
		Merchant_times = str(log_mer_num)
		a = []
		b = []
		other_buy = 0
		for i in range(len(p[user_id].record)):
			if p[user_id].record[i][1] != mer_id and p[user_id].record[i][0] < dat and p[user_id].record[i][3] == 1:
				other_mer = p[user_id].record[i][1]
				flag1 = 0
				for c in range(len(a)):
					if a[c] == other_mer:
						flag1 = 1
				if flag1 == 0:
					a.append(other_mer)
					for j in range(len(m[other_mer].record)):
						if m[other_mer].record[j][1] != user_id and m[other_mer].record[j][0] < dat:
							other_user = m[other_mer].record[j][1]
							flag2 = 0
							for d in range(len(b)):
								if b[d] == other_user:
									flag2 = 1
							if flag2 == 0:
								b.append(other_user)
								for k in range(len(p[other_user].record)):
									if p[other_user].record[k][1] == mer_id and p[other_user].record[k][0] < dat and p[other_user].record[k][3] == 1:
										other_buy += 1
		if other_buy > 1:
			log_other_buy = round(math.log(other_buy))
		else:
			log_other_buy = other_buy
		Other_times = str(log_other_buy)			
	writer.writerow({'User_id':User_id,'Merchant_id':Merchant_id,'Coupon_id':Coupon_id,'Use_rate':Use_rate,'Merchant_times':Merchant_times,'Other_times':Other_times,'Discount_req':Discount_req,'Discount_rate':Discount_rate,'Distance':Distance,'Date_received':Date_received,'Use':Use})
csvfile.close()
f.close()

csvfile = open('july_3.csv','w',newline='')
fieldnames = ['User_id','Merchant_id','Coupon_id','Use_rate','Merchant_times','Other_times','Discount_req','Discount_rate','Distance','Date_received','Use']
writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
f = open('july.csv')
for line in f:
	User_id,Merchant_id,Coupon_id,Discount_req,Discount_rate,Distance,Date_received,Use = line.split(",")
	User_id = User_id.strip()
	Merchant_id = Merchant_id.strip()
	Coupon_id = Coupon_id.strip()
	Date_received = Date_received.strip()
	Use = Use.strip()
	user_id = int(User_id)
	mer_id = int(Merchant_id)
	dat = int(Date_received[-3:])
	if p[user_id].id == '0':
		Use_rate = '?'
		Merchant_times = '0'
		Other_times = '0'
	else:
		get_num = 0
		use_num = 0
		mer_num = 0
		for i in range(len(p[user_id].record)):
			if p[user_id].record[i][1] == mer_id and p[user_id].record[i][0] < dat and p[user_id].record[i][3] == 1:
				mer_num += 1
			if p[user_id].record[i][0] < dat and p[user_id].record[i][2] == 1:
				get_num += 1
				if p[user_id].record[i][3] == 1:
					use_num += 1
		if get_num == 0:
			Use_rate = '?'
		else:
			rate = use_num/get_num
			Use_rate = str('%.3f'%rate)
		if mer_num > 1:
			log_mer_num = round(math.log(mer_num))
		else:
			log_mer_num = mer_num
		Merchant_times = str(log_mer_num)
		a = []
		b = []
		other_buy = 0
		for i in range(len(p[user_id].record)):
			if p[user_id].record[i][1] != mer_id and p[user_id].record[i][0] < dat and p[user_id].record[i][3] == 1:
				other_mer = p[user_id].record[i][1]
				flag1 = 0
				for c in range(len(a)):
					if a[c] == other_mer:
						flag1 = 1
				if flag1 == 0:
					a.append(other_mer)
					for j in range(len(m[other_mer].record)):
						if m[other_mer].record[j][1] != user_id and m[other_mer].record[j][0] < dat:
							other_user = m[other_mer].record[j][1]
							flag2 = 0
							for d in range(len(b)):
								if b[d] == other_user:
									flag2 = 1
							if flag2 == 0:
								b.append(other_user)
								for k in range(len(p[other_user].record)):
									if p[other_user].record[k][1] == mer_id and p[other_user].record[k][0] < dat and p[other_user].record[k][3] == 1:
										other_buy += 1
		if other_buy > 1:
			log_other_buy = round(math.log(other_buy))
		else:
			log_other_buy = other_buy
		Other_times = str(log_other_buy)
	writer.writerow({'User_id':User_id,'Merchant_id':Merchant_id,'Coupon_id':Coupon_id,'Use_rate':Use_rate,'Merchant_times':Merchant_times,'Other_times':Other_times,'Discount_req':Discount_req,'Discount_rate':Discount_rate,'Distance':Distance,'Date_received':Date_received,'Use':Use})
csvfile.close()
f.close()