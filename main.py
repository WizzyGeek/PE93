# 4 digit set
# 4 operations
# Build all possible expressions evaluate
#
# Canonicaly this is like building trees and folding them


# So now think of how to make all possible trees
# there are four numbers in the expression
# so 4 leaf nodes
# three 3 operation nodes so 3 full nodes
# first put genrics for leaf nodes

# a b + c d + + is one tree, a b c d can change
# ab+c+d* is another -> (a + b + c) * d
# ab+cd*+ -> a + b + c * d is another

# ok let me make new terminology: degree
# a, b are a degree 1 node
# ab+ is degree 2 since sum of lr degree (left = 1 + right= 1)
# ab*, ab/, ab- all are degree 2
# ab+c* the * is root node, and degree = 3 since sum of lr degree (left = 2 + right= 1)
# ab+c*d- => - is root, and degree = 4 since sum of lr degree (left = 3 + right= 1)
# ab+ cd- / => and degree = 4 since sum of lr degree (left = 2 + right= 2)
# Degree of a node is the leafcount in its subtree


# Now take your degree 1
# make unordered pairs
# for + and * reduce the pair and append to a NEW set
# for - and / reduce and add and invert the order (these are commutative) and add that too
# Now all possible degree 2 subtrees are reduced in a new set

# note keep ab, bc, cd, da, bd, ac, bc all in seperate sets

# Take all degree 2 nodeset take degree 1 sets
# make degree 3 nodesets abc, bcd, acd, abd

# Take all degree 2 nodesets,
# ab and cd, ac and bd, ... add ints to degree 4 nodeset

# take all degree 3 nodesets
# do ops with degree 1, abc with d eg
# all ints to degree 4 nodeset

# sort nodeset degree 4 and find max value

# when you combine two numbers, they can only combine to produce 6 new numbers
# (see code for mix(vals, new))

# there are only 7 * 6 = 42 possible node2 (nodeset with degree 2)
# (6 possible vals for lowest in the set since 3 other DIGITS have to be bigger)
# giving 42 * 6 unique vals max bu folding all node 2, cache them
# for node3 8 * 7 * 6 (* 2?) possibles node structures MAX,
# I simply get the 3rd value pair eith 2nd and 1st folded, so I have
# abc and values given by ab, bc, ac
# 3 * 6 values max, now i combine each of 6 with their residue, giving another * 6
# 3 * 6 * 6 = 108 unique vals max
# now node4
# decompose as
# abcd -> ab,cd | ac,bd | ad,bc | abc,d | abd,c | acd,b | bcd,a
# each pair (ab/bc/ac/bd/...) has max 6vals so every order 4 that way will have
# 6 * 6, we have 3 like ab,cd so 3 * 6 * 6
# and 3 ways have 3 * 6 * 6 already, adding one more values can make 6 more unique vals
# so we have a max of 3 * 6 * 6 * 6 vals in 3,1 structure which we have 4 of so
# 3 * 6^3 * 4 + 3 * 6 * 6 = 2700 unique vals for every set MAX
# this number could be easily 25%-50% of that mostly, so I wont add on the
# cost of finding the max run
# 126 * 2700 ops = 340200 ops
# which at 10microsecs per op is 3402000 us =  3400ms = 3.4 secs max
# 10 microsecs is like 100-1000 python instructions depending on which one,
# lets go with 300 instructions on this cpu and algo for my code,
# which should be very generous

# lets compare this with naive
# 4! and 4^3 * 5 = 7680 evals
# a _ b _ c _ d
# (ab)(cd)
# (a(bc))d
# a((bc)d)
# ((ab)c)d
# a(b(cd))

# 4 inital
# 2nd (4C2 + 4P2) * 2 -> (6 + 12) * 2 -> 36
# 3rd, hmmm 2 ops, 3 leaves, 2 bracketing structure, 36 (2nd) * 6 (ops 4 plus two inverse) + 4 (1st)
# 864 (unique expressions possible)
# 4th
# 864 * 6 * 4 + 36C2 * 6 -> very big,
# but the original problem doesn't have enough space :o soooo

# I like my method yo
# I have a hunch its better


# (7380 evals + 7380 checking the max consecutive) * 126 solution space
# 1859760 ops-ish give take few hundred thousand, at 10 microsecond per op, 18 seconds
# So easily under a minute by bruteforce with just simple opts
# uh well meh Road not taken by Robert Frost.

# I am gonna fold trees and use memoized recursion,
# basically dp the tree folding problem, but the
# substruture is a bit complicated to code up,
# so I will hardcode the structure into a specialised transition
# function for each dp update (adding a 3rd or 4th value) :/
from itertools import chain
from functools import cache

# 9 * 8 * 7 * 6 would be the biggest value i explore
# so I set the float epsilon to its reciprocal with some leeway well
# epsilon = (1 / 3024) * 0.5
epsilon = 1e-9

def mix(vals, new):
    for i in vals:
        yield i * new
        yield i + new
        yield i - new
        yield new - i
        yield i / new
        if abs(i) > epsilon: # new trusted non zero, i is not
            yield new / i

def mixunsafe(vals, new):
    for i in vals:
        yield i * new
        yield i + new
        yield i - new
        yield new - i
        if abs(new) > epsilon:
            yield i / new
        if abs(i) > epsilon:
            yield new / i

def mixtwo(vala, valb):
    # if len(vala) < len(valb):
    #     vala, valb = valb, vala

    for i in valb:
        yield from mixunsafe(vala, i)

@cache
def make_a_2(a: int, b: int):
    return sorted(mix([a], b))

@cache
def make_a_3_part(o: tuple[int, int, int]):
    return (mix(make_a_2(o[0], o[1]), o[2]))

@cache
def make_a_3(a: int, b: int, c: int):
    r = chain.from_iterable(make_a_3_part(o) for o in ((a, b, c), (b, c, a), (a, c, b)))
    return set(r)

def make_a_4_part(o):
    return mix(make_a_3(o[0], o[1], o[2]), o[3])

def make_a_4(a, b, c, d):
    bs = 0
    for i in chain.from_iterable(chain(
        (mixtwo(make_a_2(*i), make_a_2(*j)) for i, j in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))),
        (make_a_4_part(o) for o in ((a, b, c, d), (a, b, d, c), (a, c, d, b), (b, c, d, a))),
    )):
        if i.is_integer() and i > 0:
            bs |= 1 << (int(i) - 1) # create bitset

    base = 1
    rl = 0
    while bs & base:
        rl += 1
        base <<= 1
    return rl

s = 0
mc = -1
lim = 50
for a in range(1, lim-3): # the lowest can only be till here
    for b in range(a + 1, lim-2): # 7 is the lowest 2nd last
        for c in range(b + 1, lim-1):
            for d in range(c + 1, lim):
                cnt = make_a_4(a, b, c, d)
                if cnt >= mc:
                    print(a, b, c, d, cnt)
                    mc = cnt

                s += 1
print(s, mc)