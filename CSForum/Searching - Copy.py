import random
basicOps = 0
def main():
    global basicOps
    unsortedList = generateNumbers(101)

    print("The unsorted list is:", unsortedList)

    number = getNatural("Please enter the number you want to search for: ")

    index = linearSearch(unsortedList, number)

    if index == -1:
        print("The item has not been found")
    else:
        print("The item has been found at index:", index)

    print("The basic operations for linear search is:", basicOps)

    sortedList = mergeSort(unsortedList, 0, len(unsortedList) - 1)
    print(sortedList)

    #Resets the basicOps variable
    basicOps = 0

    index2 = binarySearch(sortedList, number, 0, len(unsortedList) - 1)
    print(index2)
    if index2 == -1:
        print("Item not found")
    else:
        print("Item was found at:", index2)

    print("The basic operations for binary search is:", basicOps)



def linearSearch(list, searchFor):
    global basicOps
    found = False
    basicOps = 0
    index = 0
    while not found and index < len(list):
        basicOps += 1
        if list[index] == searchFor:
            found = True
        else:
            index += 1

    if index == len(list):
        index = -1

    print("Basic ops are:", basicOps)
    return index

def generateNumbers(upper):

    numbers = []

    while len(numbers) != upper:
        number = random.randrange(upper)
        if not (number in numbers):
            numbers.append(number)
    return numbers

def binarySearch(list, searchFor, first, last):

    global basicOps

    if first > last:
        return -1
    else:
        mid = (first + last) // 2
        basicOps += 1

        if searchFor == list[mid]:
            return mid
        else:
            if searchFor > list[mid]:
                first = mid + 1

            else:
                last = mid - 1

            return binarySearch(list, searchFor, first, last)

def mergeSort(list, first, last):

    if  first < last:
        mid = (first + last) // 2

        list1 = mergeSort(list, first, mid)
        list2 = mergeSort(list, mid + 1, last)
        return merge(list1, list2)
    else:
        list3 = []
        list3.append(list[first])

        return list3


def merge(list1, list2):
    global basicOps

    list3 = []

    while len(list1) > 0 and len(list2) > 0:
        if list1[0] > list2 [0]:
            list3.append(list2[0])
            list2 = list2[1:]
            basicOps += 1
        else:
            list3.append(list1[0])
            list1 = list1[1:]
            basicOps += 1

    while len(list1) > 0:
        list3.append(list1[0])
        list1 = list1[1:]
        basicOps += 1

    while len(list2) > 0:
        list3.append(list2[0])
        list2 = list2[1:]
        basicOps += 1

    return list3

def getNatural(message):
    #SUBROUTINE RETURNS intger
    #LOCAL VARIABLES
    # valid    boolean to indicate the state of input
    # number   string to hold the inputted number

    #initialise switch for validity
    valid = False
    while not valid:
        #getnumber
        number = input(message)
        #determine if the number is an integer
        if not number.isdigit():
            print("Invalid number, try again")
        else:
            valid = True
        #ENDIF

    #ENDWHILE

    return int(number)
#END

main()

































