class Suffix_Node():
    __slots__ = ['_suffix_link', 'transition_links', 'idx', 'depth', 'parent', 'generalized_ids']

    """This Class represents a Node in the Suffix tree and it's method"""

    def __init__(self, idx=-1, parentNode=None, depth=-1):
        # Links
        self._suffix_link = None
        self.transition_links = {}
        # Properties
        self.idx = idx
        self.depth = depth
        self.parent = parentNode
        self.generalized_ids = {}

    def add_suffix_link(self, node):
        self._suffix_link = node

    def get_suffix_link(self):
        if self._suffix_link is not None:
            return self._suffix_link
        else:
            return False

    def get_transition_link(self, suffix):
        return False if suffix not in self.transition_links else self.transition_links[suffix]

    def add_transition_link(self, suffix_node, suffix):
        self.transition_links[suffix] = suffix_node

    def found_transition(self, suffix):
        return suffix in self.transition_links

    def is_leaf(self):
        return len(self.transition_links) == 0

    def traverse(self, t):
        for node in self.transition_links.values():
            node.traverse(t)
        t(self)

    def get_leaves(self):
        # Python <3.6 dicts don't perserve insertion order (and even after, we
        # shouldn't rely on dicts perserving the order) therefore these can be
        # out-of-order, so we return a set of leaves.
        if self.is_leaf():
            return {self}
        else:
            return {x for n in self.transition_links.values() for x in n.get_leaves()}

class Suffix_Tree():
    """Class representing the suffix tree."""

    def __init__(self, input=''):
        self.root = Suffix_Node()
        self.root.depth = 0
        self.root.idx = 0
        self.root.parent = self.root
        self.root.add_suffix_link(self.root)

        if not input == '':
            self.algorithm_build(input)

    def check_input(self, input):
        """Checks the validity of the input.
        """
        if isinstance(input, str):
            return 'st'
        elif isinstance(input, list):
            if all(isinstance(item, str) for item in input):
                return 'gst'

        raise ValueError("String argument should be of type String or a list of strings")

    def algorithm_build(self, graph):
        """This function builds the Suffix tree on the given input. If the input is a List of Strings then a
        Generalized Suffix Tree is built.
        """
        type = self.check_input(graph)

        if type == 'st':
            graph += next(self.Terminal_Symbol_Generator())
            self.suffix_algorithm_build(graph)
        if type == 'gst':
            self.build_generalized(graph)

    def suffix_algorithm_build(self, input):
        """ This function builds a Suffix tree based on the algorithm from "suffix_build"
        :Time complexity: O(n^2)
        :Aux space complexity: O(n^2)
        """
        self.word = input
        self.suffix_build(input)

    def suffix_build(self, input):
        """ this function build a suffix algorithm based in the input given
        :Time complexity: O(n)
        :Aux space complexity: O(n)
        """
        u = self.root
        v = 0
        for i in range(len(input)):
            while u.depth == v and u.found_transition(input[v + i]):
                u = u.get_transition_link(input[v + i])
                v = v + 1
                while v < u.depth and input[u.idx + v] == input[i + v]:
                    v = v + 1
            if v < u.depth:
                u = self.create_node(input,u,v)
            self.create_leaf(input,i,u,v)
            if not u.get_suffix_link():
                self.compute_suffix_link(input,u)
            u = u.get_suffix_link()
            v = v - 1
            if v < 0:
                v = 0

    def create_node(self, graph, u, d):
        i = u.idx
        p = u.parent
        v = Suffix_Node(idx=i,depth=d)
        v.add_transition_link(u,graph[i + d])
        u.parent = v
        p.add_transition_link(v,graph[i + p.depth])
        v.parent = p
        return v

    def create_leaf(self, graph, i, u, d):
        w = Suffix_Node()
        w.idx = i
        w.depth = len(graph) - i
        u.add_transition_link(w,graph[i + d])
        w.parent = u
        return w

    def compute_suffix_link(self, graph, u):
        d = u.depth
        v = u.parent.get_suffix_link()
        while v.depth < d - 1:
            v = v.get_transition_link(graph[u.idx + v.depth + 1])
        if v.depth > d - 1:
            v = self.create_node(graph,v,d - 1)
        u.add_suffix_link(v)

    def build_generalized(self, xs):
        """Builds a Generalized Suffix Tree (GST) from the array of strings provided.
        """
        terminal_gen = self.Terminal_Symbol_Generator()

        _xs = ''.join([x + next(terminal_gen) for x in xs])
        self.word = _xs
        self.GST_word_starts(xs)
        self.suffix_algorithm_build(_xs)
        self.root.traverse(self.label_generalized)

    def label_generalized(self, node):
        """labels the nodes of Generalized Suffix Tree (GST) with indexes of strings found in their previous nodes.
        """
        if node.is_leaf():
            x = {self.get_word_start_index(node.idx)}
        else:
            x = {n for ns in node.transition_links.values() for n in ns.generalized_ids}
        node.generalized_ids = x

    def get_word_start_index(self, ids):
        """returns the index of the string based on node's starting index"""
        i = 0
        for _idx in self.word_starts[1:]:
            if ids < _idx:
                return i
            else:
                i += 1
        return i

    def long_common_substring(self, stringIds=-1):
        """Returns the Largest Common Substring from Strings provided in stringIds.
        If stringIds is not provided, the LCS of all strings is returned.
        """
        if stringIds == -1 or not isinstance(stringIds,list):
            stringIds = set(range(len(self.word_starts)))
        else:
            stringIds = set(stringIds)

        deepest_Node = self.find_long_common_string(self.root,stringIds)
        starting_node = deepest_Node.idx
        ending_node = deepest_Node.idx + deepest_Node.depth
        return self.word[starting_node:ending_node]

    def find_long_common_string(self, node, stringIds):
        """finds the longest common string by traversing the labeled GSD."""
        nodes = [self.find_long_common_string(n,stringIds)
                 for n in node.transition_links.values()
                 if n.generalized_ids.issuperset(stringIds)]

        if nodes == []:
            return node

        deepest_Node = max(nodes,key=lambda n: n.depth)
        return deepest_Node

    def GST_word_starts(self, xs):
        """returns the starting indexes of strings in Generalized Suffix Tree (GST)"""
        self.word_starts = []
        i = 0
        for n in range(len(xs)):
            self.word_starts.append(i)
            i += len(xs[n]) + 1

    def find(self, y):
        """Returns starting position of the substring y in the string used for building the Suffix tree.
        """
        node = self.root
        while True:
            edge = self.edge_Label(node,node.parent)
            if edge.startswith(y):
                return node.idx

            i = 0
            while (i < len(edge) and edge[i] == y[0]):
                y = y[1:]
                i += 1

            if i != 0:
                if i == len(edge) and y != '':
                    pass
                else:
                    return -1

            node = node.get_transition_link(y[0])
            if not node:
                return -1

    def find_all(self, x):
        node = self.root
        while True:
            edge = self.edge_Label(node,node.parent)
            if edge.startswith(x):
                break

            i = 0
            while (i<len(edge) and edge[i] == x[0]):
                x = x[1:]
                i += 1

            if i != 0:
                if i == len(edge) and x != '':
                    pass
                else:
                    return {}

            node = node.get_transition_link(x[0])
            if not node:
                return {}

        leaves = node.get_leaves()
        return {n.idx for n in leaves}

    def edge_Label(self, node, parent):
        """returns the edge labels between a node, and it's parent"""
        return self.word[node.idx + parent.depth: node.idx + node.depth]

    def Terminal_Symbol_Generator(self):
        """This functions generates terminal symbols which are necessary for building Generalized Suffix Tree (GST).
        The Unicode Private uses Area U+E000 to U+F8FF is to make sure that terminal symbols are not part of the input string.
        """
        terminal_symbols = list(list(range(0xE000,0xF8FF + 1)) +
                                list(range(0xF0000, 0xFFFFD+1)) + list(range(0x100000, 0x10FFFD+1)))
        for i in terminal_symbols:
            yield (chr(i))

        raise ValueError("To many input strings.")

def compare_subs(submission1, submission2):
    """ This final function here calls the "Suffix_Tree" class and then takes in the inputs of the submission  is list form
        and call my "long_common_string" method from the "Suffix_Tree" class which computes the longest common string. Afterwards
        it calculates the similar percentage taking the length of "lcs" stored in this variable and divides it by the length of
        each submission, thus multiplying it with 100. and therefore returns the longest common string, similarity rate of submission 1
        and similarity rate of submission 2 in list.
        :Time complexity: O(n+m)
        :Aux space complexity: O(n+m)
    """
    lst = [submission1,submission2]
    st = Suffix_Tree(lst)
    lcs = st.long_common_substring()
    similar_percentage_1 = round((len(lcs)/len(submission1))*100)
    similar_percentage_2 = round((len(lcs)/len(submission2))*100)
    output = [lcs, similar_percentage_1, similar_percentage_2]
    return(output)

# Test cases:
submission1 = 'the quick brown fox jumped over the lazy dog'
submission2 = 'my lazy dog has eaten my homework'
print(compare_subs(submission1, submission2))

submission1 = 'radix sort and counting sort are both non-comparison sorting algorithms'
submission2 = 'counting sort and radix sort are both non-comparison sorting algorithms'
print(compare_subs(submission1, submission2))

submission1 = ' '
submission2 = '  '
print(compare_subs(submission1, submission2))