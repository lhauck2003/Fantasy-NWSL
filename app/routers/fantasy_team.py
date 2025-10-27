## Holds the Code for getting a fantasy team information and gives th user ability to sub,
## transfer, or view their team for the week 
from players import Players as P

class Fantasy_Team(list):
    def __init__(self):
        team: list[P] = ["debinha","aitana"]

    def display(self):
        for player in self.team:
            player.display()

    def edit(self, player_in, player_out):
        pass

class Transfer_Team(Fantasy_Team):
    def __init__(self):
        pass

    def display(self):
        pass

    def edit(self, player_in: P, player_out: P):
        pass

class Sub_Team(Fantasy_Team):
    def __init__(self):
        pass

    def display(self):
        pass

    def edit(self, player_in: P, player_out: P):
        pass


def main():
    team: Fantasy_Team = Fantasy_Team()

    while(True):
        try:
            type: int = int(input(f"View(0)\nSub(1)\nTransfer(2)\n"))
            assert type >=0 and type <=2, f"Incorrect Choice, please try again"
            if(type==0):
                team.display()
                continue
            elif(type==1):
                team = Sub_Team()
            elif(type==2):
                team = Transfer_Team()
            else:
                continue

            team.display()

            player_in = input("player in name: ")
            player_out = input("player out name: ")

            team.edit(player_in, player_out)
        except EOFError:
            break
        except Exception as e:
            print("***", e)

if __name__ == "__main__":
    main()