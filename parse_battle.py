#! /usr/bin/env python


# Problem 2 :
#
# Write a python script called "parse_battle.py" to input the output text of "WorldOfTextCraft" and
# keep track of each player's actions, displaying the type of action, the number of times it
# was used, and the total defense, healing, or damage.
#
# We will read in the header and deduce the players automatically rather than relying on
# hard-coded values. As such, this can be used throughout the exam. 
#

import sys


class Stats:
    '''
    Stats class to keep track of the entity's statistics, such as
    amount of damage done (attacks), amount of healing done (heals),
    amount of damage mitigated (defends), or, for bosses, the multi-attacks. 
    This also checks if the entity is alive, and keeps its current hit points.
    The printout at the end is in the desired format so we can just use "print". 
    '''
    def __init__(self,name,attacks=0,multis=0,heals=0,defends=0,hp=0):
        self.name=name
        self.attacks=attacks
        self.heals=heals
        self.defends=defends
        self.multis=multis
        self.alive=True
        self.hp=hp
    def __str__(self):
        s = self.name + ':\n'
        s += '   attack: %d damage\n'  % (self.attacks )
        s += '   multi-attack: %d damage\n'  % (self.multis )
        s += '   defended: %d defense\n'  % (self.defends )
        s += '   healed: %d points\n'  % (self.heals )
        return s



'''
Main function. 

- Reads in the lines from the battle script output. 
- Deduces the party makeup. 
- Loops through each event in the log file and accumulates statistics. 
'''
def main() : 

    # Open the file
    if len( sys.argv) < 2 :
        print 'Usage: python parse_battle.py <battle.txt>'
        return        
    infile = open( sys.argv[1] )

    # This is the data structures to hold entities
    # (player characters, PCs, or non-player characters, NPCs)
    pcs = {}
    npcs = {}

    # Read all the lines of the file into a list. 
    lines = infile.readlines()
    infile.close()
    
    # Looping through lines
    for iline,line in enumerate(lines) :
        # Get a list of tokens for the line
        tokens = line.split()
        # Make sure there was input
        if len(tokens) == 0 :
            continue
        # Now tokenize the next line, if there is one.
        if iline < len(lines)-1:
            nextlinetokens = lines[iline+1].split()

        #######
        # Here is the header information that sets up the battle.
        # These will be used to initialize our dictionaries.
        #
        # It looks like this:        
        #    reading PC configuration
        #    Added entity:     Fordring (   Warrior): HP=  100, mana =     0, no target
        #    Added entity:       Thrall (    Priest): HP=  100, mana =   100, no target
        #    Added entity:     Mograine (     Rogue): HP=  100, mana =     0, no target
        #-->   [0]  [1]          [2]    [3]    [4]    [5]  [6]  [7]  [8]  [9] [10] [11]
        #    reading NPC configuration
        #    Input boss:       Arthas (      Boss): HP=  500, mana =     0, no target
        #-->   [0]  [1]          [2] [3]    [4]    [5]  [6]  [7]  [8]   [9] [10] [11]
        #    reading NPC action script
        #
        # We can subsequently read in the various pieces of information from the string tokens,
        # which are denoted above by the lines starting with -->
        #
        #######
        ######
        if "Added entity" in line:
            pc = tokens[2]
            hp = int (tokens[6].rstrip(','))
            pcs[pc] = Stats(name=pc,hp=hp)
        if "Input boss" in line:
            npc = tokens[2]
            hp = int (tokens[6].rstrip(','))
            npcs[npc] = Stats(name=npc,hp=hp)

        entity = tokens[0].rstrip(",")
        #######
        # Here are the stats for this turn. Tokenization is
        # the same as it is in the preceding block, where we read
        # in the header information. 
        #######
        if len(tokens) > 4:
            if tokens[3] == "HP" and tokens[2] != "Boss" :
                pcs[entity].hp = int(tokens[4].rstrip(','))
            if tokens[3] == "HP" and tokens[2] == "Boss" :
                npcs[entity].hp = int(tokens[4].rstrip(','))
            
        
        #######
        # Now loop through the lines and check the actions.
        #######

        # First check if anyone is dead. 
        if "dead" in line or "died" in line :
            if entity in npcs:
                npcs[entity].alive = False
            if entity in pcs:
                pcs[entity].alive = False

        # Now check NPCs attacking PCs (and make sure we
        # veto focus shifts like "Arthas shifts their attacks to Thrall")
        if entity in npcs and "attacks" in line and "shifts" not in line and nextlinetokens :
            # NPC attack lines look like:
            #
            #Arthas attacks Fordring with attack power 20
            #  [0]    [1]   [2]      [3]  [4]    [5]   [6]
            #   ^            ^                          ^-- AP
            #   |            |---defender
            #   |--attacker
            #Fordring loses 10 hit points after attack 20 and defense 10
            #  [0]    [1]   [2] [3]  [4]    [5]   [6]  [7] [8] [9]    [10]
            #   ^            ^                          ^               ^-defense
            #   |            |                          |--AP
            #   |            |-- loss
            #   |--- defender
            #   
            #
            #   We need to take these lines two at a time.
            #   The first line gives us the attacker and the defender.
            #   The second line gives us the defender's defense amount and HP loss.
            #   We can then compute the mitigated damage like:
            #
            #    mitigated = attackpower - loss
            #    defense += mitigated
            # 
            #
            attacktype = tokens[1]
            attackpower = int(tokens[-1])
            defender = nextlinetokens[0]
            loss = int(nextlinetokens[2])
            mitigated = attackpower - loss
            pcs[defender].hp -= loss
            if pcs[defender].alive :
                if attacktype == "attacks":
                    npcs[entity].attacks += loss
                else :
                    npcs[entity].multis += loss
                pcs[defender].defends += mitigated
        if entity in pcs :
            # PC attack lines look like:
            # "Mograine attacks Arthas with attack power 20"
            #  [0]      [1]      [2]   [3]  [4]    [5]   [6]
            #   ^                 ^                       ^--- attack power
            #   |                 |-- defender
            #   | 
            #   |--- attacker
            #
            #
            #  This can be taken one line at a time. 
            if "attacks" in line and "shifts" not in line and nextlinetokens :
                attacktype = tokens[1]
                attackpower = int(tokens[-1])
                defender = nextlinetokens[0]
                loss = int(nextlinetokens[2])
                mitigated = attackpower - loss
                if npcs[defender].alive :
                    if attacktype == "attacks":
                        pcs[entity].attacks += loss
                    else :
                        pcs[entity].multiattacks += loss
                    npcs[defender].defends += mitigated
            if "heals" in line and nextlinetokens:
                # PC heal lines look like:
                # Thrall heals Mograine for 12
                #  [0]   [1]   [2]      [3] [4]
                #   ^           ^            ^--healed
                #   |           |--healee
                #   |--healer
                #
                #  This one is easy, but we do have to check for
                #  overhealing, when the amount healed is less than the
                #  damage taken so far. In that case, 
                #  only count to get the player to 100 HP. 
                #
                healer = tokens[0]
                healee = tokens[2]
                healed = int(tokens[-1])
                pcs[entity].hp += healed
                # Make sure there is no over-healing
                if  healed + pcs[healee].hp > 100 :                    
                    healed = 100 - pcs[healee].hp
                pcs[entity].heals += healed
                pcs[healee].hp += healed
                
                    

    # Done! Print it fancily
    for ipc,pc in pcs.iteritems():
        print pc

    print '\nBOSS: ',
    for inpc,npc in npcs.iteritems():
        print npc


if __name__ == "__main__" :
    main()
