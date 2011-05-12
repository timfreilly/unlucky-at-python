allWeapons=[{'name':'six-shooter',  'range':1,  'maxbullets':6,     'ammo':'bullets',  'isRange':True},
            {'name':'shotgun',      'range':2,  'maxbullets':3,     'ammo':'shells',   'isRange':True},
            {'name':'rifle',        'range':0,  'maxbullets':1,     'ammo':'bullets',  'isRange':True},
            {'name':'bow',          'range':0,  'maxbullets':1,     'ammo':'arrows',   'isRange':True},
            {'name':'saber',        'range':0,  'maxbullets':None,  'ammo':None,       'isRange':False}]

allScenarios=[{'title':'Lonely Day at the Bank',
               'actors':[
                         {'location':(16,16),'team':'robbers','isNPC':False},
                         {'name':'the banker','location':(0,0),'team':'bankers','isNPC':True}
                         ],    
               'duration':15,
               'weaponList':['six-shooter','shotgun','rifle','saber'],
               'introduction':'''
You have 15 turns to rob a bank.
You will succeed if you:
 - Intimidate him more than he intimidates you,
 - Hit him until he sustains a concussion,
 - or Inflict massive damage.

If he out-intimidates you or you sustain
massive wounds, you will be weak enough
to be captured.  Good luck, partner!
               '''    },
               
               {'title':'Busy Bank',
                'actors':[
                          {'location':(16,16),'team':'robbers','isNPC':False},
                          {'name':'the banker','location':(0,0),'team':'bankers', 'isNPC':True},
                          {'name':'the guard', 'location':(0,16),'team':'bankers','isNPC':True}
                          ],
                'duration':25,
                'weaponList':['six-shooter','shotgun','rifle','saber'],
                'introduction':'''
You are desperate for cash and have no option
but to break into a busy bank.  You have 25
turns to fend off both the banker and a guard.

You will succeed if you disable both opponents
by intimidating, shooting, or beating them to a pulp.
                
Good luck, partner!                
                '''
                }]