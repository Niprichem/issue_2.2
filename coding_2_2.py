#-*- coding: utf-8 -*-

import os
import chardet
import json


def get_files_gener(dir_name, extention):
    return (f_name for f_name in os.listdir(dir_name) if f_name.endswith('.{}'.format(extention)))

def get_coding(data):
    return chardet.detect(data)['encoding']

def read_file(name):
    with open(name, 'rb') as f:
        data = f.read()
        coding = get_coding(data)
        return data.decode(coding)

def get_news_from_text_json(data):
    data_json = json.loads(data)['rss']['channel']['items']
    news_data = ''
    for item in data_json:
        news_data += '{} {} '.format(item['title'], item['description'])
    return news_data

def count_top_n_words(data, word_len, n_top_count):
    words = data.split(' ')
    words_set = set(words)
    words_count = [(word, words.count(word)) for word in words_set if len(word) > word_len]
    words_count.sort(key=lambda x: x[1])
    return words_count[-n_top_count:]

def print_result(name, words_count):
    words = [word for word, count in words_count]
    words.reverse()
    words_str = ', '.join(words)
    print('{}: {}\n'.format(name, words_str))

def main():
    news_path = u'news'
    word_len = 6
    n_top_count = 10
    names = get_files_gener(news_path, 'json')
    for name in names:
        data = read_file(os.path.join(news_path, name))
        news_data = get_news_from_text_json(data)
        result = count_top_n_words(news_data, word_len, n_top_count)
        print_result(name, result)

if __name__ == '__main__':
    main()
