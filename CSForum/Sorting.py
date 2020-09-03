
"""
Merge sort here has been altered to sort a list of tuples
based on the second value in the tuple
Sorts into descending order
"""

#Main sorting function
def mergeSort(list, first, last):
    #list stores the list of elements to be sorted
    #first stores the index of the first item in the list
    #last stores the index of the last item in the list

    #Ensures the list consists of more than one element
    if  first < last:
        mid = (first + last) // 2 #Sets the mid index

        #Splits the list into two and makes the recursive call
        list1 = mergeSort(list, first, mid)
        list2 = mergeSort(list, mid + 1, last)
        return merge(list1, list2) #Returns the two lists merged together
    #if the list is only one element it returns the single element
    else:
        list3 = []
        list3.append(list[first])

        return list3


#Merges two lists together
def merge(list1, list2):

    list3 = [] #Variable for the new merged list

    #Loops through until the lists are empty
    while len(list1) > 0 and len(list2) > 0:
        #As this sort is adapted for tuples double indexing has been used here
        if list1[0][1] < list2 [0][1]: #Sorts in descending order
            list3.append(list2[0])
            list2 = list2[1:]
        else:
            list3.append(list1[0])
            list1 = list1[1:]

    #Once one list gets emptied first the remaining elements are added to the end of the main list
    while len(list1) > 0:
        list3.append(list1[0])
        list1 = list1[1:]

    while len(list2) > 0:
        list3.append(list2[0])
        list2 = list2[1:]

    return list3



























