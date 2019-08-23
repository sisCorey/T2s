# coding:utf-8
'''
自动AA算账工具
快速推算出各人如何摊平费用，以求动用最少费用来往完成摊平过程
'''

import os, sys, time

def toF(str):
    f = float(str)
    f = round(f, 4)
    return f

i = 0
total = []
total_cost = 0
while True:
    i = i + 1
    print('输入第%d位参与者开销：' % i)
    r = sys.stdin.readline().strip()
    if r == '':
        print('录入完毕')
        break
    r = r.split(' ')
    cost = toF(r[0])
    if len(r) > 1:
        ID = r[1]
    else:
        ID = i
    if cost <= 0.0:
        cost = 0
    total.append({"ID":ID, "cost":cost, "pay":0.0, "earn":0.0})
    total_cost = toF('%.4f' % (total_cost + cost))
    print('参与者[%s] 已付 ￥%.2f：' % (ID, cost))

print('总共 %d 位参与者' % len(total))
print('总开销 ￥%.2f ' % (total_cost))
print('\n')

aver_cost = toF('%.4f' % (total_cost / len(total)))

i = 0
pay_order=[]
earn_order=[]
max_pay_desc=[]
max_earn_desc=[]
for one in total:
    i = i + 1
    pay = aver_cost - one['cost']
    if pay > 0:
        one['pay'] = pay
        pay_order.append(one)
        print('[%s]应付 %.2f' % (one['ID'], pay))
    if pay < 0:
        one['earn'] = (-1*pay)
        earn_order.append(one)
        print('[%s]应收 %.2f' % (one['ID'], (-1*pay)))

# 计算最优结算关系

# 欠最多优先处理，优先还给与欠款绝对差最小的应收者
# 结算一次后盘点所有人应欠应收，把款额为0的排除
max_pay_desc=sorted(pay_order, reverse=True, key=lambda list:list['pay'])
max_earn_desc=sorted(earn_order, reverse=True, key=lambda list:list['earn'])
print('\n')

try:
    while True:
        topay = None
        bepay = None
        try:
            topay = max_pay_desc[0]
            bepay = max_earn_desc[0]
        except:
            raise Exception('已清')

        # 结算
        r = topay['pay'] - bepay['earn']
        if r < 0:
            print('[%s] 付 [%s] ￥%.2f' % (topay['ID'], bepay['ID'], topay['pay']))
            topay['pay'] = 0.0
            bepay['earn'] = -1 * r
        else:
            print('[%s] 付 [%s] ￥%.2f' % (topay['ID'], bepay['ID'], bepay['earn']))
            topay['pay'] = r
            bepay['earn'] = 0.0
        if topay['pay'] <= 0.0:
            # print('-- [%s]付已清' % topay['ID'])
            max_pay_desc.pop(0)
        if bepay['earn'] <= 0.0:
            # print('-- [%s]收已清' % bepay['ID'])
            max_earn_desc.pop(0)
        # 盘点
        max_pay_desc.sort(reverse=True, key=lambda list:list['pay'])
        max_earn_desc.sort(reverse=True, key=lambda list:list['earn'])

except Exception as e:
    print('%s' % e)
finally:
    print('完毕')
