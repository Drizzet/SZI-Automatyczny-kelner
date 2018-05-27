from sklearn import tree
from sklearn.externals.six import StringIO
import pydotplus

class DataSet:
    def __init__(self, target, data, feature_names, target_names, labels):
        self.target = target
        self.data = data
        self.feature_names = feature_names
        self.target_names = target_names
        self.labels = labels

def num_or_str(x):
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return str(x).strip()

def parse_csv(input, delim=';'):
    lines = [line for line in input.splitlines() if line.strip()]
    return [list(map(num_or_str, line.split(delim))) for line in lines]

def prepareDataSet(csv, label):
    target = [] ## symbole dań z dishes.csv
    data = [] ### wartości przy daniach z dishes.csv
    feature_names = [] ### nazwy wartości data
    target_names = [] ### nazwy dań z labels.csv
    labels = [] ### symbole dań z labels.csv
    i = 0
    for x in csv:
        if i != 0:
            target.append(x[-1])
            data.append(x[:-1])
        else:
            ys = []
            for y in x[:-1]:
                if "\ufeff" in y:
                    y = y.replace('\ufeff', '')
                ys.append(y)
            feature_names = ys
        i = i + 1
    i = 0
    for x in label:
        if i != 0:
            target_names.append(x[1])
            labels.append(x[0])
        i = i + 1
    '''print('\nCele (jako etykiety liczbowe dań):')
    print(target)
    print('\nDane uczące:')
    print(data)
    print('\nNazwy atrybutów:')
    print(feature_names)
    print('\nDania:')
    print(target_names)
    print('\nEtykiety dań:')
    print(labels)'''
    return DataSet(target, data, feature_names, target_names, labels)

def getTree(dataset):
    train_target = dataset.target
    train_data = dataset.data
    dtree = tree.DecisionTreeClassifier(criterion='entropy')
    dtree.fit(train_data, train_target)
    return dtree

def getDecision(dtree, test_data):
    return dtree.predict(test_data)

def pdfGen(dtree, dataset):
    dot_data = StringIO()
    tree.export_graphviz(
        decision_tree=dtree,
        out_file=dot_data,
        feature_names=dataset.feature_names,
        class_names=dataset.target_names,
        filled=True,
        rounded=True,
        impurity=True
    )
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_pdf('tree.pdf')
    print('\nDrzewo w PDF-ie!')

csv = parse_csv(open('data/dishes.csv', 'r', encoding='utf-8').read())
labels = parse_csv(open('data/labels.csv', 'r', encoding='utf-8').read())
dataset = prepareDataSet(csv, labels)

## test_data = [[10, 10, 4, 4, 4, 4, 4, 4, 10, 10, 0, 10]]

