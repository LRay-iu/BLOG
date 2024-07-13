import os


def generate_albums():
    # 获取当前脚本所在的目录
    directory = os.path.dirname(os.path.abspath(__file__))

    # 获取目录下的所有文件
    files = os.listdir(directory)

    # 过滤出所有图片文件（假设图片文件的扩展名为jpg, jpeg, png, gif）
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    images = [file for file in files if os.path.splitext(
        file)[1].lower() in image_extensions]

    # 生成 albums 列表
    albums = [[f"/gallery/index/{image}", image] for image in images]

    # 将 albums 列表写入到 albums.txt 文件中
    output_file = os.path.join(directory, "albums.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("albums: [\n")
        for album in albums:
            f.write(f'    ["{album[0]}", "{album[1]}"],\n')
        f.write("]")

    print(f"albums.txt 已生成在目录 {directory} 下")


# 调用函数
generate_albums()
