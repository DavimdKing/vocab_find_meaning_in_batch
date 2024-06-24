Using ChatGPT API to get the meaning, POS, example, synonyms, antonyms and phonetics of a batch of vocabularies around 500 words each round. 

Method:
1. Raw vocabulary stores in Excel
2. program extracts the raw vocab by Pandas and become dataframe during processing
3. Use for loop to push each vocab to ChatGPT API to get the result
4. Use lists to store the result in order
5. Put all lists together and become a dataframe
6. Turn Dataframe to Excel and export to local computer
