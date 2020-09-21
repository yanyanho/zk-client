## ZK-BAC Python钱包服务  

### 1.1 功能
Python钱包服务以Django服务框架为基础，使用fisco python sdk与fisco节点交互和使用GRPC与零知识证明计算服务Prover_server交互，
为用户提供账号（包括fisco账号和匿名账号）创建，资产（包括bac token和匿名资产commits）管理，匿名交易，智能合约（包括Bac001合约和Groth16mixer合约）调用和查询交易记录等服务。
其中，匿名交易包括： 
-  将bac token存入到Groth16mixer合约，生成匿名资产commits（一次最多生成两个）；
- 向匿名账号转账（一次最多指定两个匿名账号）；
- 从Groth16mixer合约提取匿名资产为bac token。

此服务提供BAC的匿名转账功能；  
 1 生成ZKBAC地址（匿名转账所需的地址）和fisco地址（公开转账需要）   
 2 存入资产（从fisco地址转移BAC到匿名转账合约地址以生成UTXO到ZKBAC地址），ZKBAC地址获取utxo    
 3 转账  （ZKBAC地址互转，全匿名）  
 4 取出资产  （从ZKBAC地址转移到fisco地址）  

### 1.2 部署

- 环境要求：Python 3.7， gcc，mysql  
#### 1.2.1
 - 1 拉取代码：
    git clone git@git.weoa.com:ttip/bac-zk-client.git;
 - 2 进入zk-client目录
 ```
    cd bac-zk-client && cd zk-client;
    pip install -r requirements.txt   #安装相关python库;
 ```
 - 3 拷贝fisco节点sdk证书到python_web3/bin目录下;
 -  在./commands/constants.py中配置prover_server，fisco节点，mysql服务器的地址，端口和数据库等信息:


```
FISCO_RPC_ENDPOINT_DEFAULT = http://119.23.46.126:8545（Fisco节点的地址）
PROVER_SERVER_ENDPOINT_DEFAULT = "116.85.72.123:50051"（PROVER_SERVER的地址）
DATABASE_DEFAULT_ADDRESS = "39.108.248.156"（数据库地址）
DATABASE_DEFAULT_PORT = 3306（数据库端口）
DATABASE_DEFAULT_USER = "root"（数据库用户名）
DATABASE_DEFAULT_PASSWORD = "******"（数据库密码）
DATABASE_DEFAULT_DATABASE = "zk_test"（数据库名字）
```
 

 - 5 创建数据库以及初始化表：
    create database zk_test（这里的数据库名字与配置文件中的数据库名字DATABASE_DEFAULT_DATABASE一致）  
    use zk_test  
    使用create_tables.sql文件中的sql语句创建表      


 - 6 数据库初始化完成后：
  ```
python manage.py runserver 0.0.0.0:5002 
#启动django服务（如果python命令默认是python2，请使用python3命令）  
  ```
### 1.3 接口说明
   1 产生匿名地址：
   
   ```
  {
    "description": "genZbacAddr",
    "request": {
      "method": "POST",
      "uri": "/genZbacAddr",

      "body": {
        "username": "hehe"
      }
    },
    "response": {
    "status": 0,
    "address": "d3603132dbaf076060d16d911a4adf8d6624b60510a819def82599353a0685ec:8f37a09af7b7469a5b7bef573e941521e8cc8ef6c528b30a16a5b7bb211f7362"
     }
  }
  ```

 2 将BAC资产转换为匿名资产
```
  {
    "description": "depositBac",
    "request": {
      "method": "POST",
      "uri": "/depositBac",

      "body": {
       "username": "hehe",
      "password":"123456",
     "token_amount":20,
	  "mixer_address":"0x808b153005654821f8c9b2e9344807998734a999",
	"token_address":"0x511003e45fdbfdc993d6a87b6c71dedda2fe5e09",
	"value1": 10,
	"value2":10
      }
    },
    "response": {
       "status": 0,
    "commits": [
        "29c6f32e",
        "1b9e9873"
    ],
    "total_value": "20"
    }
  },
``` 
 3 匿名转账
```
{
    "description": "zkbac transfer",
    "request": {
      "method": "POST",
      "uri": "/mixBac",
      "body": {
        "username": "hehe",
        "password": "123456",
        "token_amount": 20,
        "vin": 0,
        "vout": 0,
        "mixer_address": "0x808b153005654821f8c9b2e9344807998734a999",
        "token_address": "0x511003e45fdbfdc993d6a87b6c71dedda2fe5e09",
        "input_notes": [
          "29c6f32e",
          "1b9e9873"
        ],
        "output_specs": [
          "71640b0fe737a883b7a51ce81eb08c04c8504df17a8cff30e5bb0ad722fd7240:18c4a3ce86546a36aedb7d456cd5c29bc8986d02061e1249b5f9ff2bcc03d519,20"
        ]
      }
    },
     "response": {
    "status": 0,
    "text": "mix success"
    }
  },
```
4 匿名资产提取为BAC地址
```
{
    "description": "zkbac withdraw",
    "request": {
      "method": "POST",
      "uri": "/mixBac",

      "body": {
       "username": "hehe",
      "password":"123456",
      "token_amount":20,
      "vin":0,
      "vout":20,
	"mixer_address":"0x808b153005654821f8c9b2e9344807998734a999",
	"token_address":"0x511003e45fdbfdc993d6a87b6c71dedda2fe5e09",
	"input_notes": ["29c6f32e","1b9e9873"],
	"output_specs":[]
      }
    },
    "response": {
      "status": 0,
      "commits": [],
      "total_value": "0"
    }
  },

```