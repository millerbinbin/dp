# encoding=utf-8
import jieba


seg_list = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造", cut_all=False, HMM=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
