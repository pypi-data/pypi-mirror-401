import os
import re
import sys

def ToConfigAfter(path='.', language='cn', arena='gray', level='basic'):
    # 验证参数是否在范围内
    valid_languages = ['cn', 'en']
    valid_arenas = ['green', 'blue', 'red', 'gray']
    valid_levels = ['basic', 'advanced']

    if language not in valid_languages:
        print(f"错误: language 参数必须是 {valid_languages} 中的一个")
        return False

    if arena not in valid_arenas:
        print(f"错误: arena 参数必须是 {valid_arenas} 中的一个")
        return False

    if level not in valid_levels:
        print(f"错误: level 参数必须是 {valid_levels} 中的一个")
        return False

    # 检查 build.py 文件是否存在
    build_py_path = os.path.join(path, 'build.py')
    if not os.path.exists(build_py_path):
        print("build.py 文件不存在，跳过修改操作")
        return False

    # 读取文件内容
    with open(build_py_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式替换配置语句
    # 替换 language 配置
    content = re.sub(
        r'config\.language\s*=\s*[\'"]([^\'"]*)[\'"]\s*#\s*\'en\'\s+or\s+\'cn\'',
        f"config.language = '{language}'  # 'en' or 'cn'",
        content
    )

    # 替换 arena 配置
    content = re.sub(
        r'config\.arena\s*=\s*[\'"]([^\'"]*)[\'"]\s*#\s*\'green\',\s*\'blue\',\s*\'red\',\s*\'gray\'',
        f"config.arena = '{arena}'   # 'green', 'blue', 'red', 'gray'",
        content
    )

    # 替换 level 配置
    content = re.sub(
        r'config\.level\s*=\s*[\'"]([^\'"]*)[\'"]\s*#\s*\'basic\',\s*\'advanced\'',
        f"config.level = '{level}'   # 'basic', 'advanced'",
        content
    )

    # 写回文件
    with open(build_py_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"已更新 build.py 配置:")
    print(f"  language = {language}")
    print(f"  arena = {arena}")
    print(f"  level = {level}")
    return True

if __name__ == "__main__":
    # 解析命令行参数
    # 默认值
    path = '.'
    language = 'cn'
    arena = 'gray'
    level = 'basic'

    # 处理命令行参数
    if len(sys.argv) > 1:
        path = sys.argv[1]
    if len(sys.argv) > 2:
        language = sys.argv[2]
    if len(sys.argv) > 3:
        arena = sys.argv[3]
    if len(sys.argv) > 4:
        level = sys.argv[4]

    # 执行更新
    ToConfigAfter(path, language, arena, level)
