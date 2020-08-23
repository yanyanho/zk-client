## ZK-BAC Python钱包服务  

### 1.1 功能
Python钱包服务以Django服务框架为基础，使用fisco python sdk与fisco节点交互和使用GRPC与零知识证明计算服务Prover_server交互，为用户提供账号（包括fisco账号和匿名账号）创建，资产（包括bac token和匿名资产commits）管理，匿名交易，智能合约（包括Bac001合约和Groth16mixer合约）调用和查询交易记录等服务。
其中，匿名交易包括： 
-  将bac token存入到Groth16mixer合约，生成匿名资产commits（一次最多生成两个）；
- 向匿名账号转账（一次最多指定两个匿名账号）；
- 从Groth16mixer合约提取匿名资产为bac token。

### 1.2 部署
- 环境要求：Python 3.7， gcc，mysql
Git clone https://github.com/yanyanho/zk-client.git
- 进入zk-client目录
Pip install -r requirement.txt 安装相关python库

在./commands/constants.py中配置prover_server，fisco节点，mysql服务器的地址，端口和数据库等信息:
```
FISCO_RPC_ENDPOINT_DEFAULT = http://119.23.46.126:8545（Fisco节点的地址）
PROVER_SERVER_ENDPOINT_DEFAULT = "116.85.72.123:50051"（PROVER_SERVER的地址）
DATABASE_DEFAULT_ADDRESS = "39.108.248.156"（数据库地址）
DATABASE_DEFAULT_PORT = 3306（数据库端口）
DATABASE_DEFAULT_USER = "root"（数据库用户名）
DATABASE_DEFAULT_PASSWORD = "******"（数据库密码）
DATABASE_DEFAULT_DATABASE = "zk_test"（数据库名字）
```

创建数据库以及初始化表：
Create database zk_test（这里的数据库名字与配置文件中的数据库名字DATABASE_DEFAULT_DATABASE一致）  
Use zk_test  
使用create_tables.sql文件中的sql语句创建表  

数据库初始化完成后：  
python manage.py runserver 0.0.0.0:5002 启动django服务（如果python命令默认是python2，请使用python3命令）  
