import string

def analyze_text(text):
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text.translate(translator).lower()
    
    words = clean_text.split()
    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
            
    return word_count

def get_frequent_words(word_dict, threshold=3):
    return [word for word, count in word_dict.items() if count > threshold]

if __name__ == "__main__":
    sample_text = """
    Python is great. Python is easy. Python is powerful.
    Code code code code. Loop loop loop.
    Test text for testing the test function.
    """

    counts = analyze_text(sample_text)
    print("Статистика слів:", counts)

    frequent = get_frequent_words(counts, 3)
    print("\nСлова, що зустрічаються більше 3 разів:", frequent)
