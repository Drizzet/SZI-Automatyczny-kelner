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

def talk(talk, test_data, ind):
    notEnd = True
    ##print('\nDane testowe:')
    ##print(test_data)
    dtree = getTree(dataset)
    output = getDecision(dtree, test_data)
    order = output[0]
    pdfGen(dtree, dataset, ind)
    outputs = []
    while notEnd:
        dtree = getTree(dataset)
        outputP = getDecision(dtree, test_data)[0]
        if outputP in outputs:
            continue
        else:
            outputs.append(outputP)
            pdfGen(dtree, dataset, ind)
        x = getCustomerDecision(talk, outputs[-1], notEnd)
        talk = x[0]
        order = x[1]
        notEnd = x[2]
    return [talk, order, notEnd]

def getCustomerDecision(talk, output, notEnd):
    talk.append('KELNER: Moja propozycja to:')
    talk.append(dataset.target_names[output])
    answers = [0, 1, 2]
    odpowiedz = 1##random.choice(answers)
    order = output
    if odpowiedz == 0:
        talk.append('KLIENT: Czy mógłby Pan zaproponować mi coś innego?')
    else:
        talk.append('KLIENT: Może być - poproszę.')
        talk.append('')
        notEnd = False
    return [talk, order, notEnd]

def getDishName(i):
    return dataset.target_names[i]

def startConversation():
    talk = []
    talk.append('KELNER: Dzień dobry!')
    talk.append(('KLIENT: Dzień dobry. Chcę coś, co jest: '))
    return talk

def prepareTestData(talk):
    dishes = dataset.feature_names
    doNotChoose = []
    choices = []
    labels = []
    data = []
    indeks = 0
    ind = 0
    while indeks < len(dishes):
        indeks = indeks + 1
        data.append(5)
    i = 0
    while ind < 3:
        x = random.choice(dishes)
        if x not in doNotChoose:
            choices.append(x)
            labels.append(dishes.index(choices[ind]))
            if ind == 0:
                talk.append(choices[ind] + ',')
                i = len(talk) - 1
            else:
                talk[i] = talk[i] + ' ' + choices[ind] + ','
            data[labels[ind]] = 10
            ind = ind + 1
            xInd = dishes.index(x)
            doNotChoose.append(dishes[xInd])
    i = 0
    while ind < 6:
        x = random.choice(dishes)
        if x not in doNotChoose:
            choices.append(x)
            labels.append(dishes.index(choices[ind]))
            if ind == 3:
                talk.append('nie ' + choices[ind] + ',')
                i = len(talk) - 1
            else:
                talk[i] = talk[i] + ' nie ' + choices[ind] + ','
            data[labels[ind]] = 0
            ind = ind + 1
            xInd = dishes.index(x)
            doNotChoose.append(dishes[xInd])
    i = 0
    while ind < 9:
        x = random.choice(dishes)
        if x not in doNotChoose:
            choices.append(x)
            labels.append(dishes.index(choices[ind]))
            if ind == 6:
                talk.append('niezbyt ' + choices[ind] + ',')
                i = len(talk) - 1
            else:
                talk[i] = talk[i] + ' niezbyt ' + choices[ind] + ','
            data[labels[ind]] = 3
            ind = ind + 1
            xInd = dishes.index(x)
            doNotChoose.append(dishes[xInd])
    i = 0
    while ind < 12:
        x = random.choice(dishes)
        if x not in doNotChoose:
            choices.append(x)
            labels.append(dishes.index(choices[ind]))
            if ind == 9:
                talk.append('raczej ' + choices[ind] + ',')
                i = len(talk) - 1
            else:
                if ind < 11:
                    talk[i] = talk[i] + ' raczej ' + choices[ind] + ','
                else:
                    talk[i] = talk[i] + ' raczej ' + choices[ind] + '.'
            data[labels[ind]] = 7
            ind = ind + 1
            xInd = dishes.index(x)
            doNotChoose.append(dishes[xInd])
    i = 0
    test_data = [data]
    print(test_data)
    return test_data
