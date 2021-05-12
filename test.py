# def create_2d(m,n):
#     v = 0
#     a=[]
#     for i in range(m):
#         a.append([])
#         for j in range(n):
#             a[i].append(v)
#     return a

# asd = create_2d(3,3)
# print(asd) 
# a = [1, 1, 2, 5, 10, 10, 10]
# result = None
# def contain(example_list):
#     return  len(set(example_list)) != len(example_list)


# contain(a)

# print(contain(a) )       


# def summms(a):
#     summ = 0
    
#     b=str(a)
#     b.split()
#     for i in b:
#         print(type(i))
#         summ += int(i)
#     # return summ
#     print (summ)   


# summms(27)






# print (sum(set(a)))


# summ = 0

# b = set(a)
# for i in b:
#     summ += i


# print(summ)
import time
from datetime import date
from functools import wraps

def timer(work):
    
    def wrapper(*args, **kwargs):
        start = time.time()
        work(*args, **kwargs)
        print("--- %s seconds ---" % (time.time() - start))
    return wrapper

@timer
def my_age_in_days(year:int, month:int,day:int):
    birthday = date(year, month, day)
    today = date.today()
    delta = today - birthday
    print(f'today im lived days: {delta.days}')


my_age_in_days(1994, 10, 18) 