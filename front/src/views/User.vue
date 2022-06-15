<template>
  <div class="chat">

    <div>
      <el-container>
        <el-aside width="200px" style="background-color: transparent; border-radius: 5px;">

          <el-menu
              default-active="1"
              class="el-menu-vertical-demo"
              @open="handleOpen"
              @close="handleClose"
              background-color="#FFFFFF66"
              @select="handleSelect"
          >
            <el-menu-item index="1">
              <template #title>
                <el-icon>
                  <location/>
                </el-icon>
                <span>个人信息</span>
              </template>
            </el-menu-item>
            <el-menu-item index="2">
              <el-icon>
                <icon-menu/>
              </el-icon>
              <span>充电详单</span>
            </el-menu-item>

            <el-menu-item index="3">
              <el-icon>
                <icon-menu/>
              </el-icon>
              <span>充电界面</span>
            </el-menu-item>

          </el-menu>
        </el-aside>
        <el-main>
          <div v-if="index == 1">
            <el-card>
              <el-row>
                <el-col :span="8">
                  <el-avatar :size="100"
                             src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
                </el-col>
              </el-row>
              <el-form :model="form" label-width="120px" style="margin-top: 20px;">
                <el-form-item label="用户名：">
                  <div>{{ userName }}</div>
                </el-form-item>
              </el-form>
            </el-card>
          </div>
          <div v-if="index == 2">
            <el-card>
              <el-row>
                <el-col :span="8">
                  <el-avatar :size="100"
                             src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
                </el-col>
              </el-row>
              <el-form :model="form" label-width="120px" style="margin-top: 20px;">
                <el-form-item label="用户名：">
                  <div>{{ userName }}</div>
                </el-form-item>
              </el-form>
            </el-card>
          </div>
          <div v-if="index == 3">
            <el-card>
              <el-form :model="order" label-width="120px">
                <el-form-item label="充电电量">
                  <el-input v-model="order.requestVol"/>
                </el-form-item>
                <el-form-item label="充电模式">
                  <el-select v-model="order.chargingMode" placeholder="请选择你的充电模式">
                    <el-option label="快充" value="F"/>
                    <el-option label="慢充" value="T"/>
                  </el-select>
                </el-form-item>

                <el-form-item>
                  <el-button v-if="isRunning == false" type="primary" @click="onSubmit">请求充电</el-button>
                  <el-button v-else type="primary" @click="onSubmit" disabled>请求充电</el-button>
                  <el-button @click="cancle">结束充电</el-button>
                </el-form-item>
              </el-form>
            </el-card>
            <el-card style="margin-top: 20px">
              <el-row>
                <el-col :span="4">本车排队代码：</el-col>
                <el-col :span="5">{{ number }}</el-col>
              </el-row>
              <el-row>
                <el-col :span="4">前车等待数量：</el-col>
                <el-col :span="5">{{ carsAhead }}</el-col>
              </el-row>
              <el-row>
                <el-col :span="4">当前所在区域：</el-col>
                <el-col :span="5">{{ area }}</el-col>
              </el-row>
              <el-row>
                <el-col :span="4">预期使用充电桩：</el-col>
                <el-col :span="5">{{ chargePileID }}</el-col>
              </el-row>
              <el-row>
                <el-col :span="4">等待前车进度：</el-col>
                <el-col :span="5">
                  <el-progress
                      :text-inside="true"
                      :stroke-width="20"
                      :percentage="car_per"
                      status="exception"
                      color="blue"
                  >
                    <span>排队进度</span>
                  </el-progress>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="4">汽车充电进度：</el-col>
                <el-col :span="5">
                  <el-progress type="dashboard" :percentage="ele_per">
                    <template #default="{ percentage }">
                      <span class="percentage-value">{{ percentage }}%</span>

                    </template>
                  </el-progress>
                </el-col>
              </el-row>
              <button>结束充电</button>
            </el-card>
          </div>
          <div>
            {{menu}}
          </div>
          <div>
            <button @click="test">test</button>
          </div>
        </el-main>
      </el-container>
    </div>


  </div>
</template>

<script>

import axios from "axios";

export default {
  name: "User",
  data() {
    return {
      userName: window.localStorage.getItem("userName"),
      logoUrl: "../assets/images/logo.png",
      isAdmin: window.localStorage.getItem("isAdmin"),
      index: 1,
      form: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      },
      order: {
        name: window.localStorage.getItem("userName"),
        id: window.localStorage.getItem("id"),
        requestVol: 0,
        startVol: 0,
        chargingMode: "",
        carVol: 0
      },
      carStatus: 0,
      chargePileID: "暂未加入排队序列",
      carsAhead: "暂未加入排队序列",
      queueNo: 0,
      number: "暂未加入排队序列",
      area: "暂未加入排队序列",
      car_per: 0,
      ele_per: 0,
      totalCar: 0,
      isRunning: false,
      timer: null,
      timer2: null,
      vol: 0,
      menu: {},
      timerList: []
    }
  },
  created() {

  },
  mounted() {
    this.cancle()

    window.clearInterval(this.timer)
    const userName = window.localStorage.getItem("userName")
    console.log(userName)
  },
  methods: {
    test() {
      var _this = this
      for (let i = 6; i <= 8; i++) {
        _this.order.userName = i + ''
        _this.order.id = i
        _this.order.requestVol = 10
        _this.order.chargingMode = 'F'
        _this.onSubmit()
      }
    },
    cancle() {
      var _this = this
      axios.post('http://127.0.0.1:5000/usr/cancel', _this.order).then(
          function (response) {
            window.clearInterval(_this.timer)
            window.clearInterval(_this.timer2)
            console.log(response)
            _this.isRunning = false
          }
      )
    },
    perSecond() {
      const _this = this
      axios.post('http://127.0.0.1:5000/usr/car-status', _this.order).then(
          function (response) {
            _this.carsAhead = response.data.carsAhead
            console.log(_this.order.userName, response)
            switch (response.data.status){
              case 'charging':
                window.clearInterval(_this.timer)
                axios.post('http://127.0.0.1:5000/usr/start-charging', _this.order).then(
                    function (response) {
                      console.log(response.data)
                      _this.timer2 = setInterval(function () {
                        _this.perSecond2()
                      }, 1000)
                    }
                )
            }
          }
      )
    },
    perSecond2() {
      const _this = this
      axios.post('http://127.0.0.1:5000/usr/car-status', _this.order).then(
          function (response) {
            _this.carsAhead = response.data.carsAhead
            if (response.data.status == 'charging-finished'){
              window.clearInterval(_this.timer2)
              axios.post('http://127.0.0.1:5000/usr/end-charging', _this.order).then(
                  function (response) {
                    console.log(_this.order.userName, response)
                    _this.isRunning = false
                    _this.menu = response.data
                  }
              )
            } else {
              _this.vol += response.data.incVol
              _this.ele_per = (_this.vol / _this.order.carVol) * 100
            }
            console.log(response)
            }
      )
    },
    handleSelect(key, keyPath) {
      this.index = key
      console.log(this.index)
    },
    onSubmit() {
      var mode = [100, 150, 200, 250, 300]
      var _this = this
      _this.order.carVol = mode[Math.floor(Math.random() * 5)]
      _this.order.startVol = Math.floor(Math.random() * (_this.order.carVol + 1))
      _this.vol = _this.order.startVol
      console.log(this.order)
      axios.post('http://127.0.0.1:5000/usr/getqueueno', _this.order).then(
          function (response) {
            console.log(response)
            let data = response.data
            _this.carStatus = data.carStatus
            _this.chargePileID = data.chargePileID
            _this.carsAhead = data.carsAhead + ""
            _this.queueNo = data.queueNo
            _this.number = data.carsAhead + 1 + ""
            _this.totalCar = data.carsAhead + 1
            _this.car_per = (data.carsAhead + 1 - data.carsAhead) / (data.carsAhead + 1) * 100
            _this.ele_per = (_this.order.startVol / _this.order.carVol) * 100
            _this.isRunning = true
            console.log(_this.car_per)
            switch (data.carStatus) {
              case 3:
                _this.area = "优先等待区"
                break;
              case 2:
                _this.area = "等待区"
                break;
              case 1:
                _this.area = "充电等待区"
                break;
              default:
                _this.area = "充电区"
                break;
            }

            _this.timer = setInterval(function () {
              _this.perSecond()
            }, 1000)

          }
      )
    }
  }
}
</script>

<style scoped>

.chat {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 200%;
  z-index: -1;

  background-image: linear-gradient(45deg, rgba(0, 200, 255, 0.4) 0%, rgba(132, 43, 171, 0.4) 100%);
}

#title {
  color: white;
  position: center !important;
}

.contain {
  background: rgba(34, 34, 34, 0.5) !important;
}

.m-card {
  margin-right: 40px;
  background-image: linear-gradient(45deg, rgba(0, 200, 255, 0.4) 0%, rgba(132, 43, 171, 0.4) 100%);
}

.ourpage {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  border-radius: 5px;
}
</style>