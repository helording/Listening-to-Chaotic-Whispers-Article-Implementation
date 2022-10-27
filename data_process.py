import csv
import pandas as pd
import os
import numpy as np
import multiprocessing as mp


def create_csv_firm(spnas):

    firm_name = str(spnas[1])
    company_csv = firm_csv_folder + firm_name + ".csv"
    csv_stock = open(company_csv, 'w+')
    writer = csv.writer(csv_stock, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    for day in os.listdir(dirname):
        day_path = os.path.join(dirname, day + '/wsj/')
        if os.path.isdir(day_path):
            non_empty_day = False
            row = "%s" % (day[:4])
            for fname in os.listdir(day_path) :
                if firm_name in fname or firm_name.upper() in fname:
                    non_empty_day = True
                    row += "%s%s" % (',', fname[:-4])

                else :
                    f_path=os.path.join(day_path,fname)
                    if "DS_Store" in f_path:
                        break
                    file = open(f_path, 'r')
                    found=False
                    for line in file:
                        if firm_name in line or firm_name.upper() in line:
                            non_empty_day=True
                            found=True
                            break
                    file.close()
                    if found:
                        row += "%s%s" % (',', fname[:-4])

            if non_empty_day:
                writer.writerow([row])
    csv_stock.close()


def rename_dir(dirname):

    day_list = []
    for day in os.listdir(dirname):
        day_path = os.path.join(dirname, day)
        if os.path.isdir(day_path):
            day_list.append(day)


    day_list = sorted(day_list)
    double_list = []
    for i,x in enumerate(day_list):
        double_list.append([x, str(i)])

    for double in double_list:
        for day in os.listdir(dirname):
            if double[0] == day:
                day_path = os.path.join(dirname, day)
                new_name = double[1].zfill(4)
                new_path = os.path.join(dirname, new_name)
                os.rename(day_path, new_path)


def rename_file(dirname):

    for day in os.listdir(dirname):
        i = 0
        day_path = os.path.join(dirname, day)
        wsj_path = os.path.join(dirname, day + '/wsj/')
        if os.path.isdir(wsj_path):
            for fname in os.listdir(wsj_path):
                new_fname = "%s%s%s%s" % (day[:4], "_", str(i), ".txt")
                old_path = os.path.join(wsj_path, fname)
                new_path = os.path.join(wsj_path, new_fname)
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                i += 1


if __name__ == '__main__':

    #Loading of files
    spnas = '/Users/admin/Dropbox/School work/SJTU/AIProject/AI_Project/SP500_nasdaq100.csv'
    spnas_df = pd.read_csv(spnas)
    spnas_list = spnas_df[['Symbol', 'Name1']].values.tolist()
    dirname = '/Users/admin/Dropbox/School work/SJTU/AIProject/AI_Project/text_data/'

    firm_csv_folder = '/Users/admin/Dropbox/School work/SJTU/AIProject/AI_Project/firm_csv_folder/'
    #/Users/admin/Dropbox/School work/SJTU/AIProject/AI_Project/‎⁨firm_csv_folder/Comcast.csv


    # Parallelization of the task

    #rename_dir(dirname)
    #rename_file(dirname)

    nb_process = 35

    l = list(np.array_split(spnas_list, nb_process))


    process_list = []
    for spnas in spnas_list:
        if spnas[1][0] is 'Z':
            print(spnas[1])
            process_list.append(mp.Process(target=create_csv_firm, args=(spnas,)))

        #create_csv_firm(spnas)

    for p in process_list:
        p.start()

    for p in process_list:
        p.join()

