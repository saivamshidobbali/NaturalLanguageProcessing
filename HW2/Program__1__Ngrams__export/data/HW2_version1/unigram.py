def unigram():
    #Unigram
    #logspace
    #product of these probabilities
    
    test_file = open(sys.argv[3], "r")
    test_contents = test_file.read()
    test_data = test_contents.split()
    
    # handle word not here in dictionary case
    for test_word in test_data:
    	test_word = test_word.lower()
    	if test_word not in DB:
    	   print("Probability of",test_word,"===========",0)
    	   continue
    	print("Probability of",test_word,"===========",DB[test_word]/len(DB),"count of the word =============",DB[test_word])