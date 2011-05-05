allWeapons=[{'name':'six-shooter',  'range':1,  'maxbullets':6,   'sharp':0,    'isRange':True},
            {'name':'shotgun',      'range':2,  'maxbullets':3,   'sharp':10,   'isRange':True},
            {'name':'rifle',        'range':0,  'maxbullets':1,   'sharp':30,   'isRange':True},
            {'name':'saber',        'range':0,  'maxbullets':10,  'sharp':20,   'isRange':False}]

allScenarios=[{'title':'Lonely Day at the Bank',    
               'playerCount':1,
               'playerLocations':[(16,16)],
               'npcCount':1,
               'npcLocations':[(0,0)],
               'npcNames':['the banker'],
               'duration':10,
               'introduction':'''
You have 10 turns to rob a bank.
You will succeed if you:"
 - Intimidate him more than he intimidates you,
 - Hit him until he sustains a concussion,
 - or Inflict massive damage.

If he out-intimidates you or you sustain
massive wounds, you will be weak enough
to be captured.  Good luck, partner!
               '''    },
               
               {'title':'Busy Bank',
                'playerCount':1,
                'playerLocations':[(16,16)],
                'npcCount':2,
                'npcLocations':[(0,0),(0,0)],
                'npcNames':['the banker','the guard'],
                'duration':20,
                'introduction':'''
You are desperate for cash and have no option
but to break into a busy bank.  You have 20
turns to fend off both the banker and a guard.

You will succeed if you disable both opponents
by intimidating, shooting, or beating them to a pulp.
                
Good luck, partner!                
                '''
                }]