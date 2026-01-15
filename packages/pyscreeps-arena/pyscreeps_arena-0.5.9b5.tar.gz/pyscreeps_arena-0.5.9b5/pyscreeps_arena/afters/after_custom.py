import os
import re


def ToCustomAfter(path='.'):
    # 检查 prefab 目录是否存在
    prefab_dir = os.path.join(path, 'src', 'prefab')
    if not os.path.exists(prefab_dir):
        print("src/prefab 目录不存在，跳过处理")
        return

    # 创建 src/custom 目录
    custom_dir = os.path.join(path, 'src', 'custom')
    if not os.path.exists(custom_dir):
        os.makedirs(custom_dir)
        print("已创建 src/custom 目录")
    else:
        print("src/custom 目录已存在，跳过创建操作")

    # 遍历 prefab 目录中的非 _ 开头的 .py 文件
    for file_name in os.listdir(prefab_dir):
        if file_name.startswith('_') or not file_name.endswith('.py'):
            continue

        file_path = os.path.join(prefab_dir, file_name)
        print(f"处理文件: {file_path}")

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否存在 """$TEMPLATE...""" 的内容
        template_match = re.search(r'"""(\$TEMPLATE.*?)"""', content, re.DOTALL)
        if template_match:
            template_content = template_match.group(1)
            # 移除开头的 $TEMPLATE 标记
            template_content = re.sub(r'^\s*\$TEMPLATE\s*', '', template_content)

            # 在 custom 目录下创建同名文件
            custom_file_path = os.path.join(custom_dir, file_name)
            with open(custom_file_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
            print(f"已在 custom 目录下创建 {file_name} 文件")
        else:
            print(f"{file_name} 中未找到模板内容，跳过")

    # 检查并修改 src/main.py 文件，在导入语句末尾添加 from custom import *
    main_py_path = os.path.join(path, 'src', 'main.py')
    if not os.path.exists(main_py_path):
        print("src/main.py 文件不存在，跳过导入语句添加操作")
        return

    # 读取文件内容
    with open(main_py_path, 'r') as f:
        lines = f.readlines()

    # 检查是否存在 from custom import * 语句
    has_custom_import = False
    import_end_line = 0

    for i, line in enumerate(lines):
        if re.search(r'from\s+custom\s+import\s+\*', line):
            has_custom_import = True
            break
        # 检查是否为导入语句
        if re.match(r'^(from|import)\s+', line.strip()):
            import_end_line = i + 1  # 记录导入语句的结束位置（下一行）

    if not has_custom_import:
        # 在导入语句的末尾插入 from custom import * 语句
        if import_end_line > 0:
            # 在导入语句末尾插入
            lines.insert(import_end_line, '\nfrom custom import *\n')
        else:
            # 如果没有导入语句，在文件开头插入
            lines.insert(0, 'from custom import *\n')

        # 写回文件
        with open(main_py_path, 'w') as f:
            f.writelines(lines)
        print("已在 src/main.py 中导入语句末尾追加 from custom import * 语句")
    else:
        print("src/main.py 中已存在 from custom import * 语句，跳过添加操作")


if __name__ == "__main__":
    ToCustomAfter('.')
