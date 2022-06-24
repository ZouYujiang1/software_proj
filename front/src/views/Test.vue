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
              <el-icon>
                <icon-menu/>
              </el-icon>
              <span>测试界面</span>
            </el-menu-item>

          </el-menu>
          <el-card>
            <template #header>
              <div class="card-header">
                <span>测试用例</span>
              </div>
            </template>
            <div v-for="(i, index) in ceshi" class="text item" style="padding-bottom: 20px">{{i}}</div>
          </el-card>
        </el-aside>
        <el-main>

          <div v-if="index == 1">
            <el-row>
              <el-col

                  :key="o"
                  :span="10"
                  :offset="index % 2 == 0 ? 0 : 2"
                  v-for="(item,index) in list"
              >
                <el-card  v-if="item != null" style="margin-top: 20px; width: 500px;">
                  <el-row>
                    <el-col :span="6">车辆标号：</el-col>
                    <el-col :span="5">{{item.order.id - 2}}</el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">本车排队代码：</el-col>
                    <el-col :span="5">{{ item.number }}</el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">前车等待数量：</el-col>
                    <el-col :span="5">{{ item.carsAhead }}</el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">当前所在区域：</el-col>
                    <el-col :span="5">{{ item.area }}</el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">使用充电桩：</el-col>
                    <el-col :span="5">{{ item.chargePileID }}</el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">当前使用电量：</el-col>
                    <el-col :span="5">{{ (item.usedVol).toFixed(2) }}</el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">当前费用：</el-col>
                    <el-col :span="5">{{ (item.usedCost).toFixed(2) }}</el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">等待前车进度：</el-col>
                    <el-col :span="5">
                      <el-progress
                          :text-inside="true"
                          :stroke-width="20"
                          :percentage="item.car_per"
                          status="exception"
                          color="blue"
                      >
                        <span>排队进度</span>
                      </el-progress>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">汽车充电进度：</el-col>
                    <el-col :span="5">
                      <el-progress type="dashboard" :percentage="item.ele_per" :indeterminate="true">
                        <template #default="{ percentage }">
                          <span class="percentage-value">{{ percentage.toFixed(2) }}%</span>

                        </template>
                      </el-progress>
                    </el-col>
                  </el-row>
                  <button @click="endCharging(index)">结束充电</button>
                </el-card>
              </el-col>
            </el-row>

            <div>
              <button @click="test">test</button>
            </div>
          </div>


        </el-main>
      </el-container>
    </div>


  </div>
</template>

<script>

import axios from "axios";

export default {
  name: "Test",
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
      timerList: [],
      timerList2: [],
      list: [],
      ceshi: [],
      testData:[
        {
          name: '3', id: 3, requestVol : 40, chargingMode : 'T', modeChoose : 'A',
          time : '2022/6/16 6:00:00', year : 2022, month : 6, day : 16,
          hour : 6,
          minute : 0,
          second : 0,
        },
        {
          name: '4', id: 4, requestVol : 30, chargingMode : 'T', modeChoose : 'A',
          time : '2022/6/16 6:05:00', year : 2022, month : 6, day : 16,
          hour : 6,
          minute : 5,
          second : 0,
        },
        {
          name: '5', id: 5, requestVol : 100, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 6:10:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 10,

        },
        {
          name: '6', id: 6, requestVol : 120, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 6:15:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 15,

        },
        {
          name: '4', id: 4, requestVol : 0, chargingMode : 'O', modeChoose : 'A',
          time : '2022/6/16 6:20:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 20,

        },
        {
          name: '7', id: 7, requestVol : 20, chargingMode : 'T', modeChoose : 'A',
          time : '2022/6/16 6:25:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 25,

        },
        {
          name: '8', id: 8, requestVol : 20, chargingMode : 'T', modeChoose : 'A',
          time : '2022/6/16 6:30:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 30,

        },
        {
          name: '9', id: 9, requestVol : 110, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 6:35:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 35,

        },
        {
          name: '10', id: 10, requestVol : 20, chargingMode : 'T', modeChoose : 'A',
          time : '2022/6/16 6:40:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 40,

        },
        {
          name: '11', id: 11, requestVol : 105, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 6:45:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 45,

        },
        {
          name: '12', id: 12, requestVol : 10, chargingMode : 'T', modeChoose : 'A',
          time : '2022/6/16 6:50:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 50,

        },
        {
          name: '13', id: 13, requestVol : 110, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 6:55:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 6,
          minute : 55,

        },
        {
          name: '14', id: 14, requestVol : 90, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 7:00:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 0,

        },
        {
          name: '15', id: 15, requestVol : 110, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 7:05:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 5,

        },
        {
          name: '16', id: 16, requestVol : 95, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 7:10:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 10,

        },
        {
          name: '17', id: 17, requestVol : 10, chargingMode : 'T', modeChoose : 'A',
          time : '2022/6/16 7:15:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 15,

        },
        {
          name: '18', id: 18, requestVol : 60, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 7:20:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 20,

        },
        {
          name: '19', id: 19, requestVol : 10, chargingMode : 'T', modeChoose : 'A',
          time : '2022/6/16 7:25:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 25,

        },
        {
          name: '20', id: 20, requestVol : 7.5, chargingMode : 'T', modeChoose : 'A',
          time : '2022/6/16 7:30:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 30,

        },
        {
          name: '21', id: 21, requestVol : 75, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 7:35:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 35,

        },
        {
          name: '22', id: 22, requestVol : 95, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 7:40:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 40,

        },
        {
          name: '23', id: 23, requestVol : 95, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 7:45:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 45,

        },
        {
          name: '24', id: 24, requestVol : 70, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 7:50:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 50,

        },
        {
          name: '25', id: 25, requestVol : 80, chargingMode : 'F', modeChoose : 'A',
          time : '2022/6/16 7:55:00', year : 2022, month : 6, day : 16,second : 0,
          hour : 7,
          minute : 55,

        },
        {
          name: '26',
          id: 26,
          requestVol : 5,
          chargingMode : 'T',
          modeChoose : 'A',
          time : '2022/6/16 8:00:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 8,
          minute : 0,
          second : 0,
        },{
          name: '27',
          id: 27,
          requestVol : 15,
          chargingMode : 'T',
          modeChoose : 'A',
          time : '2022/6/16 8:20:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 8,
          minute : 20,
          second : 0,
        },{
          name: 'T1',
          id: 111,
          requestVol : 0,
          chargingMode : 'O',
          modeChoose : 'B',
          time : '2022/6/16 8:25:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 8,
          minute : 25,
          second : 0,
        },{
          name: '28',
          id: 28,
          requestVol : 20,
          chargingMode : 'T',
          modeChoose : 'A',
          time : '2022/6/16 8:30:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 8,
          minute : 30,
          second : 0,
        },{
          name: '29',
          id: 29,
          requestVol : 25,
          chargingMode : 'T',
          modeChoose : 'A',
          time : '2022/6/16 8:35:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 8,
          minute : 35,
          second : 0,
        },{
          name: 'F1',
          id: 101,
          requestVol : 5,
          chargingMode : 'O',
          modeChoose : 'B',
          time : '2022/6/16 8:50:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 8,
          minute : 50,
          second : 0,
        },{
          name: '30',
          id: 30,
          requestVol : 30,
          chargingMode : 'F',
          modeChoose : 'A',
          time : '2022/6/16 9:00:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute : 0,
          second : 0,
        },{
          name: '3',
          id: 3,
          requestVol : 0,
          chargingMode : 'O',
          modeChoose : 'A',
          time : '2022/6/16 9:10:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute : 10,
          second : 0,
        },{
          name: 'T1',
          id: 111,
          requestVol : 1,
          chargingMode : 'O',
          modeChoose : 'B',
          time : '2022/6/16 9:15:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute : 15,
          second : 0,
        },{
          name: '29',
          id: 29,
          requestVol : 0,
          chargingMode : 'O',
          modeChoose : 'A',
          time : '2022/6/16 9:20:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute : 20,
          second : 0,
        },{
          name: '23',
          id: 23,
          requestVol : 35,
          chargingMode : 'F',
          modeChoose : 'C',
          time : '2022/6/16 9:25:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute : 25,
          second : 0,
        },{
          name: '21',
          id: 21,
          requestVol : 0,
          chargingMode : 'O',
          modeChoose : 'A',
          time : '2022/6/16 9:30:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute : 30,
          second : 0,
        },{
          name: '30',
          id: 30,
          requestVol : 0,
          chargingMode : 'O',
          modeChoose : 'A',
          time : '2022/6/16 9:35:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute : 35,
          second : 0,
        },{
          name: '25',
          id: 25,
          requestVol : 40,
          chargingMode : 'F',
          modeChoose : 'C',
          time : '2022/6/16 9:40:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute : 40,
          second : 0,
        },{
          name: '31',
          id: 31,
          requestVol : 30,
          chargingMode : 'T',
          modeChoose : 'A',
          time : '2022/6/16 9:50:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute : 50,
          second : 0,
        },{
          name: '16',
          id: 16,
          requestVol : 30,
          chargingMode : 'F',
          modeChoose : 'C',
          time : '2022/6/16 9:55:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 9,
          minute :55,
          second : 0,
        },{
          name: '32',
          id: 32,
          requestVol : 10,
          chargingMode : 'T',
          modeChoose : 'A',
          time : '2022/6/16 10:00:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 10,
          minute : 0,
          second : 0,
        },{
          name: 'F1',
          id: 101,
          requestVol : 1,
          chargingMode : 'O',
          modeChoose : 'B',
          time : '2022/6/16 10:50:00',
          year : 2022,
          month : 6,
          day : 16,
          hour : 10,
          minute : 50,
          second : 0,
        }

      ],
    }
  },
  created() {

  },
  mounted() {

  },
  methods: {

    test() {
      var _this = this
      var i = 0
      var timer = setInterval(function (){
        if (i == 40){
          window.clearInterval(timer)
        }
        var temp = _this.testData[i]
        _this.startTest(i, temp)
        i++
      }, 5000)

    },
    startTest(i, order){
      var _this = this

      switch (order.modeChoose){
        case 'A':
          if(order.chargingMode === 'O'){
            _this.list.push(null)
            let j,k;
            for (k = 0; k < i; k++){
              if(_this.testData[k].id === _this.testData[i].id){
                j = k;
                console.log(613, j)
                break;
              }
            }
            _this.endCharging(j)
          }
          else{
            _this.onSubmit(i, order)
          }
          break;
        case 'B':
          _this.list.push(null)
          _this.switch_broken(i, order)
          break;
        case 'C':
          _this.list.push(null)
          let j, k;
          for (k = 0; k < i; k++){
            if(_this.testData[k].id === _this.testData[i].id){
              j = k;
              console.log(613, j)
              break;
            }
          }
          _this.change(i, order, j)
          break;
      }

    },
    sleep(numberMillis) {
      var now = new Date();
      var exitTime = now.getTime() + numberMillis;
      while (true) {
        now = new Date();
        if (now.getTime() > exitTime)
          return true;
      }
    },
    switch_broken(i, order){
      let _this = this;
      if(order.name === 'F1'){
        order.id = 1
      }else {
        order.id = 3
      }
      if(order.requestVol === 0){
        axios.post('http://127.0.0.1:5000/admin/charger/break', {'chargerID': order.id}).then(
            function (response){
              if(response.data === 1){
              }else {
                console.log('ERROR!')
              }
            }
        )
      }
      else{
        axios.post('http://127.0.0.1:5000/admin/charger/fix', {'chargerID': order.id}).then(
            function (response){
              if(response.data === 1){
              }else {
                console.log('ERROR!')
              }
            }
        )
      }
    },
    change(i, order, j){

      var _this = this
      window.clearInterval(_this.timerList[j])
      window.clearInterval(_this.timerList2[j])
      axios.post('http://127.0.0.1:5000/usr/modify-chargingreq', _this.list[i].order).then(
          function (response) {
            switch (data.carStatus) {
              case 3:
                _this.list[j].area = "优先等待区"
                break;
              case 2:
                _this.list[j].area = "等待区"
                break;
              case 1:
                _this.list[j].area = "充电等待区"
                break;
              default:
                _this.list[j].area = "充电区"
                break;
            }

            _this.list[j].number = data.carsAhead + 1 + ""
            _this.list[j].carsAhead = data.carsAhead + ""

            _this.list[j].chargePileID = data.chargePileID
            var s = (j+1) + '进入' + _this.area + '在' + order.time + '修改了' + order.requestVol + '充电量'
            _this.ceshi.push(s)
            _this.timerList[i] = setInterval(function () {
              _this.perSecond(i)
            }, 1000)
          }
      )
    },
    cancle() {
      var _this = this
      axios.post('http://127.0.0.1:5000/usr/cancel', _this.order).then(
          function (response) {
            window.clearInterval(_this.timer)
            window.clearInterval(_this.timer2)
            _this.isRunning = false
          }
      )
    },
    endCharging(index) {
      console.log(index)
      var _this = this
      axios.post('http://127.0.0.1:5000/usr/cancel', _this.list[index].order).then(
          function (response) {
            var str = (_this.list[index].order.id - 2) + '结束充电'
            _this.ceshi.push(str)
            window.clearInterval(_this.timerList[index])
            window.clearInterval(_this.timerList2[index])
            console.log(726, response.data)
            if(response.data.msg !== 'success to cancel!'){
              axios.post('http://127.0.0.1:5000/usr/end-charging', _this.list[index].order).then(
                  function (response) {
                    _this.list[index].area = '离开'
                    _this.list[index].chargePileID = null
                    _this.list[index].carsAhead = null
                    _this.isRunning = false
                    // _this.menu = response.data
                  }
              ).catch(
                  function (err){
                    console.log(err)
                  }
              )
            }
          }
      )
    },
    perSecond(i) {
      const _this = this
      console.log(728, _this.list, _this.list[i], i)
      axios.post('http://127.0.0.1:5000/usr/car-status', _this.list[i].order).then(
          function (response) {
            _this.list[i].carsAhead = response.data.carsAhead
            console.log("V", i+1, response.data)
            switch (response.data.carStatus) {
              case 3:
                _this.list[i].area = "优先等待区"
                break;
              case 2:
                _this.list[i].area = "等待区"
                break;
              case 1:
                _this.list[i].number = null
                _this.list[i].carsAhead = null
                _this.list[i].area = "充电等待区"
                break;
              default:
                _this.list[i].area = "充电区"
                break;
            }
            _this.list[i].chargePileID = response.data.chargePileID

            switch (response.data.status){
              case 'charging':
                window.clearInterval(_this.timerList[i])
                axios.post('http://127.0.0.1:5000/usr/start-charging', _this.list[i].order).then(
                    function (response) {
                      _this.list[i].queueNo = null
                      console.log("V", i+1, response.data)
                      switch (response.data.carStatus) {
                        case 3:
                          _this.list[i].area = "优先等待区"
                          break;
                        case 2:
                          _this.list[i].area = "等待区"
                          break;
                        case 1:
                          _this.list[i].area = "充电等待区"
                          break;
                        default:
                          _this.list[i].area = "充电区"
                          break;
                      }
                      _this.timerList2[i] = setInterval(function () {
                        _this.perSecond2(i)
                      }, 1000)
                    }
                )
            }
          }
      )
    },
    perSecond2(i) {
      const _this = this
      axios.post('http://127.0.0.1:5000/usr/car-status', _this.list[i].order).then(
          function (response) {
            _this.list[i].number = null
            _this.list[i].chargePileID = response.data.chargePileID
            _this.list[i].usedVol = response.data.usedVol
            _this.list[i].usedCost = response.data.usedCost
            switch (response.data.carStatus) {
              case 3:
                _this.list[i].carsAhead = response.data.carsAhead
                _this.list[i].area = "优先等待区"
                break;
              case 2:
                _this.list[i].area = "等待区"
                break;
              case 1:
                _this.list[i].number = null
                _this.list[i].carsAhead = null
                _this.list[i].area = "充电等待区"
                break;
              default:
                _this.list[i].area = "充电区"
                break;
            }
            if (response.data.status === 'charging-finished'){
              _this.list[i].carsAhead = response.data.carsAhead
              _this.list[i].chargePileID = response.data.chargePileID
              window.clearInterval(_this.timerList2[i])
              // _this.list[i] = null
              console.log("V", i+1, response.data)
              axios.post('http://127.0.0.1:5000/usr/end-charging', _this.list[i].order).then(
                  function (response) {
                    console.log("V", i+1, response.data.status)
                    _this.list[i].area = '离开'
                    _this.list[i].chargePileID = null
                    _this.list[i].carsAhead = null
                    _this.isRunning = false
                    _this.menu = response.data
                  }
              ).catch(
                  function (err){
                    console.log(err)
                  }
              )
            }
            else if (response.data.status === 'charging'){
              _this.list[i].vol += response.data.incVol
              _this.list[i].ele_per = (_this.list[i].vol / _this.list[i].carVol) * 100
            }
            else if (response.data.status === 'prewaiting'){

            }
            else {

            }
          }
      )
    },
    handleSelect(key, keyPath) {
      this.index = key
    },
    onSubmit(i, order) {
      var mode = [100, 150, 200, 250, 300]
      var _this = this
      _this.order.carVol = mode[Math.floor(Math.random() * 5)]
      _this.order.startVol = Math.floor(Math.random() * (order.carVol + 1))
      _this.vol = order.startVol
      axios.post('http://127.0.0.1:5000/usr/getqueueno', order).then(
          function (response) {
            console.log(870, response)
            if(response.data == "There are not enough spaces in the waiting area!"){
              var str = (order.id - 2) + '离开了充电桩'
              _this.ceshi.push(str)
            }
            else{
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
              var str = (order.id - 2) + '进入' + _this.area + '在' + order.time + '申请了' + order.requestVol + '充电量'
              _this.ceshi.push(str)
              var obj = {}
              obj.number = data.carsAhead + 1 + ""
              obj.carsAhead = data.carsAhead + ""
              obj.area = _this.area
              obj.chargePileID = data.chargePileID
              obj.car_per = (data.carsAhead + 1 - data.carsAhead) / (data.carsAhead + 1) * 100

              obj.carVol = mode[Math.floor(Math.random() * 5)]
              obj.startVol = Math.floor(Math.random() * (obj.carVol + 1))
              obj.ele_per = (obj.startVol / obj.carVol) * 100
              obj.vol = obj.startVol
              obj.order = order
              obj.order.startVol = obj.startVol
              obj.order.carVol = obj.carVol
              obj.usedCost = 0
              obj.usedVol = 0

              _this.list.push(obj)
              console.log(895, i, _this.list)
              _this.timerList[i] = setInterval(function () {
                _this.perSecond(i)
              }, 1000)
            }


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