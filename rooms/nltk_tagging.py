from nltk import word_tokenize, pos_tag

def process_message(message):
    words = word_tokenize(message)
    tagged_words = pos_tag(words)

    pos_color_mapping = {
        'JJ': 'orange',
        'VBZ': 'red',
        'CC': 'black',
        'DT': 'violet',
        'NN': 'gray',
        'CD': 'green',
        'IN': 'pink',
        'PRP': 'yellow',
        'VB': 'teal',
    }

    colored_message = []

    for word, tag in tagged_words:
        color_class = pos_color_mapping.get(tag, 'white')
        colored_message.append(
            {
                'word' : word,
                'color_class' : color_class
            }
        )
    return colored_message