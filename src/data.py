allWeapons=[{'name':'six-shooter',  'range':1,  'maxbullets':6,     'ammo':'bullets',  'isRange':True,  'flags':['fast fire']},
            {'name':'shotgun',      'range':2,  'maxbullets':2,     'ammo':'shells',   'isRange':True,  'flags':['double fire']},
            {'name':'rifle',        'range':0,  'maxbullets':4,     'ammo':'bullets',  'isRange':True,  'flags':[]},
            {'name':'bow',          'range':0,  'maxbullets':1,     'ammo':'arrows',   'isRange':True,  'flags':['instant reload']}, 
            {'name':'saber',        'range':0,  'maxbullets':None,  'ammo':None,       'isRange':False, 'flags':[]},
            {'name':'tomahawk',     'range':0,  'maxbullets':None,  'ammo':None,       'isRange':False, 'flags':[]}]

allScenarios=[{'title':'Lonely Day at the Bank',
               'actors':[
                         {'location':(16,16),'team':'robbers','isNPC':False,'isHidden':False},
                         {'name':'the banker','location':(0,0),'team':'bankers','isNPC':True,'isHidden':False},
                         {'name':'the sheriff','location':(8,16),'team':'bankers','isNPC':True,'isHidden':True}
                         ],    
               'teams':[
                        {'name':'bankers','weaponList':['six-shooter','shotgun'],'defeatMessage':'All resistance is disabled!  You make off with the cash!'},
                        {'name':'robbers','weaponList':['six-shooter','shotgun','rifle','saber'],'defeatMessage':'Your opposition is too strong. You can not complete your task!\nYou Lose!'}
                        ],
               'events':[
                         {'condition':'self.roundCount > 15',
                          'actions':[
                                    "self.revealActor('the sheriff')"
                                    ]}
                        ],
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
                          {'location':(16,16),'team':'robbers','isNPC':False,'isHidden':False},
                          {'name':'the banker','location':(0,0),'team':'bankers', 'isNPC':True,'isHidden':False},
                          {'name':'the guard', 'location':(0,16),'team':'bankers','isNPC':True,'isHidden':False}
                          ],
                'teams':[
                        {'name':'bankers','weaponList':['six-shooter','shotgun'],'defeatMessage':'All resistance is disabled!  You make off with the cash!'},
                        {'name':'robbers','weaponList':['six-shooter','shotgun','rifle','saber'],'defeatMessage':'Your opposition is too strong. You can not complete your task!\nYou Lose!'}
                        ],
               'events':[{'condition':'self.roundCount > 25',
                          'actions':[
                                    "self.endBattle('You have waited too long and the sheriff walks in the door.  You lose!',victory=False)"
                                    ]}
                         ],
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
                          {'location':(16,16),'team':'soldiers','isNPC':False,'isHidden':False},
                          {'name':'the captain','location':(8,15),'team':'soldiers','isNPC':True,'isHidden':False},
                          {'name':'an apache warrior','location':(0,9),'team':'apache', 'isNPC':True,'isHidden':False},
                          {'name':'an apache warrior','location':(0,12),'team':'apache', 'isNPC':True,'isHidden':False},
                          {'name':'the apache leader', 'location':(0,16),'team':'apache','isNPC':True,'isHidden':False}
                          ],
                'teams':[
                        {'name':'apache','weaponList':['bow','tomahawk'],'defeatMessage':'You have disabled them all without reinforcements!  You survive!'},
                        {'name':'soldiers','weaponList':['six-shooter','rifle','saber'],'defeatMessage':'You and the captain could not make it happen!\nYou Lose!'}
                        ],
               'events':[{'condition':'self.roundCount > 25',
                          'actions':[
                                    "self.endBattle('You have lasted long enough for help to arrive.  You win!',victory=True)"
                                    ]}
                         ],                              
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