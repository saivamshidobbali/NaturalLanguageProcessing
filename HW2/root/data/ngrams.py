import sys
import random
import math

def read_file(filename):
    data = open(filename,"r").read().split("\n")
    list_of_words = []
     
    for sentence in data:
         sentence = "phi " + sentence
         temp_list = sentence.split()

         for word in temp_list:
            list_of_words.append(word)


    return list_of_words

def unigram_modelling_db(list_of_words):
    DB = {}
    for x in list_of_words:
        x= x.lower()
        if x in DB:
          DB[x] = DB[x]+1
        else:
          DB[x] = 1
    return DB 


def roundoff(number):
    if number == "undefined":
      return number
    number = number * 10000
    number = math.ceil(number)
    number = number/10000
    return number


def bigram_modelling_db(list_of_words):
    bigram_dict = {"phi" : {"the" : 0}}

    for i, word in enumerate(list_of_words):
        if word == "phi":
           continue
     
        context = list_of_words[i-1]
        context = context.lower()
        word= word.lower()
        
        if context in bigram_dict.keys() :
            if word in bigram_dict[context].keys():
                bigram_dict[context][word] +=1
            if word not in bigram_dict[context].keys():
                bigram_dict[context].update({word : 1})    
            
        else:
            bigram_dict.update({context : {word : 1}})
    return bigram_dict        



def populate_bigram_probabilities():
    list_of_words = read_file(sys.argv[1])
    bigram_dict = bigram_modelling_db(list_of_words)
    unigram_dict = unigram_modelling_db(list_of_words)
    bigram_dict_prob = bigram_dict

    for context in bigram_dict:
        for word in bigram_dict[context]:
            bigram_dict_prob[context][word] = bigram_dict[context][word]/unigram_dict[context]
       
    return bigram_dict_prob

def populate_bigram_smoothed_probabilities():
    list_of_words = read_file(sys.argv[1])
    bigram_dict = bigram_modelling_db(list_of_words)
    unigram_dict = unigram_modelling_db(list_of_words)
    bigram_dict_prob_smoothed = bigram_dict

    for context in bigram_dict:
        for word in bigram_dict[context]:
            bigram_dict_prob_smoothed[context][word] = (bigram_dict[context][word] + 1)/(unigram_dict[context] + len(unigram_dict))
       
    return bigram_dict_prob_smoothed

def bigram_smoothed_modelling_test(sentence):
        bigram_dict_prob_smoothed = populate_bigram_smoothed_probabilities()
        list_of_words = read_file(sys.argv[1])
        unigram_dict = unigram_modelling_db(list_of_words)

        probability_of_sentence = 0
        sentence = "phi " + sentence
        sentence = sentence.split()

        for i,word in enumerate(sentence):

           if word == "phi":
             continue

           word = word.lower()
           context = sentence[i-1].lower()

           if context not in bigram_dict_prob_smoothed.keys():
             probability_of_sentence = probability_of_sentence + math.log2(1/len(unigram_dict))
             continue 
 
           if word not in bigram_dict_prob_smoothed[context].keys():
             probability_of_sentence = probability_of_sentence + math.log2(1/((unigram_dict[context]+len(unigram_dict))))
             continue


           probability_of_sentence = probability_of_sentence + math.log2(bigram_dict_prob_smoothed[context][word])
        print("Smoothed Bigrams, logprob(S) =",roundoff(probability_of_sentence))

def populate_unigram_probabilities():
    list_of_words = read_file(sys.argv[1])
    unigram_dict = unigram_modelling_db(list_of_words)
    unigram_dict_prob = unigram_dict
    namesake_list = open(sys.argv[1],"r").read().split()

    for word in unigram_dict_prob:
           unigram_dict_prob[word] = unigram_dict_prob[word]/len(namesake_list)   
    
    return unigram_dict_prob



def phase_one(testfile):
    data = open(testfile, "r").read().split("\n")

    for sentence in data:
        print("S =", sentence)
        unigram_modelling_test(sentence)
        bigram_modelling_test(sentence)
        bigram_smoothed_modelling_test(sentence)

def unigram_modelling_test(sentence):
        unigram_dict_prob = populate_unigram_probabilities()
        probability_of_sentence = 0
        sentence = sentence.split()
        for i,word in enumerate(sentence):
           word =word.lower()
           if word not in unigram_dict_prob:
             probability_of_sentence = "undefined"
             break
           probability_of_sentence = probability_of_sentence + math.log2(unigram_dict_prob[word])
        print("Unsmoothed Unigrams, logprob(S) =",roundoff(probability_of_sentence))


def bigram_modelling_test(sentence):
        bigram_dict_prob = populate_bigram_probabilities()     
        probability_of_sentence = 0
        sentence = "phi " + sentence
        sentence = sentence.split()
        for i,word in enumerate(sentence):

           if word == "phi":
             continue

           word = word.lower()
           context = sentence[i-1].lower()

           if word not in bigram_dict_prob[context].keys():
             probability_of_sentence = "undefined"
             break

           probability_of_sentence = probability_of_sentence + math.log2(bigram_dict_prob[context][word])
        print("Unsmoothed Bigrams, logprob(S) =",roundoff(probability_of_sentence))

def next_word_generation(seed_word, bigram_dict_prob, counter):
       if counter == 0:
         print("\n")
         return
       random_int = random.randint(0,1)
       sum = 0
       for x in bigram_dict_prob[seed_word]:
           sum += bigram_dict_prob[seed_word][x]
           if random_int < sum:
              break
       print(x, end = " ")
       if x == "?" or x == "!" or x == ".":
          print("\n")
          return   
       counter -= 1
       next_word_generation(x, bigram_dict_prob, counter)

def sentence_generation(filename):
    bigram_dict_prob = populate_bigram_probabilities()
    data = open(filename,"r").read().split("\n")
    for seed in data:
       seed = seed.lower()
       print("Seed =", seed)
       i = 0
       while i != 10:
         i += 1             
         print("Sentence",i,":"," ",seed, end = " ") 
         next_word_generation(seed,bigram_dict_prob,10)

##########
##########
# TEST ON CADE MACHINE
# ADD LOGS TO THE PROBS
def main():
    if sys.argv[2] == "-test":
       phase_one(sys.argv[3])

    if sys.argv[2] == "-gen":
       sentence_generation(sys.argv[3])

main()