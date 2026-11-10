# PE93

https://projecteuler.net/problem=93
Ran in 40ms in python3.14 (set lim=10 in code)

The approach is simply folds expression nodes
and memoises the folding

the 2 operand nodes are simple
3 operand nodes are based on the folding for 2 nodes
4 operand nodes do 3,1 and 2,2

the bracketing and commutavity is simply encoded
into "mix" generator which yield all 6 possible values
and repeated calls to lower layer (4 nodes calling 3 node)
over all combinations possible

the node 4 folding code, simply dedups all possible
integer values by using a bitset, then count
the running 1's by doubling a python int (the bitset could be ~3000-1000 bits big, shifting it right would be slow)

running code till 50 (96 secs yikes)
found
2, 3, 4, 22 - making 1..52

Read the comments in code for full approach