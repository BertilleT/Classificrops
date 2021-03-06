# converter.py
import argparse
from converter import *
from optimal_threshold import *
import json

d = {
    "f": "optimal_threshold", 
    "pa": "../../data/FR/FR_2020.csv", 
    "pl": "FR", 
    "l": "fr", 
    "s": "split+ratio+symetric",
    "t": 80
}

class keyvalue(argparse.Action):
    def __call__( self , parser, namespace,
                 values, option_string = None):
        setattr(namespace, self.dest, dict())
          
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


#parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser = argparse.ArgumentParser(description = 'arguments for converter tool',fromfile_prefix_chars='@')

parser.add_argument('-f',
                    help='the function : converter, optimal_threshold, percentages, evolution, or map')

parser.add_argument('-pa',
                    help='the path to the source classification')

parser.add_argument('-pl',
                    help='the place under study, it can be a country, region, lander. It can be situated in France, Belgium or Catalunya. ')

parser.add_argument('-l',
                    help='the language in which the classification is written')

parser.add_argument('-s',
                    help='the similarity method chosen')

parser.add_argument('-t', 
                    type = int, 
                    help='similarity threshold')

parser.add_argument('-c',  
                    help='classification : original or ICC.')

#parser.add_argument('-m', 
#                    type=str, 
#                    help='dictionary, instead of listing every arguments one by one')

parser.add_argument('-d', type=json.loads)

# adding an arguments 
parser.add_argument('--kwargs', 
                    nargs='*', 
                    action = keyvalue)
#mydict = args.d
#print(mydict)

args = parser.parse_args()
args.__dict__.update(d)
print(args)

args = parser.parse_args()
with open('dict.json') as json_file:
    #json to dict
    args.__dict__.update(json.load(json_file))

# Execute parse_args()
argparse_dict = vars(args)
argparse_dict.update(json_dict)

print(args.s)
print('If you read this line it means that you have provided '
    'all the parameters')

'''if args.f == 'converter':
    print('the function called is converter')
    if args.t is not None:
        converter(args.pa,args.pl,args.l, args.t, args.s)
    else: 
        print("you forgot to set a threshold value. For example -t 90")
elif args.f == 'optimal_threshold' :
    print('the function called is optimal_threshold')
    optimal_threshold(args.pa,args.pl,args.l,args.s)'''

#def test(**kargs):
#    if kargs['fct'] == 'converter':
#        converter()'''