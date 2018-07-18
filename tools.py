import pprint
import random, csv
pp = pprint.PrettyPrinter(indent=1)

blank=[]

def p(element):
    test = 1
    if test==1:
        print('\n','*'*100,'\n')
        pp.pprint(element)
        print('\n', '*' * 100, '\n')



def randalphnum(count):
    string = 'abcdefghijklmnopqrstuwxyz1234567890'
    final=''
    while count > 0:
        a=''.join(random.choice(string))
        count-=1
        final=final+a
    return final


def fileout(listoflists):
    name=randalphnum(15)
    with open("static/fileupload/{}.csv".format(name), "w",newline='') as f:
        writer = csv.writer(f)
        writer.writerows(listoflists)