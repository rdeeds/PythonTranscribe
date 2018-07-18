import json
import os


def rem_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    else:  ## Show an error ##
        print("Error: %s file not found" % filename)


def get_data_json(filename):
    with open('./jsonfilesfromtranscribe/'+filename) as json_data:
        d = json.load(json_data)
        return d


def create_file(filename, localsavename):
    a = get_data_json(filename)
    wordlist = []
    total = ''
    for item in a['results']['speaker_labels']['segments']:  #get list of times and words
        for word in item['items']:
            for segment in a['results']['items']:
                try:
                    if word['start_time'] == segment['start_time']:
                        wordlist.append(segment['alternatives'][0]['content'])
                except:
                    pass
        wordlist.insert(0, word['speaker_label'] + ':')
        res = ' '.join(wordlist)
        total = total + res + '\n\n'
        wordlist = []

    file = open('./final_txt_file/{}.txt'.format(localsavename), 'w')
    file.write(total)
    file.close()
