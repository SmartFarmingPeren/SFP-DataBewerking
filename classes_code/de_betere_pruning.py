from Branch import Branch
from utilities.debug_log_functions import debug_message, info_message, warning_message

'''
Pruning rules:
[1.] If a one year old branch comes from a two year old branch, 
        the  branch needs to be cut about 5 cm from the fork.
        
[2.] If a one year old branch forks from a leader, 
        the branch needs to be cut 5 cm from the top.

[3.] When more than one branch spring from a two year old branch, 
        the branch from the fork will be cut 5 cm from the fork and the others close to the branch it grown from.

[4.] If new branches spring from a 3+ year old branch, 
        the branch needs to be cut close to the fork as well.
'''

def get_pruning_type(branch : Branch):
    if branch.age == 1:
        if branch.is_pruned == False:
            if branch.parent.is_leader:
                debug_message("RULE 2: Branch age:{0}, Parent is leader:{1}".format(branch.age, branch.parent.is_leader))
                RULE2()
                branch.is_pruned = True
        else:
            warning_message("Child already pruned")

    elif branch.age == 2:
        first_child_found = False
        for child in branch.children:
            if child.is_pruned == False:
                if child.age == 1:
                    if not first_child_found:
                        first_child_found = True
                        debug_message("RULE 1(RULE3): Branch age:{0}, Child age:{1}".format(branch.age, child.age))
                        RULE1()
                        child.is_pruned = True
                    else:
                        debug_message("RULE 3: Branch age:{0}, Child age:{1}".format(branch.age, child.age))
                        RULE3()
                        child.is_pruned = True
            else:
                warning_message("Child already pruned")

    elif branch.age >= 3:
        for child in branch.children:
            if child.is_pruned == False:
                if child.age == 1:
                    debug_message("RULE 4: Branch age:{0}, Child age:{1}".format(branch.age, child.age))
                    RULE4()
                    child.is_pruned = True
            else:
                warning_message("Child already pruned")

def RULE1():
    pass
    # info_message("Branch cut 5cm from the fork [RULE 1]")

def RULE2():
    pass
    # info_message("Branch is 1 year and connected to a leader [RULE 2]")

def RULE3():
    pass
    # info_message("SAME AS 4: Branch cut close to the fork [RULE 3]")

def RULE4():
    pass
    # info_message("SAME AS 3: Branch cut close to the fork [RULE 4]")


