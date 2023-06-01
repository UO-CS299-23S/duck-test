"""Example using test harness on sample_subject"""

import sample_subject
from sample_subject import Branch, Leaf, Empty
import test_harness
from test_harness import test_case
test_harness.init()

def callee():
    return

@test_case("debugging")
def caller():
    callee()

@test_case
def test_empty():
    assert Empty().count() == 0

@test_case
def test_bare():
    bare_tree = Branch(Empty(), Leaf("foo"))
    assert bare_tree.count() == 1, "((),foo) -> 1"

    bare_tree = Branch(Leaf("bar"), Empty())
    assert bare_tree.count() == 1, "(foo, ()) -> 1"

@test_case([Branch, Leaf])
def test_small():
    min_tree = Branch(Leaf("foo"), Leaf("bar"))
    assert min_tree.count() == 2

@test_case([Branch, Empty, Leaf])
def test_deeper():
    min_tree = Branch(Branch(Leaf("a"), Empty()),
                      Branch(Leaf("b"), Leaf("c")))
    assert min_tree.count() == 3, "Should have three non-empty leaves"

test_harness.main()
print(f"Thoroughness: Found test cases for {test_harness.coverage()}")
print(f"Missing: {test_harness.uncovered(sample_subject)}")
