import matplotlib.pyplot as plt 
import mysql.connector
from datetime import datetime
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

reader = mysql.connector.connect(database='DigikalaPhones1', user='admin', password='password', host='localhost')
cursor =reader.cursor()
query='select * from phones_info;'
cursor.execute(query)
phones_info=[]

for (product_name , price , Internal_memory , ram , os , os_version ,picture_resolution , technologt , date) in cursor:
    list1=[product_name , price , Internal_memory , ram , os , os_version ,picture_resolution , technologt , date]
    phones_info.append(list1)
phones_info.sort(key=lambda x:x[0])

def find_position(phones_info, phone ):
    for i in range (0, len(phones_info)):
        if phones_info[i][0]== phone:
            return i
    
    return -1
dates1=[]
external_info1=[]
prices1=[]
dates2=[]
external_info2=[]
prices2=[]

def Diagram( phones_info , phone1, phone2):
    result1 =find_position(phones_info, phone1)
    if result1 ==-1:
        return (print("You Have Entered Wrong Phone Name"))
   
    result2 =find_position(phones_info, phone2)
    if result2 ==-1:
        return (print("You Have Entered Wrong Phone Name"))
    
    l1=[phones_info[result1][2],phones_info[result1][3],phones_info[result1][4],phones_info[result1][6]]
    external_info1.append(l1)
    for i in range(result1, len(phones_info)):
        if phones_info[i][0]==phone1 :
           
            date1=datetime.strptime(phones_info[i][8],'%Y-%m-%d' )
            dates1.append(date1)
            price1=int(str(phones_info[i][1]).replace(',', '', 2))
            prices1.append(price1)
            print(type(price1))
        else:
            break
    

    l2=[phones_info[result2][2],phones_info[result2][3],phones_info[result2][4],phones_info[result2][6]]
    external_info2.append(l2)
    for j in range(result2, len(phones_info)):

        if phones_info[j][0]==phone2 :
           
            date2=datetime.strptime(phones_info[j][8],'%Y-%m-%d' )
            dates2.append(date2)
            price2=int(str(phones_info[j][1]).replace(',', '', 2))
            prices2.append(price2)
            
        else:
            break


     # Let Go For Diagrams ;)
    print(external_info2)
    print(external_info1)
    plt.title('\n Lets See Difference :))))' )
    lab1=('\n %s  :  Internal_Memory_GB : %s     Ram_GB : %s      Os : %s     Picture_Resoloution : %s    \n %s  :  Internal_Memory_GB : %s     Ram_GB : %s      Os : %s     Picture_Resoloution : %s    '%(phone1,external_info1[0][0], external_info1[0][1], external_info1[0][2],  external_info1[0][3], phone2,  external_info2[0][0],  external_info2[0][1], external_info2[0][2], external_info2[0][3]))
    print(lab1)
    plt.plot(dates1,prices1, label = phone1)
    plt.plot(dates2,prices2, label = phone2)
    plt.xlabel(lab1)
    plt.ylabel('\n Prices')
    plt.legend()
    plt.show()

boolean=True
while boolean == True:
    print('\n   Enter Your Phone Model /product name/ :) ')
    target_phone1= input()
    target_phone2=input()
    Diagram(phones_info, target_phone1, target_phone2)
    dates1=[]
    external_info1=[]
    prices1=[]
    dates2=[]
    external_info2=[]
    prices2=[]
    print('\n   Do You Want to Continue : \n    Enter y(Yes) or n(No)')
    result=input().lower()
    if result=='n':
        boolean=False
