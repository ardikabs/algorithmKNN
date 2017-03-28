from operator import itemgetter
from dataIris import Data as dataFlower
import math
import random
import json
import sys
jenis_kelas = []

#Fungsi Membaca File Data
def readFile(file = None):
    dataset = []
    with open(file,'r') as ins:
        datalist = ins.read().splitlines()

        for i in range(len(datalist)):
            line = datalist[i]
            list = line.split(',')
            temp = dataFlower(i,list[0],list[1],list[2],list[3],list[4])
            dataset.append(temp)

            if list[4] not in jenis_kelas:
                jenis_kelas.append(list[4])

    return dataset

#Fungsi Memisahkan dataset berdasarkan kelas
def dataset_by_kelas(dataset = []):

    dataset_kelas = []

    for i in range(len(jenis_kelas)):
        temp = []
        for j in range(len(dataset)):
            if dataset[j].classification == jenis_kelas[i]:
                temp.append(dataset[j])
        dataset_kelas.append(temp)

    return dataset_kelas

#Fungsi menentukan data training dan sample
#Dengan metode holdout
def holdout(dataset = []):

    sample = []
    training = []
    dataset_kelas = dataset_by_kelas(dataset)

    for i in range(len(jenis_kelas)):
        for j in range(int(0.2* len(dataset_kelas[i]))):
            sample.append(dataset_kelas[i].pop())

    for i in range(len(jenis_kelas)):
        for j in range(len(dataset_kelas[i])):
            training.append(dataset_kelas[i][j])

    proses = nearest_neighbor(dataset, training,sample)

    return proses

def random_subsampling(dataset = [], eksperimen = 0):

    hasil = []
    for x in range(eksperimen):
        sample = []
        training = []
        datalength = len(dataset)

        for i in range(default_data):
            index = random.randint(0, datalength-1)
            sample.append(dataset[index])

        for i in range(datalength):
            if dataset[i] not in sample :
                training.append(dataset[i])

        proses = nearest_neighbor(dataset, training, sample)
        hasil.append(proses)

    return hasil

def kfold(dataset = [], eksperimen = 0):
    hasil = []
    divider = len(dataset) / eksperimen
    divider_by_eksperimen =[]
    if eksperimen == 1:
        print "Error cok"
    else :
        for x in range(eksperimen):
            sample = []
            training = []
            div = []

            for i in range(divider):
                if x == 0:
                    div.append(i)
                else :
                    firstnum = divider_by_eksperimen[x-1][1][-1] + 1
                    num = firstnum + i
                    div.append(num)
            info = x , div
            divider_by_eksperimen.append(info)

            first = divider_by_eksperimen[x][1][0]
            last = divider_by_eksperimen[x][1][-1] + 1

            for i in range(first,last):
                sample.append(dataset[i])

            for i in range(len(dataset)):
                if dataset[i] not in sample:
                    training.append(dataset[i])

            proses = nearest_neighbor(dataset, training, sample)
            hasil.append(proses)

    return hasil

def leaveoneout(dataset=[]):

    hasil = []
    datalength = len(dataset)

    for i in range(datalength):
        sample = []
        training = []
        sample.append(dataset[i])

        for j in range(len(dataset)):
            training.append(dataset[j])

        del training[i]

        proses = nearest_neighbor(dataset, training, sample)
        hasil.append(proses)

    return hasil

def bootstrap(dataset = [], eksperimen  = []):
    hasil = []
    datasetlength = len(dataset)

    for x in range(eksperimen):
        sample = []
        training = []
        for i in range(datasetlength):
            index = random.randint(0,datasetlength-1)
            training.append(dataset[index])

        for i in range(datasetlength):
            if dataset[i] not in training:
                sample.append(dataset[i])

        proses = nearest_neighbor(dataset, training, sample)
        hasil.append(proses)
    return hasil

#Fungsi Algoritma Nearest Neighbor
def nearest_neighbor(dataset = [],training = [], sample = []):

    result_knn = {"Result_KNN":[]}
    rank = {"Rank": []}

    sample_length = len(sample)
    training_length = len(training)
    for i in range(sample_length) :

        proses_knn = {"id-sample":  sample[i].index, "result" : []}
        proses_rank = {"id-sample" :  sample[i].index, "result": []}

        result_knn["Result_KNN"].append(proses_knn)
        rank["Rank"].append(proses_rank)

        temp_jarak = []
        for j in range(training_length):
            res = sample[i].distance(training[j])
            data = {"id-training" : training[j].index, "Jarak" : res,"Dataset" : (training[j].a,training[j].b,training[j].c, training[j].d, training[j].classification) ,"Sample ": (sample[i].a, sample[i].b, sample[i].c, sample[i].d)}
            result_knn['Result_KNN'][i]['result'].append(data)

            #mengambil index dataset_training yang didapat, dan hasil penghitungan jarak_id
            #lalu mengassign data tersebut ke temp_jarak
            jarak_id = result_knn['Result_KNN'][i]['result'][j]['id-training']
            jarak_hasil = result_knn['Result_KNN'][i]['result'][j]['Jarak']
            data_jarak = jarak_id,jarak_hasil
            temp_jarak.append(data_jarak)

        #ketika temp_jarak tidak kosong, maka tiap ranking berdasarkan index akan menerima hasil dari temp_jarak
        if temp_jarak :
            temp_jarak.sort(key=itemgetter(1))
            rank['Rank'][i]['result'].append(temp_jarak[0:k])

    hasil_voting = get_result_by_voting(dataset, rank, sample_length)

    valid = 0
    error = 0

    for i in range(len(sample)):
        # print ""
        # print "Sample {0} : {1}".format(sample[i].index,(sample[i].a , sample[i].b,sample[i].c , sample[i].d))
        # for j in range(k):
        #     print "{0}. Dataset Index : {1}, Jarak : {2} ".format(j+1,rank['Rank'][i]['result'][0][j][0],rank['Rank'][i]['result'][0][j][1])
        # print "____________________________________________________"
        # print "Algoritma KNN\t\t-> Sample termasuk class {}".format(hasil_voting[i][0][0])
        # print "Data Training\t\t-> Sample termasuk class {}\n".format(sample[i].classification)

        if hasil_voting[i][0][0] != sample[i].classification:
            error = error + 1
        else:
            valid = valid + 1

    # print("Conclusion")
    # print "Jumlah data valid : {0}".format(valid)
    prosentase = float(valid)/float(len(sample)) * 100
    prosentase = round(prosentase, 1)
    # print "Maka dengan k = {0} didapatkan prosentase benar sebesar {1}%".format(k, prosentase)
    return prosentase

#Fungsi untuk melakukan voting data sample
def get_result_by_voting(dataset = [], result_ranking=[], length=0):
    classWin = []

    for i in range(length):
        hasil_vote = []
        res = []
        accumulation = [0] * len(jenis_kelas)
        for j in range(k):
            identifier = result_ranking['Rank'][i]['result'][0][j][0]
            res = vote(dataset[identifier].classification, accumulation)

        for j in range(len(jenis_kelas)):
            item = jenis_kelas[j], res[j]
            hasil_vote.append(item)

        hasil_vote.sort(key=itemgetter(1),reverse=True)
        classWin.append(hasil_vote)

    return classWin

#Fungsi menghitung kelas yg dominan
def vote(selection, accumulation):

    for i in range(len(jenis_kelas)):
        if selection == jenis_kelas[i]:
            accumulation[i] = accumulation[i] + 1

    return accumulation


if __name__ == "__main__" :
    file = "iris.data"
    dataset = readFile(file)
    default_data = 15
    k = 5
    eksperimen = 5
    hasil_ho = holdout(dataset)
    hasil_rs = random_subsampling(dataset, eksperimen)
    hasil_kf = kfold(dataset, eksperimen)
    hasil_loo = leaveoneout(dataset)
    hasil_bs = bootstrap(dataset,eksperimen)

    orig_stdout = sys.stdout
    nama_file = "{}NN-output-{}.txt".format(k,eksperimen)
    f = open(nama_file,'w')
    sys.stdout = f
    print "ALGORITMA KNN (VALIDATION MODEL)"
    print " "
    print "Validation Model : Holdout"
    print "K = {}".format(k)
    print "LIST PROSENTASE BENAR"
    prosentase = hasil_ho
    prosentase = round(prosentase,1)
    print "Prosentase  : {} %".format(prosentase)

    print " "

    print "Validation Model : Random Subsampling"
    print "K = {}".format(k)
    print "Jumlah eksperimen  = {}".format(eksperimen)
    print "LIST PROSENTASE BENAR"
    for i in range(len(hasil_rs)):
        print "{0}. Eksperimen {0} : {1}%".format(i+1, hasil_rs[i])
    prosentase = sum(hasil_rs)/eksperimen
    prosentase = round(prosentase,1)
    print "Prosentase  : {} %".format(prosentase)

    print " "

    print "Validation Model : K-Fold"
    print "K = {}".format(k)
    print "Jumlah eksperimen  = {}".format(eksperimen)
    print "LIST PROSENTASE BENAR"
    for i in range(len(hasil_kf)):
        print "{0}. Eksperimen {0} : {1}%".format(i+1, hasil_kf[i])
    prosentase = sum(hasil_kf)/eksperimen
    prosentase = round(prosentase,1)
    print "Prosentase  : {} %".format(prosentase)

    print " "

    print "Validation Model : Leave-One-Out Cross"
    print "K = {}".format(k)
    print "Jumlah eksperimen  = {}".format(len(dataset))
    print "LIST PROSENTASE BENAR"
    for i in range(len(hasil_loo)):
        print "{0}. Eksperimen {0} : {1}%".format(i+1, hasil_loo[i])
    prosentase = sum(hasil_loo)/len(dataset)
    prosentase = round(prosentase,1)
    print "Prosentase  : {} %".format(prosentase)

    print " "

    print "Validation Model : Bootstrap"
    print "K = {}".format(k)
    print "Jumlah eksperimen  = {}".format(eksperimen)
    print "LIST PROSENTASE BENAR"
    for i in range(len(hasil_bs)):
        print "{0}. Eksperimen {0} : {1}%".format(i+1, hasil_bs[i])
    prosentase = sum(hasil_bs)/eksperimen
    prosentase = round(prosentase,1)
    print "Prosentase  : {} %".format(prosentase)



    sys.stdout = orig_stdout
    f.close
