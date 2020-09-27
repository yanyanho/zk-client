### 接口说明  

#### 1.1 账户产生  
  产生fisco账户和匿名账户地址。
  接口如下：
  ```      
    {
    "description": "genAccount",
    "request": {
      "method": "POST",
      "uri": "/genAccount",
      "body": {
        "username": "hehe",
        "password": "123456"
      }
    },
    "response": {
    "status": 0,
    "fisco_address": "0xc0c5e664442b3d5f0aa4d30e900d5aeeef596e04",
    "publickey": "0x3fa34c3f31a42c65c4c7056d05d3130f4d0d29bba81266de06b79be3cf80740e",
    "privatekey": "0x3fa34c3f31a42c65c4c7056d05d3130f4d0d29bba81266de06b79be3cf80740e",
    "zbac_address": "d3603132dbaf076060d16d911a4adf8d6624b60510a819def82599353a0685ec:8f37a09af7b7469a5b7bef573e941521e8cc8ef6c528b30a16a5b7bb211f7362"
      }
  }
  ```


**1）参数表**    

输入：

| **序号** | **参数名**   | **类型**       |  **必填**        | **说明**      |    
| -------- | --------  | ------------  | -------------- | ------------  |  
| 1       |  username     | String         |            是  |    用户名      |  
| 2       |  password     | String         |            是  |     密码       |  


输出：  

| **序号** | **参数名**   | **类型**       |       **说明**      |    
| -------- | --------  | ------------  | ------------  |  
| 1       |  fisco_address     | String         |           fisco地址      |  
| 2       |  publickey     | String         |            fisco地址公钥       |  
| 3       |  privatekey     | String         |            fisco地址私钥       |  
| 4       |  zbac_address     | String         |            匿名地址       |  



#### 1.2 获取合约相关信息  
  获取BAC合约和mixer合约地址 
```
   {
    "description": "getContract",
    "request": {
      "method": "GET",
      "uri": "/getContract"
    },
    "response":   {
    "contracts": {
        "bacContract": {
            "contractName": "BAC001",
            "contractType": "bac",
            "contractAddr": "0x24c945fc747b1a5a228765a3d985b9a12ebe8e1c",
            "ownerAddr": "0xf1585b8d0e08a0a00fff662e24d67ba95a438256",
            "totalAmount": 50000000000,
            "shortName": "zk-AAA-demo"
        },
        "mixerContract": {
            "contractName": "Groth16Mixer",
            "contractType": "mixer",
            "contractAddr": "0xfdfec928bec8c5e3aa0d93f08c4440b36842bc50",
            "ownerAddr": "0xf1585b8d0e08a0a00fff662e24d67ba95a438256",
            "totalAmount": 0,
            "shortName": "mixer_test"
        }
    },
    "status": 0
}       
}
```
**1）参数表**  
输入： 无
输出：  

| **序号** | **参数名**   | **类型**       |       **说明**      |    
| -------- | --------  | ------------  | ------------  |  
| 1       |  contracts     | 符合类型        |           合约相关的信息     |  

 #### 1.3 存入资产
  将BAC资产转换成匿名ZKBAC资产，获得等量commit  
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
  }
```   

**1）参数表**    

输入：

| **序号** | **参数名**   | **类型**       |  **必填**        | **说明**      |    
| -------- | --------  | ------------  | -------------- | ------------  |  
| 1       |  username     | String         |            是  |    用户名      |  
| 2       |  password     | String         |            是  |     密码       |  
| 3       |  token_amount     | String         |            是  |     BAC资产地址       |  
| 4       |  mixer_address     | String         |            是  |     mixer合约地址       |  
| 5       |  token_address     | String         |            是  |     token合约地址       |  
| 6       |  value1     | int         |            是  |     zkBAC的commit值（默认输出两个commit）       |  
| 7       |  value2     | int         |            是  |     zkBAC的commit值       |  


输出：  

| **序号** | **参数名**   | **类型**       |       **说明**      |    
| -------- | --------  | ------------  | ------------  |  
| 1       |  commits     | List<String>         |           zkBAC的commit      |  
| 1       |  total_value     | int         |           commit总金额      |  


#### 1.4 匿名资产转账
匿名ZKBAC资产互相转账，使用commit和匿名地址
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
  }
```
输入：

| **序号** | **参数名**   | **类型**       |  **必填**        | **说明**      |    
| -------- | --------  | ------------  | -------------- | ------------  |  
| 1       |  username     | String         |            是  |    用户名      |  
| 2       |  password     | String         |            是  |     密码       |  
| 3       |  token_amount     | String         |            是  |     BAC资产地址       |  
| 4       |  mixer_address     | String         |            是  |     mixer合约地址       |  
| 5       |  token_address     | String         |            是  |     token合约地址       |  
| 6       |  vin     | int         |            是  |    公开输入的转账部分 默认是0       |  
| 7       |  vout     | int         |            是  |    公开输出的转账部分  默认是0      |  
| 8       |  input_notes     | List<String>         |            是  |    输入的commit      |  
| 9       |  output_specs     |  List<String>        |            是  |    接收者地址和金额      |  


输出：  

| **序号** | **参数名**   | **类型**       |       **说明**      |    
| -------- | --------  | ------------  | ------------  |  
| 1       |  text   | String         |          状态描述     |  


#### 1.5 匿名资产提取
 将ZKBAC匿名资产转换成BAC资产
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
  }
```
**1）参数表**    

输入：

| **序号** | **参数名**   | **类型**       |  **必填**        | **说明**      |    
| -------- | --------  | ------------  | -------------- | ------------  |  
| 1       |  username     | String         |            是  |    用户名      |  
| 2       |  password     | String         |            是  |     密码       |  
| 3       |  token_amount     | String         |            是  |     BAC资产地址       |  
| 4       |  mixer_address     | String         |            是  |     mixer合约地址       |  
| 5       |  token_address     | String         |            是  |     token合约地址       |  
| 6       |  vin     | int         |            是  |    公开输入的转账部分 默认是0       |  
| 7       |  vout     | int         |            是  |    公开输出的转账部分  默认是0      |  
| 8       |  input_notes     | List<String>         |            是  |    输入的commit      |  
| 9       |  output_specs     |  List<String>        |            是  |    接收者地址和金额      |  


输出：  

| **序号** | **参数名**   | **类型**       |       **说明**      |    
| -------- | --------  | ------------  | ------------  |  
| 1       |  commits     | List<String>         |           zkBAC的commit      |  
| 1       |  total_value     | int         |           commit总金额      |  
