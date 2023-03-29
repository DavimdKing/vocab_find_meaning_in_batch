import requests
import time
import openai
import pandas as pd
count = 0
raw_df = pd.read_excel('C:/Users/David Eng/Downloads/raw_vocab.xlsx')

vocabulary = raw_df.iloc[3100:3587, 0].tolist()


meanings = []
p_o_ss = []
examples = []
synonyms = []
antonyms = []
phonetics = []


def make_request_with_retry(url, headers, data, max_retries=5, timeout_duration=10):
    retries = 0

    while retries < max_retries:
        try:
            response = requests.post(url, headers=headers, json=data, timeout=timeout_duration)
            response.raise_for_status()  # Raise an exception if the response contains an HTTP error status code.
            return response.json()
        except (requests.Timeout, requests.HTTPError) as e:
            print(f"Request failed with error: {e}. Retrying...")
            retries += 1
            time.sleep(1)  # Optional: Wait for a short period before retrying the request.
    raise Exception(f"Failed to complete the request after {max_retries} retries.")

# Example usage:
url = 'https://api.openai.com/v1/chat/completions'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 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'
}
for word in vocabulary:
    data = {
        'messages': [
            {'role': 'system', 'content': f"give the meaning, part of speech, one example with more than five words, synonyms no more than three, antonyms no more than three, phonetic of the vocabulary: {word}. Answer me with the format of Meaning:, POS:, Example:, Synonyms:, Antonyms:, Phonetic:"}
        ],
        'max_tokens': 1000,
        'model': "gpt-3.5-turbo"
    }

    try:
        response = make_request_with_retry(url, headers, data)
        print(response)
    except Exception as e:
        print(f"Error: {e}")
    text = response['choices'][0]['message']['content']
    print(text)
    if "POS:" in text:
        meaning = text.split("Meaning:")[1].split("POS:")[0]
        p_o_s = text.split("POS:")[1].split("Example:")[0]
    elif "Part of speech:" in text:
        meaning = text.split("Meaning:")[1].split("Part of speech:")[0]
        p_o_s = text.split("Part of speech:")[1].split("Example:")[0]
    elif "part of speech:" in text:
        meaning = text.split("Meaning:")[1].split("part of speech:")[0]
        p_o_s = text.split("part of speech:")[1].split("Example:")[0]
    else:
        meanings.append("None")
        p_o_ss.append("None")
        examples.append("None")
        synonyms.append("None")
        antonyms.append("None")
        phonetics.append("None")
        continue

    example = text.split("Example:")[1].split("Synonyms:")[0]
    synonym = text.split("Synonyms:")[1].split("Antonyms:")[0]
    antonym = text.split("Antonyms:")[1].split("Phonetic:")[0]
    if "Phonetic" in text:
        if "Phonetic transcription" in text:
            phonetic = text.split("Phonetic transcription:")[1]
        else:
            phonetic = text.split("Phonetic:")[1]
    elif "Pronunciation" in text:
        phonetic = text.split("Pronunciation:")[1]
    elif "Phonetics" in text:
        phonetic = text.split("Phonetics:")[1]
    else:
        meanings.append("None")
        p_o_ss.append("None")
        examples.append("None")
        synonyms.append("None")
        antonyms.append("None")
        phonetics.append("None")
        continue

    # Add the extracted information to our lists
    meanings.append(meaning)
    p_o_ss.append(p_o_s)
    examples.append(example)
    synonyms.append(synonym)
    antonyms.append(antonym)
    phonetics.append(phonetic)
    count = count + 1

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
