##1.任务与提示词
角色：你是Python教学助手
任务：写一段代码读生词表CSV井生成练习题要求：按HSK等级筛选、统计词性分布、输出txt，仅用标准库，每行加注释。
最后你输出给我的应该是一段代码

##2.AI初代代码
# 导入csv标准库，用来读取csv生词表文件
import csv

# 定义函数：读取生词表csv文件
def load_words(csv_path="生词表.csv"):
    # 打开csv文件
    with open(csv_path) as f:
        # 将csv内容转为字典列表，方便按字段读取
        word_list = list(csv.DictReader(f))
    return word_list

# 定义函数：根据指定HSK等级筛选词汇
def filter_by_hsk(word_list, target_level="4"):
    # 创建空列表存放筛选后的词汇
    filter_result = []
    # 遍历全部词汇
    for item in word_list:
        # 判断当前词汇的HSK等级是否匹配目标等级
        if item["HSK等级"] == target_level:
            filter_result.append(item)
    return filter_result

# 定义函数：统计词汇的词性分布
def count_pos(word_list):
    # 新建空字典，用来记录每种词性的数量
    pos_count = {}
    # 遍历所有词汇
    for item in word_list:
        pos = item["词性"]
        # 如果字典没有该词性，默认0，计数+1
        pos_count[pos] = pos_count.get(pos, 0) + 1
    return pos_count

# 定义函数：生成练习题并写入txt文件
def generate_exercise(word_list, txt_path="练习题.txt"):
    # 打开txt文件，准备写入
    out_file = open(txt_path, "w")
    # 遍历筛选后的词汇，生成造句题目
    for word_info in word_list:
        line = f"请使用词汇「{word_info['词汇']}」造一个句子\n"
        out_file.write(line)
    # 关闭文件
    out_file.close()

# 主程序入口
if __name__ == "__main__":
    # 读取全部生词
    all_words = load_words()
    # 筛选HSK4词汇
    hsk4_words = filter_by_hsk(all_words, "4")
    # 统计词性
    pos_dist = count_pos(hsk4_words)
    print("词性统计结果：", pos_dist)
    # 生成练习题txt
    generate_exercise(hsk4_words)
    print("练习题已经生成完成！")


##3.我的修改点
修改点1：为文件读取、写入增加 encoding="utf-8"

• 修改位置：load_words 和 generate_exercise 函数内所有open()语句

• 修改原因：Windows系统默认编码不是utf-8。不加这个参数，中文CSV和输出txt容易出现中文乱码。

修改点2：HSK等级对比增加字符串转换 str()

• 修改位置：filter_by_hsk 函数的if判断条件

• 修改原因：CSV读取出来的字段可能是数字或者字符串类型。统一转为字符串再对比，避免类型不一致，导致筛选词汇失败。

修改点3：改写文件写入逻辑，把手动open+close改为with open()

• 修改位置：generate_exercise函数

• 修改原因：原始代码手动调用open()和close()。如果程序中途报错，文件不会正常关闭。with语句可以自动关闭文件，代码更加安全规范。

修改点4：修改文件路径，采用相对路径 data/生词表.csv，移除weekpath模块

• 修改位置：load_words函数默认路径，删除import weekpath

• 修改原因：weekpath是课程自定义模块，本机没有安装，会报模块缺失错误。改用相对路径，仅使用Python自带标准库；约定csv放在项目下data文件夹，项目结构清晰。

##4.最终代码
# 导入csv标准库，用来读取csv生词表文件
import csv

# 定义函数：读取生词表csv文件
def load_words(csv_path="data/生词表.csv"):
    # 打开csv文件，增加utf-8编码防止中文乱码
    with open(csv_path, encoding="utf-8") as f:
        # 将csv内容转为字典列表，方便按字段读取
        word_list = list(csv.DictReader(f))
    return word_list

# 定义函数：根据指定HSK等级筛选词汇
def filter_by_hsk(word_list, target_level="4"):
    # 创建空列表存放筛选后的词汇
    filter_result = []
    # 遍历全部词汇
    for item in word_list:
        # 转字符串对比，防止数字/字符串类型不匹配
        if str(item["HSK等级"]) == str(target_level):
            filter_result.append(item)
    return filter_result

# 定义函数：统计词汇的词性分布
def count_pos(word_list):
    # 新建空字典，用来记录每种词性的数量
    pos_count = {}
    # 遍历所有词汇
    for item in word_list:
        pos = item["词性"]
        # 如果字典没有该词性，默认0，计数+1
        pos_count[pos] = pos_count.get(pos, 0) + 1
    return pos_count

# 定义函数：生成练习题并写入txt文件
def generate_exercise(word_list, txt_path="练习题.txt"):
    # 使用with自动管理文件，不用手动close
    with open(txt_path, "w", encoding="utf-8") as out_file:
        # 遍历筛选后的词汇，生成造句题目
        for word_info in word_list:
            line = f"请使用词汇「{word_info['词汇']}」造一个句子\n"
            out_file.write(line)

# 主程序入口
if __name__ == "__main__":
    # 读取全部生词
    all_words = load_words()
    # 筛选HSK4词汇
    hsk4_words = filter_by_hsk(all_words, "4")
    # 统计词性
    pos_dist = count_pos(hsk4_words)
    print("词性统计结果：", pos_dist)
    # 生成练习题txt
    generate_exercise(hsk4_words)
    print("练习题已经生成完成！")
