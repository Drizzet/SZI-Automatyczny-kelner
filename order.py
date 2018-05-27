from decisionTree import *
import random

class Order:
    def __init__(self, customer, order):
        self.customer = customer
        self.order = order

def customersList(customers: set):
    return list(customers)

def popCustomers(customers: list):
    return customers.pop()

def talk(talk, test_data):
    notEnd = True
    ##print('\nDane testowe:')
    ##print(test_data)
    output = getDish(test_data)
    order = output[0]
    outputs = []
    while notEnd:
        outputP = getDish(test_data)[0]
        if outputP in outputs:
            continue
        else:
            outputs.append(outputP)
        x = getCustomerDecision(talk, outputs[-1], notEnd)
        talk = x[0]
        order = x[1]
        notEnd = x[2]
    return [talk, order, notEnd]

def getCustomerDecision(talk, output, notEnd):
    talk.append('KELNER: Moja propozycja to:')
    talk.append(dataset.target_names[output])
    answers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    odpowiedz = 1 ##random.choice(answers)
    order = output
    if odpowiedz == 0:
        talk.append('KLIENT: Czy mógłby Pan zaproponować mi coś innego?')
    else:
        talk.append('KLIENT: Może być - poproszę.')
        talk.append('')
        notEnd = False
    return [talk, order, notEnd]

def getDish(test_data):
    dtree = getTree(dataset)
    output = getDecision(dtree, test_data)
    return output

def getDishName(i):
    return dataset.target_names[i]

def startConversation():
    talk = []
    talk.append('KELNER: Dzień dobry!')
    talk.append(('KLIENT: Dzień dobry. Chcę coś, co jest: '))
    return talk

def prepareTestData(talk):
    dishes = dataset.feature_names
    indeks = 0
    data = []
    while indeks < len(dishes):
        indeks = indeks + 1
        data.append(5)
    choices = [random.choice(dishes)]
    talk.append(choices[0])
    labels = [dishes.index(choices[0])]
    data[labels[0]] = 10
    ind = 1
    while ind < 3:
        x = random.choice(dishes)
        if x not in choices:
            choices.append(x)
            labels.append(dishes.index(choices[ind]))
            talk.append(choices[ind])
            data[labels[ind]] = 10
            ind = ind + 1
    test_data = [data]
    return test_data
