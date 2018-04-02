#! /usr/bin/env python


# Problem 2 :
#
# Write a python script called "parse_battle.py" to input the output text of "WorldOfTextCraft" and
# keep track of each player's actions, displaying the type of action, the number of times it
# was used, and the total defense, healing, or damage.

import sys

class Stats:
    def __init__(self,name,attacks=0,multis=0,heals=0,defends=0):
        self.name=name
        self.attacks=attacks
        self.heals=heals
        self.defends=defends
        self.multis=multis
        self.alive=True        
    def __str__(self):
        s = self.name + ':\n'
        s += '   attack: %d damage\n'  % (self.attacks )
        s += '   multi-attack: %d damage\n'  % (self.multis )
        s += '   defended: %d defense\n'  % (self.defends )
        s += '   healed: %d points\n'  % (self.heals )
        return s
    
def main() : 

    # Open the file
    if len( sys.argv) < 2 :
        print 'Usage: python parse_battle.py <battle.txt>'
        return        
    infile = open( sys.argv[1] )

    # This is the data source for the PCs and NPCs:
    pcs = {}
    npcs = {}

    # Read all the lines of the file into a list. 
    lines = infile.readlines()
    
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
        #######
        if "Added entity" in line:
            pc = tokens[2]
            pcs[pc] = Stats(name=pc)
        if "Input boss" in line:
            npc = tokens[2]
            npcs[npc] = Stats(name=npc)

        #######
        # Now loop through the lines and check the actions.
        #######
        entity = tokens[0].rstrip(",")
        if "dead" in line or "died" in line :
            if entity in npcs:
                npcs[entity].alive = False
            if entity in pcs:
                pcs[entity].alive = False
        if entity in npcs and "attacks" in line and "shifts" not in line and nextlinetokens :
            # NPC attack lines look like:
            #
            #Arthas attacks Fordring with attack power 20
            #Fordring loses 10 hit points after attack 20 and defense 10
            #
            #or
            #
            #Arthas multi-attacks Fordring with attack power 8
            #Fordring loses 0 hit points after attack 8 and defense 10
            #
            attacktype = tokens[1]
            attackpower = int(tokens[-1])
            defender = nextlinetokens[0]
            loss = int(nextlinetokens[2])
            mitigated = attackpower - loss
            if pcs[defender].alive :
                if attacktype == "attacks":
                    npcs[entity].attacks += loss
                else :
                    npcs[entity].multis += loss
                pcs[defender].defends += mitigated
        if entity in pcs :
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
                healed = int(tokens[4])
                pcs[entity].heals += healed
                    

    # Done! Print it fancily
    for ipc,pc in pcs.iteritems():
        print pc

    print '\nBOSS: ',
    for inpc,npc in npcs.iteritems():
        print npc


if __name__ == "__main__" :
    main()
