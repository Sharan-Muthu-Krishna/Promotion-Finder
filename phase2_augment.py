import pandas as pd
import random
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

def synonym_replacement(text, n=2):
    words = text.split()
    new_words = words.copy()
    random_word_list = list(set([word for word in words if wordnet.synsets(word)]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = wordnet.synsets(random_word)
        if synonyms:
            synonym = synonyms[0].lemmas()[0].name()
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break
    return ' '.join(new_words)

# Usage example
df = pd.read_csv('data/labeled_data.csv')
promo_df = df[df['is_promotional'] == 1]
augmented_texts = promo_df['text'].apply(lambda x: synonym_replacement(x))
augmented_df = promo_df.copy()
augmented_df['text'] = augmented_texts

# Combine original + augmented
final_df = pd.concat([df, augmented_df], ignore_index=True)
final_df.to_csv('data/augmented_labeled_data.csv', index=False)
print(f"Original rows: {len(df)}, After augmentation: {len(final_df)}")
