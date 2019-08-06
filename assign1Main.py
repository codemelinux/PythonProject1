####### Ugbaja Benedict #########
####### B1202330 ############

import csv
from datetime import datetime


### Funtion to get user data
def getData(fileName):
    
    dataF = open(fileName,"r")
    dataFReader = csv.reader(dataF)
    
    dataList = []
    header = next(dataFReader) ### reads the first line in header
    for row in dataFReader:
        dataList.append(row)
    dataF.close()
    return dataList

### Funtion to get monthly average
def getMonthlyAverage(dataList,monthInt,yearInt):

    Avg = []
    monthlyAvg = 0
       
    for i in dataList:
        date = i[0].split("/") # striping dates from date coln
        month=date[1]
        year=date[2]
        newDate = month + year # contains the month and year formate
        close=float(i[6]) # converting close coln to float
        volume=float(i[5]) # converting Adj Vol coln to float
        
        # Stores user month and year input
        date_year_str = str(monthInt)+str(yearInt)
                
        # compares user date input to our csv date coln and returns monthlyAvg
        if newDate == date_year_str :
            dailySales = (volume * close) / volume
            Avg.append(dailySales)
            ### calculating for monthly avg
            monthlyAvg = sum(Avg) / len(Avg) 
    if monthlyAvg == 0:
        return None

    return "{0:.2f}".format(monthlyAvg)

### Funtion to get yearly average
def getYearlyAverage(dataList, yearInt):


    Avg = []
    yearlyAvgTuple = ()
    
    # looping through the range of month
    for i in range(1,13):
        monthInt = str(i)
        totMonthlyAvg = getMonthlyAverage(dataList,monthInt,yearInt)
        if totMonthlyAvg == None:
            continue
      
        # month Dictionary, converting month number to string
        monthName = month_number_to_string(monthInt)
        # adding month and monthly avg to a tuple
        yearlyAvgTuple += ((monthName,float(totMonthlyAvg)),)
        # creating a list monthlyAvg
        Avg.append(float(totMonthlyAvg))
        # calculating for yearly avg
        TotalMonthlyAverage = sum(Avg)
        TotalNumberMonth = len(Avg)
        yearlyAvgPrice = TotalMonthlyAverage  / TotalNumberMonth 

    yrAvgPrice = "{0:.2f}".format(yearlyAvgPrice)

    return {"yearlyAvg" : yrAvgPrice, "yearAvgTuple" : yearlyAvgTuple}
  
### Funtion to get top months   
def topMonths(dataList, Year_int):

    bestMonth = ()
    worstMonth = ()

    for i in range(1,13):
        monthInt = str(i)
        avgYearTuple = getYearlyAverage(dataList, Year_int)
        yearlyTuple = avgYearTuple.get("yearAvgTuple") # getting tuple from yearlyAvg

        # looping through yearly tuple
        dt = { row[0]: row[1] for row in yearlyTuple}
        mx = max(dt, key=dt.get) # calculating month with best stock price
        mn = min(dt, key=dt.get) # calculating month with worst stock price
    bestMonth += ((mx, dt[mx]),) # best month tuple
    worstMonth += ((mn, dt[mn]),) # worse month tuple
    
       
    return {"bestMonth" : bestMonth, "worstMonth" : worstMonth }


### Funtion to get highest fluctuatution month
def highestFluct(dataList,monthInt,yearInt):
    
    fluc = ()

    for i in dataList:
        date = i[0].split("/") # striping dates from date coln
        month=date[1]
        year=date[2]
        newDate = month + year # contains the month and year formate
        high=float(i[2]) # converting high coln to float
        low=float(i[3]) # converting low Vol coln to float
     
        # Stores user month and year input
        date_year_str = str(monthInt)+str(yearInt)
        # compares user date input to our csv date coln and returns monthlyAvg
        if newDate == date_year_str :

            flucValue = high - low
            fluc += ((flucValue, i[0]),) ### passing data into tuple
            highestDayFluc = max(fluc) # getting highest fluctuation using max
            
    return {"highestFluc" : highestDayFluc ,}
    
def main():
    
    menu()
    
   

def menu():
    # Introduction msgs
    print("\nThis is a data Mining software.")
    print("Welcome to Ben_DMS mining software")

    # Setting an initial value for menu other than the value for 'quit'.
    fileName = ''
    choice = ''

    # Starting a while loop that runs until the user enters the value for 'quit'.
    while choice != 'q' and choice != 'Q' :
        # adding user options in series of print.
        print('')
        print("Choose your option below:")
        print("1 - Input new file ")
        print("2 - Monthly average price")
        print("3 - Yearly average price")
        print("4 - Top worst and best months ")
        print("5 - Highest price fluctuation")
        print("Q/q - Quit")
    
        # Accepting users choice.
        choice = input("\nYour choice? ")
    
        # Respond to the user's choice.
        #.............. Choice 1.................
        if choice == '1':
            fileName = input("\nfileName: ")
            while True:
                try:
                    dataList = getData(fileName)
                    print('\nFile processed...\n')
                    print(dataList[0:6])
    
                    break
     
                except FileNotFoundError:
                    print('\nSorry, file is not available in directory.\n')
                    fileName = input("\nfileName: ")
                    
                            
        #.............. Choice 2.................
        elif choice == '2':
            if fileName is '':
                print("\nNo dataset given. Please select option 1 to input a file.")
                menu
            else:
                print("")
                # getting user input
                yearInt = int(input("Required year: "))
                nMonth = input("Enter month: ")
                monthInt = str(month_string_to_number(nMonth))

                # calling Datalist from getData function
                dataList = getData(fileName) 
                # retrieving monthlyAvg from getMonthlyAvgg function
                monthlyAvg = getMonthlyAverage(dataList,monthInt,yearInt)
                print("Monthly Average Price: "+ monthlyAvg)
                print("")
                
        #.............. Choice 3.................           
        elif choice == '3':
            if fileName is '':
                print("\nNo dataset given. Please select option 1 to input a file.")
                menu
            else:
                print("")
                 # getting user input
                Year_int = int(input("Required year: "))
                dataList = getData(fileName)
                ### retrieving yearlyAvg from getYearlyAverage function
                yearAvgPrice = getYearlyAverage(dataList, Year_int)
                
                # getting the position of yearlyAvg and yearAvgTuple
                yearlyAvg = yearAvgPrice.get("yearlyAvg") 
                yearlyTuple = yearAvgPrice.get("yearAvgTuple")

                print("Average Price for a year: "+ yearlyAvg)
                print("")
                # requesting to display menu
                monthDetails = input("Show monthly details(Y/N)? ")
                if monthDetails == 'y' or monthDetails == 'Y':
                    for i in yearlyTuple:
                        print(i[0],"-" , i[1])
                    print("")
                    
                elif monthDetails == 'n' or monthDetails == 'N':
                    menu
                    print("")
                else:
                    print("wrong input value")
                    print("")
                      
                
        #.............. Choice 4.................
        elif choice == '4':
            if fileName is '':
                print("\nNo dataset given. Please select option 1 to input a file.")
                menu
            else:
                print("")
                # getting user input
                Year_int = int(input("Required year: "))
                dataList = getData(fileName)
                tpMonths = topMonths(dataList, Year_int)
                print("")
                
                print("Analysis for", Year_int)
                ## getting best month from top months function
                bestTpMonth = tpMonths.get("bestMonth")
                worstTpMonth = tpMonths.get("worstMonth")

                # looping through best month to print the position of month and price
                for i in bestTpMonth:
                    print("Best month:",i[0],"with stock price of", i[1])
                
                for i in worstTpMonth:
                    print("Worst month:",i[0],"with stock price of", i[1])
                print("")

     
                
        #.............. Choice 5.................
        elif choice == '5':
            if fileName is '':
                print("\nNo dataset given. Please select option 1 to input a file.")
                menu
            else:
                
                print("")
                # getting users input
                dataList = getData(fileName)
                nMonth = input("Required Month: ")
                yearInt = int(input("Required year: "))
                monthInt = int(month_string_to_number(nMonth))
                ## calling highest fluc functiom   
                highFlu = highestFluct(dataList,monthInt,yearInt)
                fluc = highFlu.get("highestFluc")
                print("")

                ### returning fluctuation value and highest Fluc
                print("Day with highest fluctuation:",str(fluc[1]))
                print("Fluctuation value:",str("{0:.2f}".format(fluc[0])))
                    
                print("")
                
        #.............. Choice Quit.................
        elif choice == 'q' or choice == 'Q':
            print("\nExiting Menu.\n")
        else:
            print("\nInvalid choice! Please select from the list of choices.")
        
    # Print a message that we are all finished.
    print("Thank you for using this program.")
    
    return choice

#### function for month dictionary
def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except :
        raise ValueError('pls enter a string e.g Jan')
            
 #### function for month dictionary
def month_number_to_string(strInt):
    m = {
        1:'January',
        2:'Febuary',
        3:'March',
        4:'April',
        5:'May',
        6:'June',
        7:'July',
        8:'August',
        9:'September',
        10:'October',
        11:'November',
        12:'December',
        }
   # s = strInt.strip()[0:]

    try:
        s = int(strInt)
        out = m[s]
        return out
    except IndexError:
        raise ValueError('no month found')
    except ValueError:
        raise ValueError('no month found')
            
    
# Main Program
if __name__ == "__main__":
    # Launch main 
    main()

    
