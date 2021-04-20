


##### 简要描述

- 搜索接口

##### 请求URL
- ` /input_search/<node_name> `
##### 请求方式
- GET 

##### 路径参数

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|node_name |是  |string |搜索节点name   |

##### 返回示例 

``` 
{
  "error_code": 0, 
  "relationship_information": [
    {
      "relationship": "建议游玩时长", 
      "source_id": "40", 
      "source_name": "灵峰", 
      "target_id": "53", 
      "target_name": "半天"
    }, 
    {
      "relationship": "所属地区", 
      "source_id": "40", 
      "source_name": "灵峰", 
      "target_id": "44", 
      "target_name": "雁荡山"
    }, 
    {
      "relationship": "总面积", 
      "source_id": "44", 
      "source_name": "雁荡山", 
      "target_id": "80", 
      "target_name": "450平方公里"
    }
  ], 
  "start_node": {
    "start_id": "40", 
    "start_name": "灵峰"
  }
}
```

##### 返回参数说明 

|参数名|类型|说明|
|:-----  |:-----|-----                           |
|error_code |int   |存储返回信息 0:查询到数据，返回 1:未查询到数据  |
|relationship_information |list   |由若干dict构成，每一个dict代表一条关系信息  |
|start_node |dict   |存储开始节点信息  |

##### 备注 

- 每一条关系信息的格式为{节点name，节点id，关系名，节点name，节点id}



