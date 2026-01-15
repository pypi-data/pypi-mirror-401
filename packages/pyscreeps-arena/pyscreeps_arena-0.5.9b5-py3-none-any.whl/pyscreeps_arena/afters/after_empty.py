import os
import re

def ToEmptyAfter(path='.'):
    # 删除 src/basic.py 文件
    basic_path = os.path.join(path, 'src', 'basic.py')
    if os.path.exists(basic_path):
        os.remove(basic_path)
        print("已删除 src/basic.py")
    else:
        print("src/basic.py 不存在，跳过删除操作")

    # 修改 src/main.py 文件，将 from basic import * 改为 from builtin import *
    main_path = os.path.join(path, 'src', 'main.py')
    if os.path.exists(main_path):
        with open(main_path, 'r') as f:
            content = f.read()

        # 使用正则表达式替换，处理各种可能的空白字符
        modified_content = re.sub(r'from\s+basic\s+import\s+\*', 'from builtin import *', content)

        # 检查是否发生了替换
        if modified_content != content:
            with open(main_path, 'w') as f:
                f.write(modified_content)
            print("已修改 src/main.py，将 from basic import * 改为 from builtin import *")
        else:
            print("src/main.py 中未找到 from basic import * 语句，跳过修改操作")
    else:
        print("src/main.py 不存在，跳过修改操作")

if __name__ == "__main__":
    ToEmptyAfter('.')
    