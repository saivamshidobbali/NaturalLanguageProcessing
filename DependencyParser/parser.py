from goldparse import *
import sys
import queue

def format_utility(word):
    if word == 'ROOT':
    	return 'ROOT(0)'

    formatted_word = word + "(" + str(data.sentence.index(word)+1) + ")"
    return formatted_word

class Input:

    def __init__(self, sentence, operators):
        self.sentence = sentence
        self.index = 0
        self.dict_index = 0
        self.dictionary = dict()
        self.operators = operators

    def Process_input(self, file_path):
        with open(file_path, 'r') as file: 
            sentences = file.readlines()
        print(sentences[0], end="")

        for i,sentence in enumerate(sentences):
            sentences[i] = sentence.rstrip('\n')
         
        self.sentence = sentences[0].lstrip('SENTENCE:').split()
        self.operators = sentences[2:len(sentences)]

    def build_relations(self):

        print("OPERATORS")
        for operator in self.operators:
        	print(operator, end=" ")
        
        print("\n\nPARSING NOW")
        
        for operator in self.operators:
            operator = operator.split('_')
            if len(operator) == 1:
               self.operator(operator[0], None)
            else:
               self.operator(operator[0], operator[1])   

    def operator(self, op, label):
        if op == 'Shift':
          print("Shifting word", self.sentence[self.index] + "(" + str(data.sentence.index(self.sentence[self.index])+1) + ") onto stack")

          stack.put(self.sentence[self.index])
          self.index += 1

        if op == 'LeftArc':

          parent= stack.get() 
          child = stack.get()


          parent_formatted = format_utility(parent)
          child_formatted = format_utility(child)

          self.dictionary[self.dict_index] = [parent_formatted, label, child_formatted]
          self.dict_index += 1

          print("Applying LeftArc_"+label+" to produce relation: "+ parent_formatted + " -- "+ label+ " --> "+ child_formatted)

          stack.put(parent)
          
        if op == 'RightArc':
          child = stack.get() 
          parent = stack.get()

          parent_formatted = format_utility(parent)
          child_formatted = format_utility(child)

          self.dictionary[self.dict_index] = [parent_formatted, label, child_formatted]
          self.dict_index += 1

          print("Applying RightArc_"+label+" to produce relation: "+ parent_formatted + " -- "+ label+ " --> "+ child_formatted)
          stack.put(parent)

    def formatted_output(self):
          print("\nFINAL DEPENDENCY PARSE")
          for relation_tuple in self.dictionary.values():
              print(relation_tuple[0] + ' -- ' + relation_tuple[1] + ' --> ' + relation_tuple[2])

# Object of Input
data = Input(None, None)

# Stack for processing
stack = queue.LifoQueue(maxsize=0)
stack.put('ROOT')

def main():
    if sys.argv[1] == "-simulate":
       data.Process_input(sys.argv[2])
       data.build_relations()
       data.formatted_output()

    if sys.argv[1] == "-genops":
       goldParse.process_input(sys.argv[3])
       goldParse.gen_operator() 
       goldParse.operator_sequence_print() 

main()