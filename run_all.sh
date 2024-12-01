#!/bin/zsh

set -e

echo "==== PHP ===="

for dir in [0-9][0-9]*/**/php
do
    ex="$(make --directory "$dir" part_a_example)"
    real="$(make --directory "$dir" part_a)"
    echo "$dir A:"
    echo "    Example = ${ex}, Real = ${real}"
    
    ex="$(make --directory "$dir" part_b_example)"
    real="$(make --directory "$dir" part_b)"
    echo "$dir B:"
    echo "    Example = ${ex}, Real = ${real}"
done

echo "==== Python ===="
for dir in [0-9][0-9]*/**/python
do
    ex="$(make --directory "$dir" part_a_example)"
    real="$(make --directory "$dir" part_a)"
    echo "$dir A:"
    echo "    Example = ${ex}, Real = ${real}"

    ex="$(make --directory "$dir" part_b_example)"
    real="$(make --directory "$dir" part_b)"
    echo "$dir B:"
    echo "    Example = ${ex}, Real = ${real}"
done
