# 导入pymysql模块
import pymysql as pmy
def handle_data():
    # 连接database
    conn = pmy.connect('localhost', 'root', '123wangchao', 'sh_life', charset='utf8')
    # 得到一个可以执行SQL语句的光标对象
    cur = conn.cursor()
    # 定义要执行的SQL语句
    # sql1 删除重复数据
    sql1 = '''DELETE t1 FROM housingdata t1, housingdata t2 WHERE t1.Name = t2.Name AND t1.IndexId > t2.IndexId'''
    # sql2，sql3充值index
    sql2 = '''SET @i=0;'''
    sql3 = '''UPDATE housingdata SET IndexId=(@i:=@i+1);'''
    sql4 = '''ALTER TABLE housingdata AUTO_INCREMENT=0;'''

    # 执行SQL语句
    print('********************开始预处理数据************************')
    cur.execute(sql1)
    # print('********************开始重置索引Index************************')
    cur.execute(sql2)
    cur.execute(sql3)
    cur.execute(sql4)
    # 提交事务
    # data = cur.fetchone()   # 获取下一行数据，第一次为首行
    # data = cur.fetchall()   # 获取所有行数据源
    # data = cur.fetchmany(4) #获取4行数据
    conn.commit()
    # 关闭光标对象
    cur.close()
    # 关闭数据库连接
    conn.close()
    print('********************数据预处理完成************************')


if __name__ == "__main__":
    handle_data()