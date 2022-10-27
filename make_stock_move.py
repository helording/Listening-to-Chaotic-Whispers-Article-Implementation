# Code attributed from https://github.com/gkeng/Listening-to-Chaotic-Whishpers--Code
import os

stock_value_folder = "stock_values"
stock_move=stock_values_folder+'stock_move'

label_line=[]

def make_stock_move() :

	for x in os.listdir(stock_values_folder):
		count_up=0
		count_neut=0
		count_down=0
		if x[-4:] == '.csv':
		    file_path = os.path.join(stock_values_folder,x)
		    print(x)
		    f = open(file_path,'r')
		    data = f.readlines()
		    f.close()
		    for i in range(len(data)-1):

		        open_t=float(data[i].split(',')[1])
		        open_tp1=float(data[i+1].split(',')[1])
		        raise_t =(open_tp1-open_t)/open_t
		        if raise_t >0.0045:
		            label=1
		        if (raise_t<= 0.0045 and raise_t>=-0.0045):
		            label=0
		        if raise_t<-0.0045:
		            label=-1
		        line='{}{}{}{}'.format(data[i].split(',')[0],',',str(label),'\n')
		        label_line.append(line)

		    with open('{}{}{}'.format(stock_move,x,'.csv'),'w') as f:
		        for line in label_line:
		            f.write(line)
	return(count_up,count_neut,count_down)
