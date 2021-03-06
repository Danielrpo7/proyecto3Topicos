import operator, os, sys
import time
import numpy as np
import matplotlib.pyplot as plt
#import pylab as plt
from mpi4py import MPI
from math import*

comm = MPI.COMM_WORLD
sendbuf = []
root = 0
plt.ion()

stopwordsman = ["a", "able", "about", "above", "according", "accordingly", "across", "actually", "after", "afterwards",
                "again", "against", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although",
                "always", "am", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone",
                "anything", "anyway", "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate", "are",
                "around", "as", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "b", "be",
                "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
                "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but",
                "by", "c", "came", "can", "cannot", "cant", "cause", "causes", "certain", "certainly", "changes",
                "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider", "considering",
                "contain", "containing", "contains", "corresponding", "could", "course", "currently", "d", "definitely",
                "described", "despite", "did", "different", "do", "does", "doing", "done", "down", "downwards",
                "during", "e", "each", "edu", "eg", "eight", "either", "else", "elsewhere", "enough", "entirely",
                "especially", "et", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere",
                "ex", "exactly", "example", "except", "f", "far", "few", "fifth", "first", "five", "followed",
                "following", "follows", "for", "former", "formerly", "forth", "four", "from", "further", "furthermore",
                "g", "get", "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten",
                "greetings", "h", "had", "happens", "hardly", "has", "have", "having", "he", "hello", "help", "hence",
                "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself",
                "his", "hither", "hopefully", "how", "howbeit", "however", "i", "ie", "if", "ignored", "immediate",
                "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "insofar", "instead",
                "into", "inward", "is", "it", "its", "itself", "j", "just", "k", "keep", "keeps", "kept", "know",
                "knows", "known", "l", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let",
                "like", "liked", "likely", "little", "ll", "look", "looking", "looks", "ltd", "m", "mainly", "many",
                "may", "maybe", "me", "mean", "meanwhile", "merely", "might", "more", "moreover", "most", "mostly",
                "much", "must", "my", "myself", "n", "name", "namely", "nd", "near", "nearly", "necessary", "need",
                "needs", "neither", "never", "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none",
                "noone", "nor", "normally", "not", "nothing", "novel", "now", "nowhere", "o", "obviously", "of", "off",
                "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "or", "other",
                "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "own",
                "p", "particular", "particularly", "per", "perhaps", "placed", "please", "plus", "possible",
                "presumably", "probably", "provides", "q", "que", "quite", "qv", "r", "rather", "rd", "re", "really",
                "reasonably", "regarding", "regardless", "regards", "relatively", "respectively", "right", "s", "said",
                "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed",
                "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven",
                "several", "shall", "she", "should", "since", "six", "so", "some", "somebody", "somehow", "someone",
                "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify",
                "specifying", "still", "sub", "such", "sup", "sure", "t", "take", "taken", "tell", "tends", "th",
                "than", "thank", "thanks", "thanx", "that", "thats", "the", "their", "theirs", "them", "themselves",
                "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "theres", "thereupon",
                "these", "they", "think", "third", "this", "thorough", "thoroughly", "those", "though", "three",
                "through", "throughout", "thru", "thus", "to", "together", "too", "took", "toward", "towards", "tried",
                "tries", "truly", "try", "trying", "twice", "two", "u", "un", "under", "unfortunately", "unless",
                "unlikely", "until", "unto", "up", "upon", "us", "use", "used", "useful", "uses", "using", "usually",
                "uucp", "v", "value", "various", "ve", "very", "via", "viz", "vs", "w", "want", "wants", "was", "way",
                "we", "welcome", "well", "went", "were", "what", "whatever", "when", "whence", "whenever", "where",
                "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while",
                "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish", "with",
                "within", "without", "wonder", "would", "would", "x", "y", "yes", "yet", "you", "your", "yours",
                "yourself", "yourselves", "z", "zero"]

def getT(rootDir):
    T = []
    fileList = []
    if comm.rank == 0:
        fileList = list(os.walk(rootDir))[0][2]
    v = comm.bcast(fileList, root)
    leidos = []
    finalwords = {}
    toSend = []
    for i in range(comm.rank, len(v), comm.size):
        # print("RANK: ", comm.rank, v[i])
        file = open(rootDir + v[i], 'r')
        mainwords = {}
        for line in file:

            for word in line.split():
                word = word.strip().lower().replace(",", "").replace(":", "").replace(";", "").replace("-", "").replace(
                    ".", "").replace("\"", "").replace("]", "").replace("[", "").replace(")", "").replace("(", "")
                if word not in stopwordsman:
                    if word in mainwords and word != '':
                        mainwords[word] += 1
                    else:
                        mainwords[word] = 1
        file.close()
        sorted_mainwords = sorted(mainwords.items(), key=operator.itemgetter(1))[::-1]

        for i in range(10):
            toSend.append(sorted_mainwords[i][0])

    recibV = comm.gather(toSend, root)
    tFinal = []
    if comm.rank == 0:
        for i in range(len(recibV)):
            tFinal.extend([element for element in recibV[i] if element not in tFinal])
    return tFinal, v

def ft(tFinal):
    frecuencia = {}
    for i in range(comm.rank, len(v), comm.size):
        result = []
        for j in range(len(w)):
            result.append(0)

        file = open(rootDir + v[i], 'r')
        for line in file:

            for word in line.split():
                word = word.strip().lower().replace(",", "").replace(":", "").replace(";", "").replace("-", "").replace(
                    ".", "").replace("\"", "").replace("]", "").replace("[", "").replace(")", "").replace("(", "")
                if word in w:
                    result[w.index(word)] += 1

        frecuencia[v[i]] = result

    recibFrecuencia = comm.gather(frecuencia, root)
    return recibFrecuencia

def preJaccard(recibFrecuencia):
    mapaFinal = {}
    if (comm.rank == 0):

        for i in range(len(recibFrecuencia)):
            mapaFinal.update(recibFrecuencia[i])

    x = comm.bcast(mapaFinal, root)

    tam = len(x)
    matrixC = np.zeros((tam, tam))
    listaFiles = list(x.keys())
    for i in range(comm.rank, len(x), comm.size):
        for j in range(tam):
            matrixC[i][j] = 1.0 - (jaccard_similarity(x[listaFiles[i]], x[listaFiles[j]]))
    recibMatrixC = comm.gather(matrixC, root)
    return recibMatrixC, x

def show(X, C, centroids, keep = False):
    import time
    time.sleep(0.5)
    plt.cla()
    plt.plot(X[C == 0, 0], X[C == 0, 1], '*b',
         X[C == 1, 0], X[C == 1, 1], '*r',
         X[C == 2, 0], X[C == 2, 1], '*g')
    plt.plot(centroids[:,0],centroids[:,1],'*m',markersize=20)
    plt.draw()
    if keep :
        plt.ioff()
        plt.show()

def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)

def KMeans(X, K, maxIters, plot_progress=None):
    C = []
    centroids = []
    matrizFinal = 0
    if comm.rank == 0:
        for matrix in recibMatrixC:
            matrizFinal += matrix
        centroids = matrizFinal[np.random.choice(np.arange(len(matrizFinal)), k), :]

    for i in range(maxIters):
        mJack = comm.bcast(matrizFinal, root)
        cent = comm.bcast(centroids, root)
        tam2 = len(mJack)
        argminList = np.zeros(tam2)

        for i in range(comm.rank, len(mJack), comm.size):
            dotList = []
            for y_k in cent:
                dotList.append(np.dot(mJack[i] - y_k, mJack[i] - y_k))
            argminList[i] = np.argmin(dotList)
        recibC = comm.gather(argminList, root)
        cFinal = []
        if comm.rank == 0:
            cFinal = np.zeros(len(recibC[0]))
            for li in range(len(recibC)):
                cFinal += recibC[li]

        z = comm.bcast(cFinal, root)

        centroidesTemp = []
        for i in range(k):
            centroidesTemp.insert(i, [])

        for i in range(comm.rank, k, comm.size):
            truefalseArr = z == i
            propiosKArr = mJack[truefalseArr]
            promedioArr = propiosKArr.mean(axis=0)
            centroidesTemp[i] = list(promedioArr)

        recibZ = comm.gather(centroidesTemp, root)
        centroidesFinales = []
        for j in range(k):
            centroidesFinales.append([])
        if comm.rank == 0:
            for i in range(len(recibZ)):
                for j in range(len(recibZ[i])):
                    centroidesFinales[j] += recibZ[i][j]
            centroids = centroidesFinales
    return np.array(centroids), C, z

def result(x,k):
    if comm.rank == 0:
        print("Tiempo final: ", time.time() - timeini)
        listaFiles = list(x.keys())
        cluster=[[]for _ in range(k)]
        for i in range(len(listaFiles)):
            for y in range(k):
                if z[i] == y:
                    cluster[y].append(listaFiles[i])


        for xy in range(k):
            print 'Cluster ', xy, ': ', cluster[xy]
            print '-----------------------'
        # show(recibMatrixC, finalList, centroides, True)


if __name__ == '__main__':
    timeini = time.time()
    k = 2
    maxIters = 5
    rootDir = sys.argv[1]
    #corte
    tFinal, v = getT(rootDir)
    w = comm.bcast(tFinal, root)
    #corteft
    recibFrecuencia=ft(tFinal)
    #corteprej
    recibMatrixC, x = preJaccard(recibFrecuencia)
    centroides, finalList, z = KMeans(recibMatrixC , k, maxIters)

    result(x, k)





