import pandas as pd
import numpy
import math
import csv
# خواندن داده از فایل Excel
df = pd.read_excel('ALL-APPROACHS3.XLSX', sheet_name='Sheet1-2')

# محاسبه تعداد ردیف‌ها
num_rows = df.shape[0]

# تعریف متغیرهای برای مقادیر مورد نیاز
coefficient=df.iloc[2:3, 13].values
percentageData =100- (df.iloc[0:1, 14].values*200)
percentage = df.iloc[18984:18985, 20].values
lenghtCandles = df.iloc[18981:18982, 18].values



g_high = df.iloc[2:18983, 1].values
g_low = df.iloc[2:18983, 2].values

b_max = df.iloc[2:18983, 15].values
b_min = df.iloc[2:18983, 16].values

coefficientZarars=[1,2,3,4,5,6,7,8,9,10] # =1/AO4     طول بزرگترین کندل پیشبینی=13.5   13.5*6*0.01*100=81
# حداکثر 81 دلار در هر معامله در ریسک خواهد بود  یعنی کمتر از 10 درصد
aboveT=1


  
for coefficientZarar in coefficientZarars:
    list1=[]
    base_balance=1000 #$$$
    initial_balance=1000


    #volume = 0.1
    profit=0
    p1=0
    p2=0
    p3=0
    p4=0
    p5=0
    p6=0
    p7=0
    p8=0
    p9=0
    p10=0
    p11=0
    p12=0
    p13=0
    p14=0



    profitP1=0
    profitP2=0
    profitP3=0
    profitP4=0
    profitP5=0
    profitP6=0
    profitP7=0
    profitP8=0
    profitP9=0
    profitP10=0
    profitP11=0
    profitP12=0
    profitP13=0
    profitP14=0
    
    broker=0.3
    perINmonth=[]
    perINmonth1=[]
    perINmonth2=[]
    maxVolume=0
    maxcondle=0
    maxrisk=0
    maxriskP=0
    volume=0.01
    s2break=""
    list3=[]
    for i in range(1,12000):
                list3.append(initial_balance)

                maxcondle=b_max[i]-b_min[i]
                risk=coefficientZarar *(maxcondle+broker)*volume*100
                if risk>maxrisk:
                    maxrisk=risk
                    maxriskP=risk/initial_balance
                #print(i,coefficientZarar,maxrisk ,initial_balance)
                #input()

                r_max=b_max[i]+((b_max[i] - b_min[i])* coefficientZarar)
                r_min=b_min[i]-((b_max[i] - b_min[i])* coefficientZarar)


                if i%990==0:

                    #print("{{{{{{{     ", initial_balance , "      }}}}}}}}}")
                    perINmonth1.append(initial_balance)
                    if i==990:
                        perINmonth.append(initial_balance-base_balance)
                    else:
                        perINmonth.append(initial_balance-base_balance-perINmonth[-1])
                    if i==990:
                        perINmonth2.append((initial_balance-base_balance)*100/base_balance)
                    else:
                        perINmonth2.append(round((perINmonth[-1])*100/perINmonth1[-1],2))
                    #print(perINmonth1)
                    #print(perINmonth)
                    #print(perINmonth2)
                    #input()    
                volume=((initial_balance-base_balance)/100000) #start with  0.01  for  more than 1000$
                #start with  0.01   
                volume=round(volume,2)
                if volume<0.01 :
                    volume=0.01 
                if i==1:
                    minVolume=volume
                if volume> maxVolume :    
                    maxVolume=volume 
                
                #print(i, "   volume : "  ,volume   )
                #input()
                

                zarar= coefficientZarar *(b_max[i] - b_min[i]+broker)
                if zarar<aboveT:
                    zarar=aboveT
                #print("zarar",zarar)    

                    
                    
                if b_max[i] - b_min[i]>aboveT  and  b_min[i] > g_low[i]  and  b_max[i] < g_high[i]  and  r_max>g_high[i]  and  r_min< g_low[i]  :
                    profit = (b_max[i] - b_min[i]-broker) * volume *100
                    initial_balance += profit
                    
                    profitP1 += profit
                    p1+=1
                    #print(i,"___________p1____",p1 ,"  *******  ",profit , b_max[i] , b_min[i]  )
                    list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p1"]
                elif b_max[i] - b_min[i]>aboveT  and  b_min[i] > g_low[i]  and  b_max[i] < g_high[i]  and  r_max<g_high[i]  and  r_min> g_low[i]  :    
                    profit = -zarar * volume *100 # ضرر
                    initial_balance += profit
                    profitP2 += profit
                    p2+=1
                    #print(i,"___________p2____",p2,"  *******  ",profit  , b_max[i] , b_min[i] , )
                    list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p2"]            
                elif b_max[i] - b_min[i]>aboveT  and  b_min[i] > g_low[i]  and  b_max[i] < g_high[i]  and  r_max>g_high[i]  and  r_min> g_low[i]  :    
                    profit = -zarar * volume *100 # ضرر
                    initial_balance += profit
                    profitP3 += profit
                    p3+=1
                    #print(i,"___________p3____",p3,"  *******  ",profit  , b_max[i] , b_min[i] , )
                    list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p3"]            
                elif b_max[i] - b_min[i]>aboveT  and  b_min[i] > g_low[i]  and  b_max[i] < g_high[i]  and  r_max<g_high[i]  and  r_min< g_low[i]  :    
                    profit = -zarar * volume *100 # ضرر
                    initial_balance += profit
                    profitP4 += profit
                    p4+=1
                    #print(i,"___________p4____",p4,"  *******  ",profit  , b_max[i] , b_min[i] , )
                    list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p4"] 

                elif b_max[i] - b_min[i]>aboveT  and  b_min[i] > g_low[i]  and  b_max[i] > g_high[i]  and    r_min> g_low[i]  :    
                    profit = -zarar * volume *100 # ضرر
                    initial_balance += profit
                    profitP5 += profit
                    p5+=1
                    #print(i,"___________p5____",p5,"  *******  ",profit  , b_max[i] , b_min[i] , )
                    list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p5","buy"] 

                elif b_max[i] - b_min[i]>aboveT  and  b_min[i] > g_low[i]  and  b_max[i] > g_high[i]  and    r_min< g_low[i]  : #buy
                    sbreak=0
                    for j in range(1,33):
                        if   g_high[i+j]>b_max[i] and r_min<g_low[i+j]:
                            profit = (b_max[i] - b_min[i]-broker) * volume *100
                            initial_balance += profit
                            profitP7 += profit
                            p7+=1
                            #print(i,"___________p7____",p7 ,"  *******  ",profit , b_max[i] , b_min[i]  )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p7","buy"]
                            sbreak=1                    
                        elif b_min[i+j]<b_min[i] and b_max[i+j]>b_min[i]:
                            profit = 0
                            p8+=1
                            #print(i,"___________p8____",p8 ,"  *******  ",profit , b_max[i] , b_min[i]  )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p8","buy"]   
                            sbreak=1
                        elif r_min>=g_low[i+j]:
                            profit = -zarar * volume *100 # ضرر
                            initial_balance += profit
                            profitP6 += profit
                            p6+=1
                            #print(i,"___________p6____",p6,"  *******  ",profit  , b_max[i] , b_min[i] , )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p6","buy"]  
                            sbreak=1

                        if sbreak==1:
                            break                    
                    if sbreak==0:
                        if b_min[i+33]<b_min[i] and b_max[i+33]>b_min[i]:
                            profit = 0
                            p8+=1
                            #print(i,"___________p8____",p8 ,"  *******  ",profit , b_max[i] , b_min[i]  )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p8","buy"]
                        else:    
                            profit = (b_max[i+33] - b_max[i]-broker) * volume *100
                            initial_balance += profit
                            profitP8 += profit
                            p8+=1
                            #print(i,"___________p8____",p8 ,"  *******  ",profit , b_max[i] , b_min[i]  )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p8","buy"] 
 
                            
                elif b_max[i] - b_min[i]>aboveT  and  b_min[i] < g_low[i]  and  b_max[i] < g_high[i]  and    r_max< g_high[i]  :  #sell  
                    profit = -zarar * volume *100 # ضرر
                    initial_balance += profit
                    profitP9 += profit
                    p9+=1
                    #print(i,"___________p9____",p9,"  *******  ",profit  , b_max[i] , b_min[i]  )
                    list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p9","sell"]

                elif b_max[i] - b_min[i]>aboveT  and  b_min[i] < g_low[i]  and  b_max[i] < g_high[i]  and    r_max> g_high[i]  : #sell
                    sbreak=0
                    for j in range(1,33):
                        if   g_low[i+j]<b_min[i] and r_max>g_high[i+j]:
                            profit = (b_max[i] - b_min[i]-broker) * volume *100
                            initial_balance += profit
                            profitP11 += profit
                            p11+=1
                            #print(i,"___________p11____",p11 ,"  *******  ",profit , b_max[i] , b_min[i]  )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p11" ,"sell"] 
                            sbreak=1
                            
                            
                        elif b_min[i+j]<b_max[i] and b_max[i+j]>b_max[i]:
                            profit = 0
                            p12+=1
                            #print(i,"___________p12____",p12 ,"  *******  ",profit , b_max[i] , b_min[i]  )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p12" ,"sell"]  
                            sbreak=1
                        elif r_max<=g_high[i+j]:
                            profit = -zarar * volume *100 # ضرر
                            initial_balance += profit
                            profitP10 += profit
                            p10+=1
                            #print(i,"___________p10____",p10,"  *******  ",profit  , b_max[i] , b_min[i] , )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p10","sell"]  
                            sbreak=1

                        if sbreak==1:
                            break
                    if sbreak==0:
                        if b_min[i+33]<b_max[i] and b_max[i+33]>b_max[i]:
                            profit = 0
                            p12+=1
                            #print(i,"___________p12____",p12 ,"  *******  ",profit , b_max[i] , b_min[i]  )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p12" ,"sell"]                        
                        else:
                            profit = (b_max[i] - b_max[i+33]-broker) * volume *100
                            initial_balance += profit
                            profitP12 += profit
                            p12+=1
                            #print(i,"___________p12____",p12 ,"  *******  ",profit , b_max[i] , b_min[i]  )
                            list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p12" ,"sell"]  
                            

                            
                elif b_max[i] - b_min[i]>aboveT  and  b_min[i] < g_low[i]  and  b_max[i] > g_high[i]:
                    p13+=1
                    #print(i,"___________p13____",p13,"  *******  ",profit  , b_max[i] , b_min[i]  )
                    list2=[i,  b_max[i] , b_min[i] ,  profit ,volume , initial_balance ,"p13", "no trade"]
                    
                else:
                    #print("no trade++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    list2=[i,  b_max[i] , b_min[i] ,  "" ,volume , initial_balance ,"p14", "no trade"]
                    p14+=1
                    
                 
                def append_to_csv2(filename, data):
                    with open(filename, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(data)
                        #print("write")
                filename2 = 'riz11_1.csv'

                # اضافه کردن اعداد لیست به فایل CSV
                append_to_csv2(filename2, list2)    

        
    #print(p1,p2,p3,p4,p5,p6,p7,p8 ,p9,p10,p11)
    #print(perINmonth1)
    #print(perINmonth)
    #print(perINmonth2)
    print("*******************************************************************************")
    print("Profit in 19 months", initial_balance - base_balance) 
    tt=(initial_balance-base_balance)/19
    print("average  profit/month :" , tt) 
    print("average monthly profit percentage (after 19 months): " , tt*100/ base_balance)
    print("*******************************************************************************")
    print("balance after 12 months", perINmonth1[11] ) 
    print("Profit in 12 months", perINmonth1[11] - base_balance) 
    tt2=(perINmonth1[11]-base_balance)/12
    print("average  profit/month :" , tt2)
    tt3=(perINmonth1[11])/ base_balance
    print("yearly profit percentage: " , tt3) 
    tt4=tt3/ 12
    print("monthly profit percentage : " , tt4)
    print("*******************************************************************************")
        

    list1=[coefficient[0], percentageData[0] ,percentage[0]  , lenghtCandles[0]    ,base_balance ,perINmonth1[11]  ,tt3,tt4 , minVolume, maxVolume ,coefficientZarar ,profitP1 ,profitP2 ,profitP3 ,profitP4 ,profitP5 ,profitP6,profitP7 ,profitP8 ,profitP9 ,profitP10 ,profitP11,profitP12 ,profitP13 ,profitP14  ," ",p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14 ,aboveT,maxriskP*100]
    print(list1)

    def append_to_csv(filename, data):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
            print("write")
    filename1 = 'result11_1.csv'

    # اضافه کردن اعداد لیست به فایل CSV
    append_to_csv(filename1, list1)

    filename3 = 'result11_2.csv'

    # اضافه کردن اعداد لیست به فایل CSV
    append_to_csv(filename3, list3)