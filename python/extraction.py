import nltk
from textblob import TextBlob
import time
from twitter import TwitterStream
import yaml, os
from twitter import *
import re
import gmplot
import googlemaps
import pyrebase


road_type_list = [
    'allee', 'alley', 'ally', 'aly', 'anex', 'annex', 'annx', 'anx',
    'arc', 'arcade', 'av', 'ave', 'aven', 'avenu', 'avenue', 'avn', 'avnue',
    'bayoo', 'bayou', 'bch', 'beach', 'bend', 'bg', 'bgs', 'bl', 'blf',
    'blfs', 'bluf', 'bluff', 'bluffs', 'blvd', 'bnd', 'bot', 'bottm',
    'bottom', 'boul', 'boulevard', 'boulv', 'br', 'branch', 'brdge', 'brg',
    'bridge', 'brk', 'brks', 'brnch', 'brook', 'brooks', 'btm', 'burg',
    'burgs', 'byp', 'bypa', 'bypas', 'bypass', 'byps', 'byu', 'camp', 'canyn',
    'canyon', 'cape', 'causeway', 'causwa', 'causway', 'cen', 'cent',
    'center', 'centers', 'centr', 'centre', 'ci', 'cir', 'circ', 'circl',
    'circle', 'circles', 'cirs', 'ck', 'clb', 'clf', 'clfs', 'cliff',
    'cliffs', 'club', 'cmn', 'cmns', 'cmp', 'cnter', 'cntr', 'cnyn', 'common',
    'commons', 'cor', 'corner', 'corners', 'cors', 'course', 'court',
    'courts', 'cove', 'coves', 'cp', 'cpe', 'cr', 'crcl', 'crcle', 'crecent',
    'creek', 'cres', 'crescent', 'cresent', 'crest', 'crk', 'crossing',
    'crossroad', 'crossroads', 'crscnt', 'crse', 'crsent', 'crsnt', 'crssing',
    'crssng', 'crst', 'crt', 'cswy', 'ct', 'ctr', 'ctrs', 'cts', 'curv',
    'curve', 'cv', 'cvs', 'cyn', 'dale', 'dam', 'div', 'divide', 'dl', 'dm',
    'dr', 'driv', 'drive', 'drives', 'drs', 'drv', 'dv', 'dvd', 'est',
    'estate', 'estates', 'ests', 'ex', 'exp', 'expr', 'express', 'expressway',
    'expw', 'expy', 'ext', 'extension', 'extensions', 'extn', 'extnsn',
    'exts', 'fall', 'falls', 'ferry', 'field', 'fields', 'flat', 'flats',
    'fld', 'flds', 'fls', 'flt', 'flts', 'ford', 'fords', 'forest', 'forests',
    'forg', 'forge', 'forges', 'fork', 'forks', 'fort', 'frd', 'frds',
    'freeway', 'freewy', 'frg', 'frgs', 'frk', 'frks', 'frry', 'frst', 'frt',
    'frway', 'frwy', 'fry', 'ft', 'fwy', 'garden', 'gardens', 'gardn',
    'gateway', 'gatewy', 'gatway', 'gdn', 'gdns', 'glen', 'glens', 'gln',
    'glns', 'grden', 'grdn', 'grdns', 'green', 'greens', 'grn', 'grns',
    'grov', 'grove', 'groves', 'grv', 'grvs', 'gtway', 'gtwy', 'harb',
    'harbor', 'harbors', 'harbr', 'haven', 'havn', 'hbr', 'hbrs', 'height',
    'heights', 'hgts', 'highway', 'highwy', 'hill', 'hills', 'hiway', 'hiwy',
    'hl', 'hllw', 'hls', 'hollow', 'hollows', 'holw', 'holws', 'hrbor', 'ht',
    'hts', 'hvn', 'hway', 'hwy', 'inlet', 'inlt', 'island', 'islands',
    'isle', 'isles', 'islnd', 'islnds', 'iss', 'jct', 'jction', 'jctn',
    'jctns', 'jcts', 'junction', 'junctions', 'junctn', 'juncton', 'key',
    'keys', 'knl', 'knls', 'knol', 'knoll', 'knolls', 'ky', 'kys', 'la',
    'lake', 'lakes', 'land', 'landing', 'lane', 'lanes', 'lck', 'lcks', 'ldg',
    'ldge', 'lf', 'lgt', 'lgts', 'light', 'lights', 'lk', 'lks', 'ln', 'lndg',
    'lndng', 'loaf', 'lock', 'locks', 'lodg', 'lodge', 'loop', 'loops', 'lp',
    'mall', 'manor', 'manors', 'mdw', 'mdws', 'meadow', 'meadows', 'medows',
    'mews', 'mi', 'mile', 'mill', 'mills', 'mission', 'missn', 'ml', 'mls',
    'mn', 'mnr', 'mnrs', 'mnt', 'mntain', 'mntn', 'mntns', 'motorway',
    'mount', 'mountain', 'mountains', 'mountin', 'msn', 'mssn', 'mt', 'mtin',
    'mtn', 'mtns', 'mtwy', 'nck', 'neck', 'opas', 'orch', 'orchard', 'orchrd',
    'oval', 'overlook', 'overpass', 'ovl', 'ovlk', 'park', 'parks', 'parkway',
    'parkways', 'parkwy', 'pass', 'passage', 'path', 'paths', 'pike', 'pikes',
    'pine', 'pines', 'pk', 'pkway', 'pkwy', 'pkwys', 'pky', 'pl', 'place',
    'plain', 'plaines', 'plains', 'plaza', 'pln', 'plns', 'plz', 'plza',
    'pne', 'pnes', 'point', 'points', 'port', 'ports', 'pr', 'prairie',
    'prarie', 'prk', 'prr', 'prt', 'prts', 'psge', 'pt', 'pts', 'pw', 'pwy',
    'rad', 'radial', 'radiel', 'radl', 'ramp', 'ranch', 'ranches', 'rapid',
    'rapids', 'rd', 'rdg', 'rdge', 'rdgs', 'rds', 'rest', 'ri', 'ridge',
    'ridges', 'rise', 'riv', 'river', 'rivr', 'rn', 'rnch', 'rnchs', 'road',
    'roads', 'route', 'row', 'rpd', 'rpds', 'rst', 'rte', 'rue', 'run', 'rvr',
    'shl', 'shls', 'shoal', 'shoals', 'shoar', 'shoars', 'shore', 'shores',
    'shr', 'shrs', 'skwy', 'skyway', 'smt', 'spg', 'spgs', 'spng', 'spngs',
    'spring', 'springs', 'sprng', 'sprngs', 'spur', 'spurs', 'sq', 'sqr',
    'sqre', 'sqrs', 'sqs', 'squ', 'square', 'squares', 'st', 'sta', 'station',
    'statn', 'stn', 'str', 'stra', 'strav', 'strave', 'straven', 'stravenue',
    'stravn', 'stream', 'street', 'streets', 'streme', 'strm', 'strt',
    'strvn', 'strvnue', 'sts', 'sumit', 'sumitt', 'summit', 'te', 'ter',
    'terr', 'terrace', 'throughway', 'tl', 'tpk', 'tpke', 'tr', 'trace',
    'traces', 'track', 'tracks', 'trafficway', 'trail', 'trailer', 'trails',
    'trak', 'trce', 'trfy', 'trk', 'trks', 'trl', 'trlr', 'trlrs', 'trls',
    'trnpk', 'trpk', 'trwy', 'tunel', 'tunl', 'tunls', 'tunnel', 'tunnels',
    'tunnl', 'turn', 'turnpike', 'turnpk', 'un', 'underpass', 'union',
    'unions', 'uns', 'upas', 'valley', 'valleys', 'vally', 'vdct', 'via',
    'viadct', 'viaduct', 'view', 'views', 'vill', 'villag', 'village',
    'villages', 'ville', 'villg', 'villiage', 'vis', 'vist', 'vista', 'vl',
    'vlg', 'vlgs', 'vlly', 'vly', 'vlys', 'vst', 'vsta', 'walk',
    'walks', 'wall', 'way', 'ways', 'well', 'wells', 'wl', 'wls', 'wy', 'xc',
    'xing', 'xrd', 'xrds'
]

directions = ['n', 's', 'e', 'w',
              'ne', 'nw', 'se', 'sw',
              'north', 'south', 'east',
              'west','northeast',
              'northwest', 'southeast',
              'southwest']

flood_list = ['flooded','flood','flooding']

numbered_streets = ['st','rd','nd','th']



class twitter_extraction:
    def __init__(self):
        self.flood_term = None
        self.flood_index = None
        self.road_type = None
        self.road_type_index = None
        self.road_name = None
        self.city_state = None
        self.city_probability = None
        self.road_probability = None
        self.lat = None
        self.lng = None
        self.verified = False
        

    def connect_twitter(self,config_filepath='/xxxx/xxxx/.xxxx/xxxx.yml'):
        credentials = yaml.load(open(os.path.expanduser(config_filepath)))
        credentials = credentials['twitter']
        token = credentials.get('token')
        token_secret = credentials.get('token_secret')
        consumer_key = credentials.get('consumer_key')
        consumer_secret = credentials.get('consumer_secret')
        t = TwitterStream(auth=OAuth(token, token_secret,
                                     consumer_key, consumer_secret))
        return t


    def connect_google(self,config_filepath='/xxxx/xxxx/.xxxx/xxxx.yml'):
        credentials = yaml.load(open(os.path.expanduser(config_filepath)))
        credentials = credentials['google']
        key = credentials.get('key')
        g = googlemaps.Client(key=key)
        return g


    def connect_firebase(self):
        config = {
        "apiKey": "xxxx",
        "authDomain": "xxxx",
        "databaseURL": "xxxx",
        "storageBucket": "xxxx",
        "serviceAccount": "/xxxx/xxxx/.json/xxxx-firebase-adminsdk-xxxx-xxxx.json"
        }
        firebase = pyrebase.initialize_app(config)
        return firebase


    def update_database(self,db,past_lat,past_lng): #,new_lat,new_lng):
        if (type(past_lat) or type(past_long)) != list:
            db.child("coordinates").update({"lat":[past_lat,self.lat]})
            db.child("coordinates").update({"long":[past_lng,self.lng]})
        else:
            past_lat.append(self.lat)
            past_lng.append(self.lng)
            db.child("coordinates").update({"lat":past_lat})
            db.child("coordinates").update({"long":past_lng})


    def parse_database(self,auth):
        db = auth.database()
        coor_key = db.child("coordinates").get()
        coor_values = coor_key.val()
        past_lat = coor_values['lat']
        past_lng = coor_values['long']
        # new_lat = self.lat
        # new_lng = self.long
        self.update_database(db,past_lat,past_lng) #,new_lat,new_lng)

        
    def clean_tokens(self,tokens):
        clean_token_list = []
        for i in range(len(tokens)):
            tokens[i] = "".join(re.findall(r'[0-9]?[a-z]?', tokens[i].lower())) # house#'s same?
        clean = list(filter(None, tokens))
        clean_token_list.append(clean)
        return clean_token_list


    #############################################
    #### Extract other info. from json file. ####
    #############################################
 
        
    def tokenize(self, string):
        token_blob = TextBlob(string).tokens
        token_list = [i for i in token_blob]
        return token_list 

    
    def search_for_flood(self,tokens):
        for i in range(len(tokens)):
            if tokens[i] in flood_list:
                self.flood_term = tokens[i]
                self.flood_index = i
            else:
                continue


    def alphanumeric_verification(self, token_list, tags):
        possible_street = token_list[self.road_type_index-1]
        if possible_street[-2:] in numbered_streets:
            if re.findall(r'[0-9]?',possible_street[0:-2]):
                self.road_name = possible_street
                self.road_probability = 'high'
                if token_list[self.road_type_index-2] in directions:
                    self.road_name = " ".join([token_list[self.road_type_index-2],
                                            self.road_name])
                    return
                else:
                    return
            else:
                if re.findall(r'[a-z]',possible_street) == tags[self.road_type_index-1][0]:
                    self.road_name = possible_street
                    self.road_probability = 'high'
                    if token_list[self.road_type_index-1] in directions:
                        self.road_name = " ".join([token_list[self.road_type_index-1],
                                                 self.road_name])
                    else:
                        return
                else:
                    return
        else:
            if re.findall(r'[0-9]',possible_street) == tags[self.road_type_index-1][0]:
                self.road_name = possible_street
                self.road_probability = 'low'
            else:
                return


    def synthax_analysis(self, token_list, tags):
        minus_one_tag = tags[self.road_type_index-1][1]
        minus_one_word = tags[self.road_type_index-1][0]
        minus_two_tag = tags[self.road_type_index-2][1]
        minus_two_word = tags[self.road_type_index-2][0]
        
        try:
            minus_three_tag = tags[self.road_type_index-3 if self.road_type_index-3 > 0 else 1000][1]
            minus_three_word = tags[self.road_type_index-3 if self.road_type_index-3 > 0 else 1000][0]
        except:
            minus_three_tag = None
            minus_three_word = None

        if minus_one_tag != ('NN' or 'NNP'):
            if minus_one_tag == 'VBD':
                if minus_two_tag == 'IN':
                    self.road_name = minus_one_word
                    self.road_probability = 'high'
                    return
                elif minus_two_tag == ('NN' or 'NNP'): 
                    self.road_name = " ".join([minus_two_word,minus_one_word])
                    self.road_probability = 'low'
                    return
                else:
                    self.road_name = minus_one_word
                    self.road_probability = 'low'
                    return
            elif minus_one_tag == 'IN':
                self.road_name = minus_one_word
                self.road_probability = 'low'
                return
            else:
                self.road_name = minus_one_word
                self.road_probability = 'low'
                return
        else:
            if minus_two_tag == ('NN' or 'NNP'):
                self.road_name = " ".join([minus_two_word,minus_one_word])
                self.road_probability = 'high'
                return
            elif minus_two_tag == ('JJ'):
                self.road_name = " ".join([minus_two_word,minus_one_word])
                self.road_probability = 'high'
                return
            elif minus_two_tag == ('IN'):
                self.road_name = minus_one_word
                self.road_probability = 'high'
                return
            else:
                self.road_name = minus_one_word
                self.road_probability = 'low'
                return


    def first_verification(self,token_list):
        tags = self.pos(token_list)
        index = self.road_type_index-1
        if index >= 1:
            if tags[index][1] == 'CD':
                return self.alphanumeric_verification(token_list,tags)
            else:
                return self.synthax_analysis(token_list,tags)
        elif index == 0:
            self.road_name = tags[index][0]
            self.road_probability = 'high'
            return
        else:
            return


    def location_pull(self,response):
        try:
            if response['place']['place_type'] == 'admin':
                self.city_state = response['location']
                self.city_probability = 'low'
            else:
                self.city_state = response['place']['full_name']
                self.city_probability = 'high'
        except IndexError:
            self.city_state = response['place']['full_name']
            self.city_probability = 'high'


    def final_verification(self,response): # Possibly look for house numbers as well ?
        self.location_pull(response)
        g = self.connect_google()
        coord = g.geocode(self.road_name+' '+self.road_type+','+self.city_state)
        print ('Found flood on',self.road_name,self.road_type,'in',self.city_state)
        try:
            self.lat = coord[0]['geometry']['location']['lat']
            self.lng = coord[0]['geometry']['location']['lng']
            self.verified = True
        except:
            self.reinit()


    def search_for_road(self,token_list):
        for i in range(len(token_list)):
            if token_list[i] in road_type_list:
                self.road_type = token_list[i]
                self.road_type_index = i
                self.first_verification(token_list)
                return 
            else: 
                continue
        self.reinit()

            
    def pos(self,token_list):
        tags = TextBlob(" ".join(token_list)).tags
        return tags


    def make_html(self):
        gmap = gmplot.GoogleMapPlotter(self.lat,self.lng,18)
        gmap.heatmap([self.lat], [self.lng], radius=30)
        gmap.draw("actual_pull.html")


    def reinit(self):
        self.flood_term = None
        self.flood_index = None
        self.road_type = None
        self.road_type_index = None
        self.road_name = None
        self.city_state = None
        self.probability = None
        self.lat = None
        self.lng = None
        self.verified = False

    
    def main(self):
        t = self.connect_twitter()
        sf = t.statuses.filter(locations='-122.524681,37.635985,-122.352848,37.813581')
        for response in sf:
            token_list = self.clean_tokens(self.tokenize(response['text']))[0]
            self.search_for_flood(token_list)
            if self.flood_term == None:
                continue
            else:
                self.search_for_road(token_list)
                if self.road_name:
                    self.final_verification(response)
                    if self.verified:
                        fire = self.connect_firebase()
                        self.parse_database(fire)
                        self.reinit()
                        continue
                    else:
                        self.reinit()
                        continue


if __name__ == '__main__':
    twitter_extraction().main()