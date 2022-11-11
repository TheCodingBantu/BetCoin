import random

# initialising _list

my_list=[]
for i in range(20):
    if(random.randint(1,2)==1):
        my_list.append('l')
    else:
        my_list.append('w')


count=0
length=[]
dates=[]
if len(my_list)>1:
    for i in range(1,len(my_list)):
        if(my_list[i]=='w'):
            if my_list[i-1]==my_list[i]:
                count+=1
        length.append(count)
        count=0

print(my_list)
print(length)

wins=0
for i in range(len(length)):
    if(length[i]==1):
        print(i+1)
        wins+=length[i]

# print(wins)