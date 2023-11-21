# !/user/bin/env python3
# -*- coding: utf-8 -*-
import csv
import os


# ！！！！！！【【【【【【【记得补充判断一下position的空字符串并输出，这样不用一个一个找没爬取到Positino的了】】】】】


def merge_csv():
    '''将所有文件合并'''
    # 文件存在则删除重新创建
    if os.path.exists('DATA.csv'):
        os.remove('DATA.csv')

    file_list = os.listdir('.')
    csv_list = []
    for file in file_list:
        if file.endswith('.csv'):
            csv_list.append(file)
    print(csv_list)

    with open('DATA.csv', 'a+', newline='', encoding='gb18030') as f:
        writer = csv.writer(f, dialect="excel")  # csv.writer()中可以传一个文件对象
        writer.writerow(
            [ 'fid', '职位', '留言标题', '留言类型', '留言标签', '留言状态', '留言日期', '留言内容', '回复内容', '回复日期',
             '回复机构'])
        for csv_file in csv_list:
            with open(csv_file, 'r', encoding='gb18030' ) as csv_f:
                print("文件为"+csv_file)
                reader = csv.reader(csv_f)
                line_count = 0
                for line in reader:
                    line_count += 1
                    print(line_count)
                    if line_count != 1:
                        writer.writerow(
                            (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10]))

def main():
    '''主函数'''
    print('开始合成文件：')
    merge_csv()
    print('文件合成结束！！！')

if __name__ == '__main__':
    '''执行主函数'''
    main()


