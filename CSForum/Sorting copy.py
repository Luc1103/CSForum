import random

basicOps = 0

def main():

    unsortedList = generateNumbers(20)
    print(unsortedList)

    merged = mergeSort(unsortedList, 0, len(unsortedList) - 1)
    print("Merged basic operations: " + str(basicOps))

    bubbled = bubbleSort(unsortedList, 0, len(unsortedList) - 1)
    print("The sorted list is:", bubbled)
    print("The merged list is:", merged)

def generateNumbers(upper):

    numbers = []

    while len(numbers) != upper:
        number = random.randrange(1001)
        if not (number in numbers):
            numbers.append(number)
    return numbers


def bubbleSort(list, first, last):

    elementSwapped = True

    basicOps = 0

    while elementSwapped:
        elementSwapped = False
        for index in range(first, last):
            if list[index] > list[index + 1]:
                elementSwapped = True
                temp = list[index]
                list[index] = list[index + 1]
                list[index + 1] = temp
                basicOps += 1

    print("Bubbled basic operations: " + str(basicOps))

    return list

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





main()
























