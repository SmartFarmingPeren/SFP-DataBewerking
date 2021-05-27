from Branch import Branch
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
    # if branch.age >= 3:
    print(branch.children[0].age)



    # if branch.age == 1:
    #     if branch.parent.is_leader == True:
    #         pass


