import Cards
import time

deck = Cards.Deck()
deck.shuffle()


def draw(hand):
    card = deck.draw_cards(hand, 1)
    return card

def print_hand(hand, print_score = True):
    if not print_score:
        print(hand.label + ": " + str(hand))
    else: print(hand.label + ": " + str(hand) + ": " + str(hand.score()))

def hit_or_stand():
    while True:  # Loop until the player picks a valid input.
        choice = raw_input("""\n'h'it or 's'tand?\n -->""")
        if(choice.lower() == 'hit' or choice.lower() == 'h'):
            # Hit
            return True
        elif(choice.lower() == 'stand' or choice.lower() == 's'):
            # Stand
            return False
        else:
            # Invalid input
            print("Invalid input, please try again.")


if __name__ == '__main__':
    print("Welcome to Black Jack! The deck reshuffles every round. To quit, Press Ctrl+C anytime to quit.")
    player_points = 0
    dealer_points = 0
    try:
        while True:
            # Reshuffle deck.
            deck = Cards.Deck()
            deck.shuffle()
            # Print score.
            print("\n\nPlayer: {}, Dealer: {}".format(player_points, dealer_points))

            # Initial card draws.
            player = Cards.Hand("Player")
            draw(player)
            draw(player)
            dealer = Cards.Hand("Dealer")
            draw(dealer)
            hole_card = draw(dealer)  # Dealer's face down card.
            hole_card.face_down = True

            print_hand(dealer)
            print_hand(player)

            while True:
                # Player's turn, goes until bust or stand.
                hit = hit_or_stand()
                if hit:
                    draw(player)
                    print_hand(dealer)
                    print_hand(player)

                    if player.score() > 21:
                        break
                    
                    continue
                else:
                    break

            if player.score() > 21:
                print("--Busted! You lost!--")
                dealer_points += 1
            else:
                # Dealer's turn, draw until >16 points or bust.
                hole_card.face_down = False
                while dealer.score() < 17:
                    draw(dealer)
                print_hand(dealer)
                print_hand(player)
                if(dealer.score() > 21):
                    print("-Dealer Busted! You won!--")
                    player_points += 1
                elif(dealer.score() > player.score()):
                    print("--You lost!--")
                    dealer_points += 1
                elif(dealer.score() < player.score()):
                    print("--You won!--")
                    player_points += 1
                else:
                    print("--Push!--")
            time.sleep(1)  # Small wait before starting a new round.

    except KeyboardInterrupt:
        print("Game over! Final scores:")
        print("Player: {}, Dealer: {}".format(player_points, dealer_points))
            

        
            

