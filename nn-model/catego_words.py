import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# def preprocess_text(text):
#     # Tokenize the text
#     tokens = word_tokenize(text.lower())
    
#     # Remove stopwords and punctuation
#     stop_words = set(stopwords.words('english'))
#     tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    
#     # Lemmatize the tokens
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
#     return tokens

# def get_wordnet_pos(word):
#     tag = nltk.pos_tag([word])[0][1][0].upper()
#     tag_dict = {"J": wordnet.ADJ,
#                 "N": wordnet.NOUN,
#                 "V": wordnet.VERB,
#                 "R": wordnet.ADV}
#     return tag_dict.get(tag, wordnet.NOUN)

def semantic_similarity(word1, word2):
    synsets1 = wordnet.synsets(word1)
    synsets2 = wordnet.synsets(word2)
    
    max_similarity = 0
    
    for synset1 in synsets1:
        for synset2 in synsets2:
            similarity = synset1.path_similarity(synset2)
            if similarity and similarity > max_similarity:
                max_similarity = similarity
    
    return max_similarity

def find_most_similar_words(target_word, word_list, top_n=5):
    # target_word = preprocess_text(target_word)[0]
    # word_list = [preprocess_text(word)[0] for word in word_list]
    
    similarities = [(word, semantic_similarity(target_word, word)) for word in word_list]
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities[:top_n]

# Example usage
target_word = "happy"
word_list = ["joyful", "sad", "excited", "angry", "content", "pleased", "depressed", "ecstatic", "furious", "satisfied"]

most_similar = find_most_similar_words(target_word, word_list)

print(f"Words most similar to '{target_word}':")
for word, similarity in most_similar:
    print(f"{word}: {similarity:.4f}")