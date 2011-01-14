import sys
import settings

'''
This is a bit non-conventional.
Defines the settings for the valuate app according to the django-project
settings.
Available Settings:
VALUATION_NAME:     Name for the type of valuation. Eg: rating, like etc.
VALUATION_CHOICES:  A list of choices which will be used as the choice set
                    for users. Each choice will be assigned an integer value,
                    going from low to high.   
                    Eg:
                    ['low', 'medium', 'high'] => ((1, 'low'),
                                                  (2, 'medium'),
                                                  (3, 'high'))
VALUATION_TEMPLATE: Name of a predefined template.
                    Currently available: rating, like.

TODO:
 - Get rid of this and have multiple types of valuations available in
   one module.   
'''

class ValuationSettings:
    '''
    Class for storing the settigs info. 
    '''
    site = settings.SITE_ID
    name = ""
    choice_list = []
    choices = ()
    def __init__(self, name, choices_list):
        self.name = name
        self.choices_list = choices_list        
        self.choices = self.get_choices()        
        self.choices_dict = dict(zip(choices_list, range(1, len(choices_list)+1)))
        self.choices_dict_rev = dict(zip(range(1, len(choices_list)+1), choices_list) )
                                 
    def __unicode__(self):
        return self.name

    def get_choice_value(self, choice):
        return self.choices_dict[choice]
    
    def get_choices(self):
        choices = []
        for i, choice in enumerate(self.choices_list):
            choices.append((i+1, choice.title()))            
        return tuple(choices)
    
VS = ValuationSettings

#Default name of valuation form field used if no template is set. 
default_name = getattr(settings,
                       'VALUATION_NAME',
                       'Value')

#Default set of choices to be used if no template is set
default_choices = getattr(settings,
                          'VALUATION_CHOICES',
                          ['low', 'medium', 'high'])

#Predefined templates
TEMPLATES = {
        'default':VS(default_name, default_choices),
        'rating':VS('rating',
                    ['bad', 'poor', 'average', 'good', 'excellent']),
        'like' :VS('like',
                   ['dislike', 'like'])
    }

#GET the template name from the settings file.
template_settings = getattr(settings,'VALUATION_TEMPLATE', 'default')
valuation_settings = TEMPLATES.get(template_settings) or TEMPLATES.get('default')
