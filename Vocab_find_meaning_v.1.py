import openai
import pandas as pd
import time

# Replace YOUR_API_KEY with your OpenAI API key
count=0
raw_df = pd.read_excel('C:/Users/David Eng/Downloads/raw_vocab.xlsx')


openai.api_key = "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"
vocabulary = raw_df.iloc[1200:1300, 0].tolist()

print(vocabulary)


meanings = []
p_o_ss = []
examples = []
synonyms = []
antonyms = []
phonetics = []

# Loop through each vocabulary word and generate information using GPT-3
for word in vocabulary:
    print(count)
    start_time = time.time()
    prompt = f"give the meaning, part of speech, one example with more than five words, synonyms no more than three, antonyms no more than three, phonetic of a vocabulary: {word}. Answer me with the format of Meaning:, POS:, Example:, Synonyms:, Antonyms:, Phonetic:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
    except:
        meanings.append("None")
        p_o_ss.append("None")
        examples.append("None")
        synonyms.append("None")
        antonyms.append("None")
        phonetics.append("None")


        continue
    end_time = time.time()
    GPT_get_time = end_time - start_time
    print("Elapsed time: ", GPT_get_time, "seconds")
    text = response.choices[0].message.content
    print(text)


    meaning = text.split("Meaning: ")[1].split("POS: ")[0]
    p_o_s = text.split("POS: ")[1].split("Example: ")[0]
    example = text.split("Example: ")[1].split("Synonyms: ")[0]
    synonym = text.split("Synonyms: ")[1].split("Antonyms: ")[0]
    antonym = text.split("Antonyms: ")[1].split("Phonetic: ")[0]
    if "Phonetic" in text:
        if "Phonetic transcription" in text:
            phonetic = text.split("Phonetic transcription: ")[1]
        else:
            phonetic = text.split("Phonetic: ")[1]
    elif "Pronunciation" in text:
        phonetic = text.split("Pronunciation: ")[1]
    elif "Phonetics" in text:
        phonetic = text.split("Phonetics: ")[1]


    # Add the extracted information to our lists
    meanings.append(meaning)
    p_o_ss.append(p_o_s)
    examples.append(example)
    synonyms.append(synonym)
    antonyms.append(antonym)
    phonetics.append(phonetic)
    count = count+1

    print(count)
# Create a DataFrame object with the extracted information
print("for loop finished")
df = pd.DataFrame({
    'vocabulary': vocabulary,
    'part of speech': p_o_ss,
    'meaning': meanings,
    'example': examples,
    'synonyms': synonyms,
    'antonyms': antonyms,
    'phonetics': phonetics
})

# Write the DataFrame to an Excel file
with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)

