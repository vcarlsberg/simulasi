from random import random, randrange
import numpy as np
import pandas as pd

def demand(number):
    if (number<=0.05):
        return 2
    elif (number<=0.20):
        return 3
    elif (number<=0.40):
        return 4
    elif (number<=0.70):
        return 5
    elif (number<=0.90):
        return 6
    elif (number<=1.00):
        return 7

def leadtime(number):
    if (number<=0.25):
        return 3
    elif (number<=0.75):
        return 4
    elif (number<=1.0):
        return 5

def simulasi(init_stock,period_cummulative,s_kecil,s_besar,shortage_cost_per_unit,inventory_cost_per_unit,lot_order_cost,price_per_unit,purchasing_cost_per_unit) :
    on_lead_time=False

    stock_EOD=[0] * (period_cummulative+10)
    shortage_cost_EOD=[0] * (period_cummulative+10)
    inventory_cost_EOD=[0] * (period_cummulative+10)
    lot_order_cost_EOD=[0] * (period_cummulative+10)
    purchasing_cost_EOD=[0] * (period_cummulative+10)
    cummulative_cost_EOD=[0] * (period_cummulative+10)
    revenue_EOD=[0] * (period_cummulative+10)
    profit_EOD=[0] * (period_cummulative+10)
    demand_EOD = [0] * (period_cummulative + 10)
    lead_time_EOD=[0] * (period_cummulative + 10)
    replenished_EOD = [0] * (period_cummulative + 10)
    random_no_demand=[0] * (period_cummulative + 10)
    random_no_lead= [0] * (period_cummulative + 10)

    for x in range(period_cummulative+1):
        if (x == 0):
            stock_EOD[0]=init_stock
            inventory_cost_EOD[0]=stock_EOD[0]*1

        if (x>0):
            demand_random=random()
            random_no_demand[x]=demand_random
            demand_EOD[x]=demand(demand_random)
            stock_EOD[x]=stock_EOD[x-1]-demand_EOD[x]+stock_EOD[x]
            if(stock_EOD[x]<=0):
                shortage_cost_EOD[x]=stock_EOD[x]*-2

            #count revenue
            if(stock_EOD[x-1]>demand_EOD[x] and stock_EOD[x-1]>0):
                revenue_EOD[x]=(demand_EOD[x])*price_per_unit
            elif(stock_EOD[x-1]<=demand_EOD[x] and stock_EOD[x-1]>0):
                revenue_EOD[x]=stock_EOD[x-1]*price_per_unit
            else:
                revenue_EOD[x]=0

            if (stock_EOD[x+1]==0 and on_lead_time==False):
                if (stock_EOD[x]<s_kecil and stock_EOD[x]>=0):
                    leadtime_random=random()
                    random_no_lead[x]=leadtime_random
                    waktu_leadtime=leadtime(leadtime_random)
                    lead_time_EOD[x]=waktu_leadtime
                    stock_EOD[x+waktu_leadtime]=(s_kecil-stock_EOD[x])+(s_besar-s_kecil)
                    purchasing_cost_EOD[x]=purchasing_cost_per_unit*(s_kecil-stock_EOD[x])+(s_besar-s_kecil)
                    replenished_EOD[x+waktu_leadtime]=stock_EOD[x+waktu_leadtime]
                    lot_order_cost_EOD[x] = lot_order_cost
                    on_lead_time=True
                if (stock_EOD[x] < 0):
                    leadtime_random = random()
                    random_no_lead[x] = leadtime_random
                    waktu_leadtime = leadtime(leadtime_random)
                    lead_time_EOD[x] = waktu_leadtime
                    stock_EOD[x+waktu_leadtime]=((stock_EOD[x]*-1)+s_kecil)+(s_besar-s_kecil)
                    purchasing_cost_EOD[x] = purchasing_cost_per_unit * (s_kecil - stock_EOD[x]) + (s_besar - s_kecil)
                    replenished_EOD[x + waktu_leadtime] = stock_EOD[x + waktu_leadtime]
                    lot_order_cost_EOD[x] = lot_order_cost
                    on_lead_time = True

            if(stock_EOD[x+1]>0):
                on_lead_time=False

            if(stock_EOD[x]>0):
                inventory_cost_EOD[x]=inventory_cost_per_unit*stock_EOD[x]

        profit_EOD[x]=revenue_EOD[x]-shortage_cost_EOD[x]-inventory_cost_EOD[x]-lot_order_cost_EOD[x]-purchasing_cost_EOD[x]

    df = pd.DataFrame({'Demand': demand_EOD[0:31],
                       'Demand Rand No':random_no_demand[0:31],
                       'Lead Time':lead_time_EOD[0:31],
                       'Leadtime Rand No': random_no_lead[0:31],
                       'Stock': stock_EOD[0:31],
                       'Replenished':replenished_EOD[0:31],
                       'Revenue':revenue_EOD[0:31],
                       'Shortage Cost':shortage_cost_EOD[0:31],
                       'Inventory Cost':inventory_cost_EOD[0:31],
                       'Lot Order Cost':lot_order_cost_EOD[0:31],
                       'Purchasing Cost':purchasing_cost_EOD[0:31],
                       'Profit':profit_EOD[0:31]
                       })

    return df

#CONFIGURABLE PARAMETERS#
init_stock = 50
period_cummulative = 30
s_kecil=750
s_besar=1000
shortage_cost_per_unit=2
inventory_cost_per_unit=1
lot_order_cost=15
price_per_unit=15
purchasing_cost_per_unit=5
iteration = 5
s_kecil_range_min=10
s_kecil_range_max=200
s_besar_range_min=10
s_besar_range_max=200
#END OF CONFIGURABLE PARAMETERS#

s_kecil_range=range(s_kecil_range_min,s_kecil_range_max+1,10)
s_besar_range=range(s_besar_range_min,s_besar_range_max+1,10)

#xx=0

df2 = pd.DataFrame(columns=['s_kecil', 's_besar', 'profit_avg'])
profit_mean=0

for d in s_kecil_range:
    for e in s_besar_range:
        for x in range(1,iteration+1):
            profit = simulasi(init_stock, period_cummulative, d, e, shortage_cost_per_unit, inventory_cost_per_unit,
                              lot_order_cost, price_per_unit, purchasing_cost_per_unit)
        #    profit.to_excel(writer, sheet_name='Sheet'+str(x))
            profit_mean=profit_mean+profit["Profit"].mean()

        #writer.save()

        df2=df2.append({'s_kecil':d,'s_besar':e,'profit_avg':profit_mean},ignore_index=True)
        print("s_kecil = "+str(d)+" s_besar = "+str(e)+" profit= "+str(profit_mean / iteration))


posisi_profit_terbesar=df2['profit_avg'].idxmax()
param_terbesar=df2.iloc[posisi_profit_terbesar,:]

writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')

for x in range(iteration):
    x=x+1
    profit = simulasi(init_stock, period_cummulative, param_terbesar["s_kecil"], param_terbesar["s_besar"],
                      shortage_cost_per_unit, inventory_cost_per_unit,
                      lot_order_cost, price_per_unit,purchasing_cost_per_unit)
    profit.to_excel(writer, sheet_name='Sheet'+str(x))
writer.save()



print(param_terbesar)
print("End of Process")
