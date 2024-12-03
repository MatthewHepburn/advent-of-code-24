from loader import input_as_ints
import collections

if __name__ == "__main__":
    input = input_as_ints()

    listA = []
    listB = []
    for a, b in input:
        listA.append(a)
        listB.append(b)

    b_count = dict(collections.Counter(listB))

    similarity_scores = [b_count[a] * a for a in listA if a in b_count]
    print(sum(similarity_scores))

