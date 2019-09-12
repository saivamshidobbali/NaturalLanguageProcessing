import sys
from init import init


file = open(sys.argv[1],"r")
contents = file.read()
data = contents.split()

def read_test_file():
    test_file = open(sys.argv[3], "r")
    test_contents = test_file.read()
    # test_data = test_contents.split()
    test_data = test_contents.split('\n')

    list_of_words = []
    for sentence in test_data:
    
        list_of_words.append("phi")
        S = sentence.split()
        
        for word in S:
            list_of_words.append(word)
    list_of_words.append("phi")
    return list_of_words

 
def bigram_position_list(data):

    position_word_list = ["phi"]

    for particle in data:
       position_word_list.append(particle.lower())
       if particle == "." or particle == "!":
          position_word_list.append("phi")

    return position_word_list   

# Bigram model
def bigram():
    pos_to_word = bigram_position_list(data) 
    DB = init(pos_to_word)
    test_data = read_test_file()
    Probability_of_S = 1

    for i, test_word in enumerate(test_data):

        print("hell ya", test_word)
        if test_word.lower() == "phi":
           print("Probability =====", Probability_of_S)
           Probability_of_S = 1
           continue

        test_word = test_word.lower()
        context = test_data[i-1].lower() 
        
        if(test_word not in DB.keys() or context not in DB.keys()):
             Probability_of_S = 0
             continue

        freq = 0     
        for j, word in enumerate(pos_to_word):
          if word == context and j != len(pos_to_word)-1:
            if pos_to_word[j+1] == test_word:
               freq += 1
        
        Probability_of_S = Probability_of_S * freq/DB[context]


bigram()