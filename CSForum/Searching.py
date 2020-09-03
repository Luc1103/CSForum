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
