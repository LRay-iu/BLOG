import os
import csv
import urllib.parse


def extract_urls_from_csv():
    # 获取当前脚本所在的目录
    directory = os.path.dirname(os.path.abspath(__file__))

    # 获取目录下的所有文件
    files = os.listdir(directory)

    # 过滤出所有CSV文件
    csv_files = [file for file in files if os.path.splitext(file)[
        1].lower() == '.csv']

    # 处理每个CSV文件
    albums = []
    for csv_file in csv_files:
        csv_path = os.path.join(directory, csv_file)
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'userDomainUrl' in row:
                    url = row['userDomainUrl']
                    decoded_url = urllib.parse.unquote(url)
                    albums.append([decoded_url])

    # 将 albums 列表写入到 albums.txt 文件中
    output_file = os.path.join(directory, "url.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for album in albums:
            f.write(f'  - image: "{album[0]}"\n  # title: \n  # description: \n')

    print(f"albums.txt 已生成在目录 {directory} 下")


# 调用函数
extract_urls_from_csv()
