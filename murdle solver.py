# EDIT: Here's a solver for similar logic puzzles which has a nice UI: http://www.jsingler.de/apps/logikloeser/
# My code below isn't super great and was made more just for the fun of making it.


#%%
from collections import defaultdict


class Murdle():
    '''
    Keeps track of the grid in a Murdle-style logic puzzle.
    There are some number of categories. Each category has N unique types.
    There are N entities in the puzzle. Each entity has exactly one unique type from each category.

    input categories: a dictionary mapping category names to a list of types in that category.
        eg: {"color": ["red","green","indigo"], "name": ["Lucy","Albert","Blibblestein"], "haţ": ["top","fedora","bald"]}
        In this implementation, the types must all have unique names, or things will break.

    The match_map contains a value in {True,False,None}, indicating what we know about that pair of types.
        True if we know they belong to the same entity. False if we know they don't. None otherwise.
        Use with match_map[a][b]

    The type_to_category map associates each type name with its category.

    mark(a,b): Records that types a and b belong to the same entity. Recursively evaluates implications of that.
    ruleOut(a,b): Records that types a and b do NOT belong to the same entity. Recursively evaluates implications.
    get_siblings(a): returns all the other types which share the category with a
    display(): prints out an ascii version of the match table.

    Some of these functions depend on python storing the order of elements in dictionaries. (py 3.7+)
    The algorithmic efficiency on parts of this are terrible, but I won't be using it with any big inputs, so :shrug:
    '''

    def __init__(self,categories):
        self.categories = categories
        self.type_set = set()
        self.type_to_category = dict()
        self.match_map = defaultdict(dict)
        self.possibility_map = defaultdict(dict)

        for category,type_list in categories.items():
            for type in type_list:
                self.type_set.add(type)
                self.type_to_category[type] = category

        for a in self.type_set:
            for b in self.type_set:
                self.match_map[a][b] = None

        # Impose reflexivity of matches
        for a in self.type_set:
            self.mark(a,a)

    def get_siblings(self,a):
        cat = self.type_to_category[a]
        return [type for type in self.categories[cat] if type != a]

    def mark(self,a,b):
        if self.match_map[a][b] == False: print("CONTRADICTION",a,b); return 0
        if self.match_map[a][b] == True: return 0 # Already marked. Don't do anything.
        # If we get past the above checks, then match_map[a][b] == None. Ie, we haven't marked the grid.
        
        self.match_map[a][b] = True

        # Rule out the sibling matches.
        for alt_b in self.get_siblings(b): self.ruleOut(a,alt_b)
        for alt_a in self.get_siblings(a): self.ruleOut(alt_a,b)

        # Impose transitivity of matches.
        for c in self.type_set:
            if c==a or c==b: continue
            elif self.match_map[a][c] == True: self.mark(b,c)
            elif self.match_map[b][c] == True: self.mark(a,c)

        # Impose symmetry of matches
        self.mark(b,a)

    def ruleOut(self,a,b):
        if self.match_map[a][b] == True: print("CONTRADICTION",a,b); return 0
        if self.match_map[a][b] == False: return 0 # Already marked. Don't do anything.
        # If we get past the above checks, then the box for (a,b) is blank. ie match_map[a][b] == None
        
        self.match_map[a][b] = False

        # Implications of transitivity of matches. (if a=b, and a!=c, then b!=c)
        for c in self.type_set:
            if c==a or c==b: continue
            elif self.match_map[a][c] == True: self.ruleOut(b,c)
            elif self.match_map[b][c] == True: self.ruleOut(a,c)

        #Test whether this results in  match by exhaustion of possibilities.
        self.markIfExhausted(a, self.type_to_category[b])
        self.markIfExhausted(b, self.type_to_category[a])

        # Impose symmetry of anti-matches
        self.ruleOut(b,a)

    def markIfExhausted(self,a,category):
        possible_matches = [b for b in self.categories[category] if self.match_map[a][b] != False]
        if len(possible_matches) == 1:
            self.mark(a,possible_matches[0])

    def display(self):
        "On columns, names are displayed as only first letter. On rows, they are truncated."
        NAME_WIDTH_MAX = 15
        row_length = len(self.type_set) + NAME_WIDTH_MAX + len(self.categories)

        DISPLAY_CHARS = {True: 'O', False: "▒", None:' '}
        #DISPLAY_CHARS = {True: '█', False: " ", None:'?'} #█░▒▓
        def displayChar(a,b): 
            return DISPLAY_CHARS[self.match_map[a][b]]
        def displayRowValues(a):
            return '|'.join([''.join([displayChar(a,b) for b in types]) for types in self.categories.values()])
        def displayRowType(a): 
            return a.ljust(NAME_WIDTH_MAX)[:NAME_WIDTH_MAX] + "|"
        def displayAbbr(a):
            words = a.split(' ')
            if len(words) > 1: return words[0][0]+words[1][0]
            else: return a[0].rjust(2)

        header1 =  '|'.join([''.join([displayAbbr(b)[0] for b in types]) for types in self.categories.values()])
        header2 =  '|'.join([''.join([displayAbbr(b)[1] for b in types]) for types in self.categories.values()])
        print(' '*(NAME_WIDTH_MAX+1) + header1)
        print(' '*(NAME_WIDTH_MAX+1) + header2)

        for cat,types in self.categories.items():
            print('-'*row_length)
            for a in types:
                print(displayRowType(a) + displayRowValues(a))

    def get_matches(self,a):
        return [k for k,v in self.match_map[a].items() if v==True]


#%%

dishonored2_puzzle = {
    "name": ["Lady Winslow", "Doctor Marcolla", "Countess Contee", "Madam Natsiou", "Baroness Finch"],
    "seat": ["far left", "mid left", "middle", "mid right", "far right"],
    "treasure": ["diamond", "snuff tin", "bird pendant", "ring", "war medal"],
    "drink": ["wine", "rum", "beer", "whisky", "absinthe"],
    "home": ["Fraeport", "Baleton", "Dunwall", "Dabokva", "Karnaca"],
    "color": ["red", "green", "white", "purple", "blue"],
}

puzzle = Murdle(dishonored2_puzzle)

puzzle.mark("Lady Winslow","red")
puzzle.mark("Doctor Marcolla","far left")
puzzle.mark("green","mid left")

# white sat left of purple
puzzle.ruleOut("white","far left") #bc then they would be left of green
puzzle.ruleOut("white","far right")
puzzle.ruleOut("purple","far left")
puzzle.ruleOut("purple","middle") #bc then would be right of green

puzzle.mark("white","wine")
puzzle.mark("Fraeport","blue")

# Fraeport next to ring
# From other clues, we know Fraeport is far left
puzzle.mark("ring","mid left")

puzzle.ruleOut("Fraeport","ring")
puzzle.mark("Madam Natsiou","diamond")
# "lady from baleton", but also "lady from Dabokva", so ignore that. Not refering to Winslow
puzzle.mark("Baleton","snuff tin")

# bird next to Dunwall
# dunwall next to rum
puzzle.ruleOut("Dunwall","bird pendant")
puzzle.ruleOut("Dunwall","rum")
# From other clues we learn that Dunwall is mid left.
# Thus the bird and rum must be either far left or middle
puzzle.ruleOut("far right","rum")
puzzle.ruleOut("mid right","rum")
puzzle.ruleOut("far right","bird pendant")
puzzle.ruleOut("mid right","bird pendant")

puzzle.mark("Countess Contee","beer")
puzzle.mark("Dabokva","whisky")
puzzle.mark("middle","absinthe")
puzzle.mark("Baroness Finch","Karnaca")

puzzle.display()

for name in puzzle.categories["name"]:
    print(puzzle.get_matches(name))


#%%
murdle20230805 = {
    "suspects": ["ms","gc","cr","ba"],
    "weapons": ["coal","knife","luggage","wine"],
    "locations": ["roof","deck","caboose","car"],
    "motives": ["fortune","blackmail","feel","spy"],
}

puzzle = Murdle(murdle20230805)

puzzle.mark("feel","ba")
puzzle.mark("gc","fortune")
puzzle.ruleOut("wine","blackmail")
puzzle.mark("spy","deck")
puzzle.ruleOut("cr","coal")
puzzle.ruleOut("ms","coal")
puzzle.mark("ba","car")

puzzle.mark("ms","deck")
#puzzle.mark("knife","car")
puzzle.mark("wine","caboose")
puzzle.mark("luggage","deck")

puzzle.display()

