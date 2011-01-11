import sys
sys.path.append('../test_project/')
import settings

class ValuationSettings:
    site = settings.SITE_ID
    name = ""
    choice_list = []
    choices = ()
    def __init__(self, name, choices_list):
        self.name = name
        self.choices_list = choices_list
        self.choices = self.get_choices_from_list()

    def __unicode__():
        return self.name
        
    def get_choices_from_list(self):
        choices = []
        for i, choice in enumerate(self.choices_list):
            choices.append((i+1, choice.title()))
        return tuple(choices)

VS = ValuationSettings

default_name = getattr(settings,
                       'VALUATION_NAME',
                       'Value')
default_choices = getattr(settings,
                          'VALUATION_CHOICES',
                          ['low', 'medium', 'high'])

TEMPLATES = {
        'default':VS(default_name, default_choices),
        'rating':VS('rating',
                    ['bad', 'poor', 'average', 'good', 'excellent']),
        'like' :VS('like',
                   ['dislike', 'like'])
    }

template_settings = getattr(settings,'VALUATION_TEMPLATE', 'default')
VALUATION_SETTINGS = TEMPLATES.get(template_settings) or TEMPLATES.get('default')
