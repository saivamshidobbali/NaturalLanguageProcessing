import sys
from init import init


def read_training_file_gen_list():
    file = open(sys.argv[1],"r")
    contents = file.read()
    words = contents.split()

    position_word_list = ["phi"]

    for particle in words:
       position_word_list.append(particle.lower())
       if particle == "." or particle == "!":
          position_word_list.append("phi")

    return position_word_list 

def read_seed_file():
    file = open(sys.argv[3],"r")
    contents = file.read()
    lines = contents.split("\n")
    return lines

def construct_bigrams_for_a_seed(seed_word,list_of_words):
    list_of_one_seed_bigrams = []
    list_of_one_seed_bigrams.append(seed_word)
    #print("biscuit",list_of_words)
    for i,word in enumerate(list_of_words):
        #print(word)
        if word == seed_word.lower() and (list_of_words[i+1] not in list_of_one_seed_bigrams):
           #print("hey vamshi")	
           list_of_one_seed_bigrams.append(list_of_words[i+1])
    #print("cream",list_of_one_seed_bigrams)       
    return list_of_one_seed_bigrams	


def calculate_probabilities(list_of_one_seed_bigrams):
        #print(list_of_one_seed_bigrams)
        list_of_probabilities = []
        root_word = list_of_one_seed_bigrams[0].lower()
        list_of_words = read_training_file_gen_list()
        DB = init(list_of_words)
        freq = 0
        for i, bigram in enumerate(list_of_one_seed_bigrams):
           print("vamshi",bigram)
           if i == 0:
             continue


           bigram = bigram.lower()
           if bigram not in DB.keys() or root_word not in DB.keys():
              list_of_probabilities.append(0)
              continue

           freq = 0     
           for j, word in enumerate(list_of_words):
              if word == root_word and j != len(list_of_words)-1:
                 if list_of_words[j+1] == bigram:
                   freq += 1
        
           list_of_probabilities.append(freq/DB[root_word])
        print(list_of_probabilities)

def generate_sentences(list_of_one_seed_bigrams):
    root_word = list_of_one_seed_bigrams[0]
    #list_of_probabilities = []
    calculate_probabilities(list_of_one_seed_bigrams)


def construct_bigrams():
    list_of_words = []
    list_of_words = read_training_file_gen_list()

    lines = read_seed_file()
    seed = lines[0]
    #for seed in lines:
    list_of_one_seed_bigrams = construct_bigrams_for_a_seed(seed, list_of_words)
    generate_sentences(list_of_one_seed_bigrams)



construct_bigrams()