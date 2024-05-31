import os
import jieba
import jieba.posseg as pseg
from multiprocessing import Pool, cpu_count

# 设置文件路径
novel_dir = r'C:\Users\HP\PycharmProjects\NLP_homework\homework_3\金庸-语料库'  # 16部金庸小说的文件夹路径
stopwords_file = r'C:\Users\HP\PycharmProjects\NLP_homework\homework_3\cn_stopwords.txt'  # 停用词文件路径

# 加载停用词
with open(stopwords_file, 'r', encoding='gbk', errors='ignore') as f:
    stopwords = set(f.read().strip().split('\n'))

# 定义只保留名词词性的函数
def filter_pos(words):
    return [word for word, flag in pseg.cut(words) if flag.startswith('n')]

# 定义预处理函数
def preprocess_text(text):
    # 分词
    words = jieba.cut(text)
    # 去除停用词
    words = [word for word in words if word not in stopwords]
    # 过滤词性
    words = filter_pos(' '.join(words))
    # 去除非中文字符
    words = [word for word in words if all('\u4e00' <= char <= '\u9fff' for char in word)]
    return words

# 处理单个文件的函数
def process_file(filepath):
    with open(filepath, 'r', encoding='gbk', errors='ignore') as f:
        text = f.read()
    return preprocess_text(text)

# 获取所有小说文件的路径
filepaths = [os.path.join(novel_dir, filename) for filename in os.listdir(novel_dir) if filename.endswith('.txt')]

# 使用多进程处理文件
if __name__ == '__main__':
    with Pool(cpu_count()) as pool:
        processed_texts = pool.map(process_file, filepaths)

    # 输出预处理后的结果
    for i, text in enumerate(processed_texts):
        print(f"Processed text from novel {i+1}: {' '.join(text[:100])}...")  # 仅展示前100个词
