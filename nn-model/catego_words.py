import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from collections import Counter

nltk.download('punkt')

words = []
with open('objects.txt') as file: # tokenize every word
    while line := file.readline():
        words += word_tokenize(line)

all_hyper = []

# Example of categorization based on synonyms or hypernyms
def get_category(word):
    # Find synsets (synonyms) for the word
    synsets = wn.synsets(word)
    
    if not synsets:
        return "miscellaneous"
    
    # Check for common categories based on hypernyms (more general terms)
    for synset in synsets:
        hypernyms = synset.hypernyms()
        for hypernym in hypernyms:
            # print(hypernym)
            # with open('catego_results.txt', 'w') as file:
            #     file.write(''.join(hypernym))
            # Here you would map the hypernyms to your predefined categories
            all_hyper.append(hypernym)
            name = hypernym.lemma_names()[0]
            # print(name)
            if name in ["vehicle", "furniture", "place", "electronic", "clothing"]:
                return name

    return "miscellaneous"

def find_closest_hypernym(word, hypernyms): # finds the closest hypernym to the word
    synsets = wn.synsets(word)
    if not synsets:
        return None

    closest_hypernym = None
    max_similarity = 0

    for synset in synsets:
        for hypernym in hypernyms:
            similarity = synset.wup_similarity(hypernym)
            if similarity > max_similarity:
                closest_hypernym = hypernym
                max_similarity = similarity

    return closest_hypernym

# for word in words:
#     category = get_category(word)
#     categorized_words[category].append(word)

for word in words:
    closest_hypernym = find_closest_hypernym(word, all_hyper)

print(closest_hypernym)

# # Output the categorized words
# with open('catego_results.txt', 'w') as file:
#     for category, words in categorized_words.items():
#         file.write(f"{category.capitalize()}: {', '.join(words)}")


