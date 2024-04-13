def ai(totalMana, handSize, hand=[], currentSelection=[]):
    # Base case: If totalMana or handSize is 0, return the currentSelection
    if totalMana == 0 or handSize == 0:
        return currentSelection
    
    # If the last card in the hand has the same value as totalMana,
    # add it to the currentSelection and return the updated currentSelection
    if hand[handSize - 1] == totalMana:
        currentSelection.append(hand[handSize - 1])
        return currentSelection
        
    # If the last card in the hand is greater than totalMana,
    # recursively call the ai function with handSize - 1
    elif hand[handSize - 1] > totalMana:
        return ai(totalMana, handSize - 1, hand, currentSelection)
    
    # If the last card in the hand is less than totalMana,
    # add it to the currentSelection and recursively call the ai function
    # with totalMana - hand[handSize - 1] and handSize - 1
    else:
        currentSelection.append(hand[handSize - 1])
        return ai(totalMana - hand[handSize - 1], handSize - 1, hand, currentSelection)
        
hand = [1, 2, 3, 4, 5]
totalMana = 7
handSize = len(hand)
playedHand = list()

# Call the ai function with the given parameters
ai(totalMana, handSize, hand, playedHand)

print(playedHand)