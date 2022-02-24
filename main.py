# DO NOT DELETE THESE LINES
###########################################################

    #  Computer Project #10
    #
    #  Initalize deck of cards and shuffle it
    #   fix kings and put them to left of stack pile
    #   get option function
    #       take user input and split it
    #       if length isnt equal to 1 or 3 report error
    #       else: check if its equal to allowed input if it is return user input if its not return error/None
    #    valid_tableau_to_tableau function
    #       checks if the movement from user is possible in tableau
    #       returns false otherwise
    #    valid_tableau_to_foundation function
    #       checks if the movement from user is possible to foundation
    #       returns false if not
    #    move_tableau_to_tableau
    #         moves data to specified place in tableau
    #   move_tableau_to_tableau
    #         moves data to specified place in tableau
    #   def undo function
    #        undoes last opertation user specified
    #   check for win
    #      loops through foundation to see if there is enough card to win
    #      if not enough cards returns false
    #   display
    #       displays foundation and tabeau everytime its called
    #    loop through main until Q is entered reprompting user for input

    ###########################################################
import cards, random

random.seed(100)  # random number generator will always generate
# the same 'random' number (needed to replicate tests)

MENU = '''     
Input options:
    MTT s d: Move card from end of Tableau pile s to end of pile d.
    MTF s d: Move card from end of Tableau pile s to Foundation d.
    U: Undo the last valid move.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''


def fix_kings(tableau):
    ''' This function sorts kings into piles with the kings being on the most left of each pile
    takes in tableau a list of 18 piles and returns None'''
    count = -1
    for i in tableau:
        count = count + 1
        ranks = []
        pile = i.copy()
        for x in i:
            ranks.append(x.rank())
        if ranks.count(13) == 1:
            if ranks[1] == 13:
                i.insert(0, i[1])
                i.pop(2)
            if ranks[2] == 13:
                i.insert(0, i[2])
                i.pop(3)
        if ranks.count(13) == 2:
            if ranks[0] != 13:
                i.append(i[0])
                i.pop(0)
            elif ranks[1] != 13:
                i.append(i[1])
                i.pop(1)
        tableau[count] = i


def initialize():
    ''' This function initializes the deck than shuffles it returns tableau and foundation as a tuple'''
    tableau = []
    deck = cards.Deck()
    deck.shuffle()
    foundation = [[], [], [], []]
    if deck == None: # if deck is none returns blank
        return (tableau, foundation)
    for i in range(17): # loops through first 17 list
        card_pile = list()
        for x in range(3):# adds three cards to each pile
            card_pile.append(deck.deal())
        tableau.append(card_pile)

    tableau.append([deck.deal()])
    fix_kings(tableau)
    lol = (tableau, foundation)
    return lol



def get_option():
    ''' This function takes user input and checks to see if usr input is valid or not returns user input as a tuple  '''
    usr_inp = input("\nInput an option (MTT,MTF,U,R,H,Q): ")
    options = usr_inp.split() # splits usr input
    if len(options) == 3: # checks to see if usr input is 3 inputs
        if options[0].upper() == 'MTT' or options[0].upper() == 'MTF': # checks to see if the first part of user input is correct
            return [options[0], int(options[1]), int(options[2])]
        else:
            print("Error in option: {}".format(usr_inp))
            return None
    elif len(options) == 1:
        if options[0].upper() in ['U', 'R', 'H', 'Q']:
            return [options[0]]
        else:
            print("Error in option: {}".format(usr_inp))
            return None
    else: # prints error if usr input isnt 1-3 inputs long
        print("Error in option: {}".format(usr_inp))
        return None


def valid_tableau_to_tableau(tableau, s, d):
    ''' This function takes tablea and sees if the wanted move is valid or not returns True if it is valid and False if it's not '''
    try:
        if tableau[s][-1].rank() == ((tableau[d][-1].rank()) + 1) or ((tableau[d][-1].rank() - 1)): # checks to see if cards wanted to move are in range of each other by one
            if len(tableau[d]) < 3:# checks to see if pile has enough room to add it too
                return True
            else:
                return False
        else:
            return False
    except:
        return False


def valid_tableau_to_foundation(tableau, foundation, s, d):
    ''' This function takes user input and see if the move wanted to make to the foundation is valid or not returns True and False'''
    try:
        if foundation[d] == []:
            if tableau[s][-1].rank() != 1: # checks to see if foundation is empty or not
                return False
            else:
                return True
        if tableau[s][-1].suit() == foundation[d][-1].suit(): # checks to see if cards are the same suit
            if foundation[d][-1].rank()  == (tableau[s][-1].rank() - 1): # checks to see if cards are in range of each other
                return True
            else:
                return False
        else:
            return False
    except:
        return False


def move_tableau_to_tableau(tableau, s, d):
    ''' This function checks if input from user is valid if it is than it moves card to specified tableau '''
    if valid_tableau_to_tableau(tableau,s,d) == False:
        return False
    else:
        card = tableau[s].pop()
        tableau[d].append(card)
        return True


def move_tableau_to_foundation(tableau, foundation, s, d):
    ''' This function checks if input from user is valid if it is than it moves card to specified foundation '''
    if valid_tableau_to_foundation(tableau,foundation,s,d) == True:
        card = tableau[s].pop()
        foundation[d].append(card)
        return True
    else:

        return False

def check_for_win(foundation):
    ''' This function cyles through foundations to see if last card is a king if all last cards are kings returnss true as a win else False '''
    win = True
    for i in foundation:
        if i != []:
            if i[-1].rank() != 13:
                win = False
        else:
            win = False
    if win == False:
        return False
    else:
        return True


def undo(moves, tableau, foundation):
    '''
    Undo the last move;
       Parameters:
           moves: the history of all valid moves. It is a list of tuples
                  (option,source,dest) for each valid move performed since the
                  start of the game.
           tableau: the data structure representing the tableau.
       Returns: Bool (True if there are moves to undo. False if not)
    '''

    if moves:  # there exist moves to undo
        last_move = moves.pop()
        option = last_move[0]
        source = last_move[1]
        dest = last_move[2]
        print("Undo:", option, source, dest)
        if option == 'MTT':
            tableau[source].append(tableau[dest].pop())
        else:  # option == 'MTF'
            tableau[source].append(foundation[dest].pop())
        return True
    else:
        return False


def display(tableau, foundation):
    '''Display the foundation in one row;
       Display the tableau in 3 rows of 5 followed by one row of 3.
       Each tableau item is a 3-card pile separated with a vertical bar.'''
    print("\nFoundation:")
    print(" " * 15, end='')  # shift foundation toward center
    # display foundation with labels
    for i, L in enumerate(foundation):
        if len(L) == 0:
            print("{:d}:    ".format(i), end="  ")  # padding for empty foundation slot
        else:
            print("{:d}: {} ".format(i, L[-1]), end="  ")  # display only "top" card
    print()
    print("=" * 80)
    print("Tableau:")
    # First fifteen 3-card piles are printed; across 3 rows
    for i in range(15):
        print("{:2d}:".format(i), end='')  # label each 3-card pile
        for c in tableau[i]:  # print 3-card pile (list)
            print(c, end=" ")
        print("    " * (3 - len(tableau[i])), end='')  # pad with spaces
        print("|", end="")
        if i % 5 == 4:  # start a new line after printing five lists
            print()
            print("-" * 80)
    # Final row of only three 3-card piles is printed
    print(" " * 15 + "|", end='')  # shift first pile right
    for i in range(15, 18):
        print("{:2d}:".format(i), end='')  # label each 3-card pile
        for c in tableau[i]:
            print(c, end=" ")
        print("    " * (3 - len(tableau[i])), end='')  # pad with spaces
        print("|", end="")
    print()
    print("-" * 80)


def main():
    '''Loops through data until Usr input is Q for quit than it quits'''
    print('\nWelcome to Shamrocks Solitaire.\n')
    (tableau, foundation) = initialize()
    display(tableau, foundation)
    print(MENU)
    options = True
    moves = list()
    while options != 'Q':
        options = get_option()

        while options == None:
            options = get_option()
        if options[0].upper() == 'Q':
            break
        if options[0].upper() == 'MTT':
            if move_tableau_to_tableau(tableau,options[1],options[2]) == True:
                display(tableau,foundation)
                move = ('MTT', options[1], options[2])
                moves.append(move)
            else:
                if options[1] >= 18:
                    print('Error in Source.')
                elif options[2] >= 18:
                    print('Error in Destination.')
                else:
                    print('Error in move: {}'.format(' , '.join(str(i).upper() for i in options)))
        if options[0].upper() == 'MTF':
            if move_tableau_to_foundation(tableau,foundation,options[1],options[2]) == False:
                if options[1] >= 18:
                    print('Error in Source.')
                elif options[2] >= 4:
                    print('Error in Destination.')
                else:
                    print('Error in move: {}'.format(' , '.join(str(i).upper() for i in options)))
            else:
                if check_for_win(foundation) == False:
                    move = ('MTF', options[1], options[2])
                    moves.append(move)
                    display(tableau,foundation)
                else:
                    print('You won!')
                    display(tableau,foundation)
                    print("\n- - - - New Game. - - - -")
                    (tableau,foundation) = initialize()
                    display(tableau,foundation)
                    print(MENU)
        if options[0].upper() == 'U':
            if len(moves) == 0:
                print('No Moves to undo.')
            else:
                undo(moves, tableau, foundation)
                display(tableau,foundation)
        if options[0].upper() == 'R':
            (tableau, foundation) = initialize()
            display(tableau, foundation)
            moves = list()
        if options[0].upper() == 'H':
            print(MENU)
    print('Thank you for playing.')



if __name__ == '__main__':
    main()