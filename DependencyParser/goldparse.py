import sys
import queue


operator_sequence = []

# Stack for processing
gen_stack = queue.LifoQueue(maxsize=0)
gen_stack.put('ROOT')

class List:
    def __init__(self):
        self.child_list = []

    def add(self, child):
        self.child_list.append(child)

    def show(self):
        print(self.child_list)

    def find(self, Index):
        for x in self.child_list:
           if (x == str(Index)):
              return 1
        return 0

    def remove_elem_from_label_list(self, childIndex):
        for elem in self.child_list:
            for key in  elem.keys():
               if  key == str(childIndex):
                 self.child_list.remove(elem)
        return elem.values();          

    def remove_elem(self, childIndex):
    	self.child_list.remove(str(childIndex))

    def length(self):
        return len(self.child_list)                 

class gold_parse:

    def __init__(self):
        self.Idmap = dict()
        self.Headmap_with_label = []
        self.Headmap = []
        self.index = 0


    def do_rightarc(self):

        child = gen_stack.get()
        parent = gen_stack.get()
        
        childIndex = list(self.Idmap.values()).index(child)
        parentIndex = list(self.Idmap.values()).index(parent)

        label = self.Headmap_with_label[parentIndex].remove_elem_from_label_list(childIndex)
        self.Headmap[parentIndex].remove_elem(childIndex)

        if parent != 'ROOT':
           gen_stack.put(parent)
        print("Generating RightArc"+"_"+list(label)[0]+" to produce relation: "+ parent +"("+str(parentIndex)+")" " -- " + list(label)[0] + " --> " + child+"("+str(childIndex)+")")
        operator_sequence.append("RightArc_"+list(label)[0])

    def do_leftarc(self):

        parent = gen_stack.get()
        child = gen_stack.get()
        
        childIndex = list(self.Idmap.values()).index(child)
        parentIndex = list(self.Idmap.values()).index(parent)

        label = self.Headmap_with_label[parentIndex].remove_elem_from_label_list(childIndex)
        self.Headmap[parentIndex].remove_elem(childIndex)
       
        if parent != 'ROOT':
           gen_stack.put(parent)
        print("Generating LeftArc"+"_"+list(label)[0]+" to produce relation: "+ parent +"("+str(parentIndex)+")" " -- " + list(label)[0] + " --> " + child+"("+str(childIndex)+")")    
        operator_sequence.append("LeftArc_"+list(label)[0])
     

    def can_rightarc(self):
        child = gen_stack.get()
        parent = gen_stack.get()
      
        gen_stack.put(parent)
        gen_stack.put(child)

        childIndex = list(self.Idmap.values()).index(child)
        parentIndex = list(self.Idmap.values()).index(parent)

        ret_dep = self.Headmap[parentIndex].find(childIndex)
        ret_len = self.Headmap[childIndex].length()

        if ret_dep == 1 and ret_len == 0:
            return 1
        else:
            return 0

    def can_leftarc(self):

        parent = gen_stack.get()
        child = gen_stack.get()
        
        gen_stack.put(child)
        gen_stack.put(parent)

        childIndex = list(self.Idmap.values()).index(child)
        parentIndex = list(self.Idmap.values()).index(parent)

        ret_dep = self.Headmap[int(parentIndex)].find(childIndex)

        if ret_dep == 1:
            return 1
        else:
            return 0

    def build_relation_tree(self, sentences):
        for i in range(len(self.Idmap)):
              self.Headmap.append(List())
              self.Headmap_with_label.append(List())

        for sentence in sentences:
            self.Headmap[int(sentence[2])].add(sentence[0])
            x = {sentence[0]: sentence[3]}
            self.Headmap_with_label[int(sentence[2])].add(x)

        first_sentence = "SENTENCE:"
        for x in self.Idmap.values():
            if x == 'ROOT':
                continue
            first_sentence = first_sentence +" "+ x
            #print(self.Idmap[sentence[2]]+"("+ sentence[2] +")"+" -- "+sentence[3]+" --> "+sentence[1]+"("+sentence[0]+")")
        
        print(first_sentence, end="")
        print("\nGOLD DEPENDENCIES")
        for sentence in sentences:
            print(self.Idmap[sentence[2]]+"("+ sentence[2] +")"+" -- "+sentence[3]+" --> "+sentence[1]+"("+sentence[0]+")")


    def process_input(self, file_path):
        with open(file_path, 'r') as file: 
            sentences = file.readlines()

        for i,sentence in enumerate(sentences):
            sentences[i] = sentence.rstrip('\n').split()       

        self.Idmap[str(0)] = "ROOT"
        for sentence in sentences:
            self.Idmap[sentence[0]] = sentence[1]

        self.build_relation_tree(sentences)

    def operator_sequence_print(self):
        print("\nFINAL OPERATOR SEQUENCE")
        for elem in operator_sequence:
            print(elem)

    def gen_operator(self):
        print("\nGENERATING PARSING OPERATORS")

        gen_stack.put(self.Idmap[str(0)])
        self.index = self.index + 1

        print('Shift')
        operator_sequence.append("Shift")

        gen_stack.put(self.Idmap[str(1)])
        self.index = self.index + 1

        while not gen_stack.empty():
            word = gen_stack.get()
            if word == 'ROOT':
                break
            gen_stack.put(word)

            if self.can_leftarc():
                self.do_leftarc()  

            elif self.can_rightarc():
                self.do_rightarc()
 
            else:
                print('Shift')
                operator_sequence.append("Shift")
                gen_stack.put(self.Idmap[str(self.index)])
                self.index += 1                            

goldParse = gold_parse()