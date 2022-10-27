# Code attributed from https://github.com/gkeng/Listening-to-Chaotic-Whishpers--Code
import pickle
import os

stock_move = "stock_move"

def pickle_stock_move():

	for fname in os.listdir(stock_move):
		if fname[-4:]=='.csv':
		    print (fname)
		    file_path=os.path.join(stock_move,fname)
		    f=open(file_path,'r')
		    lines = f.readlines()
		    f.close()
		    dic={}
		    for line in lines:
		        line=line.replace('\n','').split(',')
		        dic[line[0]]=float(line[1])

		    with open('{}{}{}'.format(stock_move_pickle , fname[:-8],'.pkl'),'wb') as pick:
		        pickle.dump(dic, pick, protocol=pickle.HIGHEST_PROTOCOL)
