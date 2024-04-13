def ai (totalMana, handSize, hand = [], currentSelection = []):
    
    if totalMana == 0 or handSize == 0:
        return 0
    
    if hand[handSize - 1] == totalMana:
        currentSelection.append(hand[handSize - 1])
        print(currentSelection[0])
        return currentSelection
        
        
    if hand[handSize - 1] > totalMana:
        return ai(totalMana, handSize - 1,hand, currentSelection)
    else:
        currentSelection.append(hand[handSize - 1])
        return ai(totalMana - hand[handSize - 1], handSize - 1, hand, currentSelection)
        
hand = [1,2,3,4,5]
totalMana = 7
handSize = len(hand)
playedHand = list()

ai(totalMana, handSize, hand, playedHand)

print(playedHand)