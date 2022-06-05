```json
"chargers": [
    {
      "id": 1, 充电桩编号
      "working": 0,	开，关
      "broken": 1, 故障，正常
      "used_times": 0,	使用次数
      "used_minutes": 0,	使用时间（分钟
      "used_vol": 0,	使用充电量
      "service_length": 0,	服务车辆容量
      "in_service": [	服务车辆信息
        {
          "client_id": 1, 用户编号
          "list_id": 1,	订单编号
          "car_vol": 100,	车辆电容量
          "request_vol": 100,	请求电量
          "queue_minutes": 60,	排队时间
          "real_vol": 10	车辆实际电量
        },
        {
          "client_id": 2,
          "list_id": 1,
          "car_vol": 100,
          "request_vol": 100,
          "queue_minutes": 60,
          "real_vol": 10
        }
      ],
      "date": "100000",	日期
      "charge_cost": 0,	充电费用
      "service_cost": 0,	服务费用
      "total_cost": 0	总费用

    },
    {
      "id": 2,
      "working": 0,
      "broken": 1,
      "used_times": 0,
      "used_minutes": 0,
      "used_vol": 0,
      "service_length": 0,
      "in_service": [
        {
          "client_id": 1,
          "list_id": 1,
          "car_vol": 100,
          "request_vol": 100,
          "queue_minutes": 60,
          "real_vol": 10
        }
      ],
      "date": "100001",
      "charge_cost": 0,
      "service_cost": 0,
      "total_cost": 0
    }

  ]
```

