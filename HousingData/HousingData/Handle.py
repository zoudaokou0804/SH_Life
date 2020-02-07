def handle_data():
    # 导入pymysql模块
    import pymysql as pmy
    # 连接database
    conn = pmy.connect('localhost', 'root', '123wangchao', 'sh_life', charset='utf8')
    # 得到一个可以执行SQL语句的光标对象
    cur = conn.cursor()
    # 定义要执行的SQL语句
    # sql1 删除重复数据
    print('********************开始删除重复数据************************')
    sql1 = '''DELETE t1 FROM housingdata t1, housingdata t2 WHERE t1.Name = t2.Name'''
    # sql2，sql3充值index
    print('********************开始充值索引Index************************')
    sql2 = '''SET @i=0;'''
    sql3 = '''UPDATE housingdata SET `id`=(@i:=@i+1);'''
    print('********************数据处理完成************************')
    # 执行SQL语句
    cur.execute(sql1)
    cur.execute(sql2)
    cur.execute(sql3)
    # 提交事务
    # data = cur.fetchone()   # 获取下一行数据，第一次为首行
    # data = cur.fetchall()   # 获取所有行数据源
    # data = cur.fetchmany(4) #获取4行数据
    conn.commit()
    # 关闭光标对象
    cur.close()
    # 关闭数据库连接
    conn.close()