#Features not yet implemented: A-List options, specific tag numbers, interests values

from copy import deepcopy
from json import loads
from warnings import warn

from robobrowser import RoboBrowser

class CupidFilter:

    default_filter = {"tagOrder": [], "order_by":"SPECIAL_BLEND","gentation":[],"gender_tags":0,"orientation_tags":0,"minimum_age":18,"maximum_age":99,"age_recip":"on","locid":0,"radius":10,"lquery":"","location":{},"located_anywhere":0,"last_login":604800,"i_want":"other","they_want":"everyone","minimum_height":None,"maximum_height":None,"languages":0,"speaks_my_language":False,"ethnicity":[],"religion":[],"availability":"any","monogamy":"","looking_for":[],"smoking":[],"drinking":[],"drugs":[],"answers":[],"interest_ids":[],"education":[],"children":[],"cats":[],"dogs":[],"save_search":True,"limit":1000,"fields":"userinfo,thumbs,percentages,likes,last_contacts,online"}

    #These tags will allow shortcuts for setting gender, they_want, and gentation tags
    common_tags = {"E4M":               (0,"men",54),
                   "E4W":               (0,"women",57),
                   "E4E":               (0, "everyone", 63),
                   "W4M":               (1,"men",54),
                   "W4W":               (1,"women",57),
                   "W4E":               (1,"everyone",63),
                   "M4M":               (2,"men",54),
                   "M4W":               (2,"women",57),
                   "M4E":               (2,"everyone",63)}

    login_tags = {"now":                3600,
                  "day":                86400,
                  "week":               604800,
                  "month":              2678400,
                  "year":               31536000}
    
    options =  {"order_by":             ("SPECIAL_BLEND", "MATCH", "DISTANCE", "JOIN", "LOGIN", "ENEMY"),
                "gender_tags":          range(0,4194303),                           #Everyone = 0, Women = 1, Men = 2
                "orientation_tags":     range(0,4095),                              
                "gentation":            range(0,63),                                #Interested in men =  54, women = 57, everyone = 63
                "minimum_age":          range(18,99),
                "maximum_age":          range(18,99),
                "age_recip":            ("on", "off"),
                "radius":               range(0,2000),
                "located_anywhere":     (0,1),
                "they_want":            ("women","men","everyone"),
                "languages":            range(0,75),
                "speaks_my_language":   (True, False),
                "availability":         ("any", "single", "not_single"),
                "monogamy":             ("unknown", "yes", "no")}

    arr_options = {"ethnicity":         ("white", "pacific_islander", "native_american", "other", 
                                         "asian", "black", "hispanic_latin", "indian", "middle_eastern"),
                   "religion":          ("agnosticism", "atheism", "buddhism", "catholicism", "christianity", 
                                          "other", "sikh", "islam", "hinduism", "judaism"),
                   "looking_for":       ("new_friends", "short_term_dating", "long_term_dating", "casual_sex"),
                   "smoking":           ("no", "sometimes", "when_drinking", "trying_to_quit", "yes" ),
                   "drinking":          ("not_at_all", "socially", "rarely", "very_often", "often", "desperately"),
                   "drugs":             ("never", "sometimes", "often"),
                   "education":         ("high_school", "two_year_college", "college_university", "post_grad"),
                   "children":          ("wants_kids", "might_want", "doesn't_want", "has_one_or_more", "doesnt_have"),
                   "cats":               "has",
                   "dogs":               "has"}

    def __init__(self, browser = None):
        if browser is None:
            self.FilterBot = RoboBrowser(parser = "html.parser")
        else:
            self.FilterBot = browser
        self.current_filter = deepcopy(self.default_filter)
        self.match_cutoff = 0

    #Set current filter; options in arr_options must be passed as lists
    def set(self, **kwargs):
        for key in kwargs:
            val = kwargs[key]
            locale = {}
            if key == "match_cutoff" and val in range(0,100):
                self.match_cutoff = val
            elif key == "who" and val in self.common_tags:
                who = self.common_tags[val]
                self.current_filter["gender_tags"] = who[0]
                self.current_filter["they_want"] = who[1]
                self.current_filter["gentation"] = who[2]
            elif key == "where" and self._location_info(val, locale):
                self.current_filter["lquery"] = val
                self.current_filter["location"] = locale
                self.current_filter["locid"] = locale["results"][0]["locid"]
            elif (key == "minimum_height" or key == "maximum_height") and val in range(0,100):
                self.current_filter[key] = val * 254
            elif key == "last_login" and val in self.login_tags:
                self.current_filter["last_login"] = self.login_tags[val]
            elif key in self.options and val in self.options[key]:
                self.current_filter[key] = val
            elif key in self.arr_options and set(val).issubset(self.arr_options[key]):
                if not isinstance(val, list):
                    val = [val]
                for element in val:
                    if element not in self.current_filter[key]:
                        self.current_filter[key].append(element)
            else:
                warn("Invalid parameter in key " + key, UserWarning)
                    
    #clear current_filter, either by key or by resetting to default 
    def clear(self, *args):
        if len(args) == 0:
            self.current_filter = deepcopy(self.default_filter)
        else:
            for arg in args:
                if arg == "who":
                    self.clear("gentation", "gender_tags", "they_want")
                elif arg == "where":
                    self.clear("lquery", "location", "locid")
                elif arg == "match_cutoff": self.match_cutoff = 0 
                elif arg in self.current_filter:
                    self.current_filter[arg] = self.default_filter[arg]
                else:
                    warn("Invalid parameter in argument " + arg, UserWarning)
     
    #copies relevant data from json into filter
    def copy(self, s_filter):
        for key in s_filter:
            if key in self.current_filter:
                self.current_filter[key] = s_filter[key]

    #determines location information through okc api and returns it through {loc}
    def _location_info(self, zip_code, loc):
        url = 'https://www.okcupid.com/1/apitun/location/query?q=' + zip_code
        self.FilterBot.open(url)
        if self.FilterBot.response.status_code == 200 and loads(str(self.FilterBot.parsed))['message'][:3] == 'Ahh':
            loc.update(loads(str(self.FilterBot.parsed)))
            return True
        else:
            return False