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
               'teams':[
                        {'name':'bankers','defeatMessage':'All resistance is disabled!  You make off with the cash!'},
                        {'name':'robbers','defeatMessage':'Your opposition is too strong. You can not complete your task!\nYou Lose!'}
                        ],
               'duration':15,
               'timeOverMessage':'You\'ve waited too long and the sheriff walks in the door.\nYou lose!',
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
                'teams':[
                        {'name':'bankers','defeatMessage':'All resistance is disabled!  You make off with the cash!'},
                        {'name':'robbers','defeatMessage':'Your opposition is too strong. You can not complete your task!\nYou Lose!'}
                        ],
                'duration':25,
                'timeOverMessage':'You\'ve waited too long and the sheriff walks in the door.\nYou lose!', 
                'weaponList':['six-shooter','shotgun','rifle','saber'],
                'introduction':'''
You are desperate for cash and have no option
but to break into a busy bank.  You have 25
turns to fend off both the banker and a guard.

You will succeed if you disable both opponents
by intimidating, shooting, or beating them to a pulp.
                
Good luck, partner!                
                '''
                },
                
                {'title':'Apache Pass',
                'actors':[
                          {'location':(16,16),'team':'soldiers','isNPC':False},
                          {'name':'the captain','location':(8,15),'team':'soldiers','isNPC':True},
                          {'name':'an apache warrior','location':(0,9),'team':'apache', 'isNPC':True},
                          {'name':'an apache warrior','location':(0,12),'team':'apache', 'isNPC':True},
                          {'name':'the apache leader', 'location':(0,16),'team':'apache','isNPC':True}
                          ],
                'teams':[
                        {'name':'apache','defeatMessage':'You have disabled them all without reinforcements!  You survive!'},
                        {'name':'soldier','defeatMessage':'You and the captain could not make it happen!\nYou Lose!'}
                        ],
                'duration':25,
                'timeOverMessage':'You\'ve waited too long and the sheriff walks in the door.\nYou lose!', 
                'weaponList':['six-shooter','rifle','saber','bow'],
                'introduction':'''
You and your captain have been ambushed while on 
a scouting run.  You are staring down three apache
warriors.  If you can just survive 25 rounds, help
should arrive.  If both of you are disabled before
then, you lose.

Injuring opponents will make it harder for them to
harm you, so aim true.
                
Good luck, partner!                
                '''
                }]