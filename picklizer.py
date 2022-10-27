# Code attributed from https://github.com/gkeng/Listening-to-Chaotic-Whishpers--Code
import pickle
article_firm_folder='/Users/admin/Dropbox/School work/SJTU/AIProject/AI_Project/firm_csv_folder/'
folder = '/Users/admin/Dropbox/School work/SJTU/AIProject/AI_Project/'
article_firm_pickle= folder + 'pickle_article/'
import csv
import os


def picklizer():

    #fname = 'Comcast.csv'
    for fname in os.listdir(article_firm_folder):
        if fname[-4:] == '.csv':
            print(fname)
            file_path = os.path.join(article_firm_folder, fname)
            f = open(file_path, 'r')
            lines = f.readlines()
            f.close()
            dic = {}
            for line in lines:
                line = line.replace('\n', '').split(',')
                dic[line[0]] = line[1:]

            #print(article_firm_pickle + fname+'.pkl')
            with open(article_firm_pickle + fname+'.pkl','wb+') as pick:
                pickle.dump(dic, pick, protocol=pickle.HIGHEST_PROTOCOL)
                #print(dic)


if __name__ == '__main__':
    picklizer()
