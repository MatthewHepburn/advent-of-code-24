from loader import input_as_ints

if __name__ == "__main__":
    input = input_as_ints()

    listA = []
    listB = []
    for a, b in input:
        listA.append(a)
        listB.append(b)

    listA.sort()
    listB.sort()

    differences = [abs(a - b) for a, b in zip(listA, listB)]
    print(sum(differences))

