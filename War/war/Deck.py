from Card import Card

class Deck:
    def __init__(self):
        print ("\n\t\t\t\t\t\t\t\t\t\t\t****************************************  START GAME ****************************************")
        print ("\nYou will be playing against the computer")

    def deal(self):
        #Initializ score
        player1score = 0
        player2score = 0
        war = 0

        round = 0

        #Create Deck
        cardDeck = Card()

        #Shuffle Deck
        cardDeck.shuffle()

        #Split Deck
        splitDeck = cardDeck.splitDeck()

        #Deal Cards
        self.Player1 = splitDeck[0]
        self.Player2 = splitDeck[1]


        for x in range(26, 0, -1):
            print ("\nThese are your cards: " + str(splitDeck[0]))
            round = round + 1
            print("\nROUND " + str(round))
            userCard = input("Please Draw A Card between 1 and " + str(len(self.Player1)) + " (eg: 1): ")
            value1 = " ".join(self.Player1[int(userCard)-1])
            value2 = " ".join(self.Player2[x-1])
            rank1 = value1[0]
            rank2 = value2[0]
            if value1[0] == 'A':
                rank1 = (value1[0].replace('A','14'))
            if value2[0] == 'A':
                rank2 = (value2[0].replace('A','14'))
            if value1[0] == 'J':
                rank1 = (value1[0].replace('J','11'))
            if value2[0] == 'J':
                rank2 = (value2[0].replace('J','11'))
            if value1[0] == 'Q':
                rank1 = (value1[0].replace('Q','12'))
            if value2[0] == 'Q':
                rank2 = (value2[0].replace('Q','12'))
            if value1[0] == 'K':
                rank1 = (value1[0].replace('K','13'))
            if value2[0] == 'K':
                rank2 = (value2[0].replace('K','13'))

            print ("\nYou Drew " + str(self.Player1[int(userCard) - 1]))
            print ("Computer Drew " + str(self.Player2[x-1]))

            #Compare the cards drawn
            if int(rank1) > int(rank2):
                print ("\nYou get all the cards!")
                print ("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                player1score = player1score + 1
            elif int(rank2) > int(rank1):
                print ("\nComputer gets all the cards!")
                print ("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                player2score = player2score + 1
            elif int(rank1) == int(rank2):
                print ("\nWAR!")
                print ("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                war = war + 1

        print ("\nYour Points: " + str(player1score))
        print ("Computer's Points: " + str(player2score))
        print ("WAR Count: " + str(war))

        if player1score > player2score:
            print ("\nCONGRATULATIONS YOU WON THE GAME!!!")
        elif player2score > player1score:
            print ("\nCOMPUTER WON THE GAME!")
        elif player2score == player1score:
            print ("\nIT'S A DRAW!")


d = Deck()
d.deal()




