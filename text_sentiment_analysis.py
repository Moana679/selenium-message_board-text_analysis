# !/user/bin/env python3
# -*- coding: utf-8 -*-

from cntext import senti_by_hownet
import pandas as pd
import numpy as np
import pyreadstat

data, meta = pyreadstat.read_dta('data.dta')
 
# 首先将pandas读取的数据转化为array
texts_array = np.array(data[['留言内容']])

# 然后转化为list形式
texts_list =texts_array.tolist()  

# 嵌套列表展开
texts = []
for _ in texts_list:
    texts += _

df = pd.DataFrame(columns=['id', 'sentence_num', 'word_num', 'stopword_num', 'pos_score', 'neg_score'])

for idx, text in enumerate(texts):
    score= senti_by_hownet(text, adj_adv=True)
    score = pd.DataFrame([score])
    score.insert(loc=0, column='id', value=idx+1)
    df=df.append(score)

df.to_csv('data_senti.csv')
    
    

    

