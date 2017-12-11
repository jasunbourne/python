from collections import defaultdict, deque
from itertools import chain

cost_add = 0
cost_remove = 0
cost_change = 0
cost_anagram = 0
start = ""
end = ""

def check_inputs(d):
    global cost_add
    global cost_remove
    global cost_change
    global cost_anagram
    global start
    global end
    lines = []
    inputs = open("input","r")
    for i in inputs:
        lines.append(i.split())
    if len(lines) != 3:
        return -1
    if len(lines[0]) != 4:
        return -1
    for i in range(0, 4):
        try:
            val = int(lines[0][i])
        except ValueError:
            return -1
    if len(lines[1]) != 1 or lines[1][0].lower() not in d:
        return -1
    if len(lines[2]) != 1 or lines[2][0].lower() not in d:
        return -1
    cost_add = int(lines[0][0])
    cost_remove = int(lines[0][1])
    cost_change = int(lines[0][2])
    cost_anagram = int(lines[0][3])
    start = lines[1][0].lower()
    end = lines[2][0].lower()
    return 1


def create_words(word):
    for i in range(len(word)):
        yield word[:i] + word[i + 1:], i

def build_graph(d):
    g = defaultdict(list)
    for word in d:
        for short in create_words(word):
            g[short].append(word)
    return g

def dijkstras(g, d, start, end):
    todo = deque([start])
    seen = {start: None}
    dist = dict()
    prev = dict()
    dist[start] = 0
    while todo:
        word = todo.popleft()
        if word == end: # end is reachable
            break

        #check if anagram
        if len(word) == len(end) and sorted(word) == sorted(end):
            alt = dist[word] + cost_anagram
            if end in dist.keys():
                if alt < dist[end]:
                    dist[end] = alt
                    prev[end] = word
        
            else:
                dist[end] = alt
                prev[end] = word

        same_length = chain(*(g[short] for short in create_words(word)))
        one_longer = chain(*(g[word, i] for i in range(len(word) + 1)))
        one_shorter = (w for w, i in create_words(word) if w in d)
        for nbor in chain(same_length,one_longer,one_shorter):
            if nbor not in seen:
                seen[nbor] = word
                todo.append(nbor)

            if len(word) < len(nbor):
                cost = cost_add
            elif len(word) > len(nbor):
                cost = cost_remove
            else:
                cost = cost_change

            alt = dist[word] + cost
            if nbor in dist.keys():
                if alt < dist[nbor]:
                    dist[nbor] = alt
                    prev[nbor] = word
            else:
                dist[nbor] = alt
                prev[nbor] = word
    else: # no break, i.e. not reachable
        return None # not reachable

    s = list()
    u = end
    keys = prev.keys()
    while u in keys and prev[u] != None:
        s.insert(0,u)
        u = prev[u]
    s.insert(0,u)
    return (s, dist[end])


dictionary = open("words","r")
dictionary = dictionary.read().splitlines()

if check_inputs(dictionary) != -1:
    graph = build_graph(dictionary)
    (words, cost) = dijkstras(graph, dictionary, start, end)

    print "(output: "+str(cost)+") (" + " - ".join([x.upper() for x in words]) +")"
else:
    print "(output: -1)"