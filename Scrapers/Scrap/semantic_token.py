def semantic_token(reddit_text):
    from nltk.tokenize import word_tokenize
    import json
    pargraph = reddit_text.strip().replace('\n', ' ')
    tokened_paragraph = word_tokenize(pargraph)
    # to populate, and lower_case
    with open('./Scrap/data.json') as data_to_read:
        data = json.loads(data_to_read.read())
    very_positive = data['very_positive']
    very_negative = data['very_negative']
    positive = data['positive']
    negative = data['negative']
    neutral = list()
    very_positive_count = 0
    positive_count = 0
    very_negative_count = 0
    negative_count = 0
    neutral_count = 0
    # semantic analysis begins here
    for token in tokened_paragraph:
        if token.lower() in very_positive:
            very_positive_count += 1
        elif token.lower() in positive:
            positive_count += 1
        elif token.lower() in very_negative:
            very_negative_count += 1
        elif token.lower() in negative:
            negative_count += 1
        else:
            neutral_count += 0
    if very_positive_count > positive_count and very_positive_count > very_negative_count and very_positive_count > negative_count and very_positive_count > neutral_count:
        return ('very_positive')
    elif positive_count > very_positive_count and positive_count > very_negative_count and positive_count > negative_count and positive_count > neutral_count:
        return ('positive')
    elif very_negative_count > very_positive_count and very_negative_count > positive_count and very_negative_count > negative_count and very_negative_count > neutral_count:
        return ('very_negative')
    elif negative_count > very_positive_count and negative_count > positive_count and negative_count > very_negative_count and negative_count > neutral_count:
        return ('negative')
    else:
        return ('neutral')
