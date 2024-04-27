import nltk

def calculate_grammar_percentage(text):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Initialize a counter for correct sentences
    correct_sentences = 0

    # Iterate through each sentence
    for sentence in sentences:
        # Tokenize the sentence into words
        words = nltk.word_tokenize(sentence)
        
        # Perform part-of-speech tagging
        pos_tags = nltk.pos_tag(words)
        
        # Count the number of verbs in the sentence
        num_verbs = sum(1 for _, tag in pos_tags if tag.startswith('VB'))

        # If the number of verbs is greater than 0, consider the sentence correct
        if num_verbs > 0:
            correct_sentences += 1

    # Calculate the percentage of correct sentences
    grammar_percentage = (correct_sentences / len(sentences)) * 100

    return grammar_percentage

# Example text
text = """
Natural Language Processing (NLP) is a subfield of linguistics, computer science, information engineering, and artificial intelligence concerned with the interactions between computers and human (natural) languages, in particular how to program computers to process and analyze large amounts of natural language data.
It can be challenging to ensure perfect grammar in every sentence, but NLP techniques can help improve the overall grammatical correctness of text.
"""

# Calculate the grammar percentage
percentage = calculate_grammar_percentage(text)
print(f"Grammar percentage: {percentage:.2f}%")


# python -m nltk.downloader averaged_perceptron_tagger
# python -m nltk.downloader punkt