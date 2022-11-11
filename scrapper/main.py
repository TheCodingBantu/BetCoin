# initialising _list
ini_list = [5, 4, 89, 12, 32, 45]
  
# printing iniial_list
print("intial_list", str(ini_list))
# Calculating difference list
diff_list = []
for index,( x, y )in enumerate (zip(ini_list[0::], ini_list[1::])):
    if(index%2 ==0):
        diff_list.append(y-x)

      
# printing difference list
print ("difference list: ", str(diff_list))