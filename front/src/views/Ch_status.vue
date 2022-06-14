<template>
  <table border="1" align="center" style="width:85%; height:400px">
    <tr>
      <td>
        编号：{{current.id}}
        <button v-on:click="last_one" style="float: left">上一个</button>
        <button v-on:click="next_one" style="float: right">下一个</button>
      </td>

    </tr>
    <tr>
      <td>
        状态：{{working}} {{broken}}
        <button v-on:click="switch_charge">开/关</button>
        <button v-on:click="switch_broken">故障/修复（模拟）</button>
        <br>
        充电桩类型：{{kind}}
        <br>
        当前充电区服务车辆数：{{current.service_length}}
      </td>

    </tr>
    <tr>
      <td>累计充电次数：{{statistic.used_times}}</td>

    </tr>
    <tr>
      <td>充电总时长：{{statistic.used_minutes}}</td>
    </tr>
    <tr>
      <td>充电总电量：{{statistic.used_vol}}</td>
    </tr>
    <tr>
      <input type="text" class="in" id="in" placeholder="请输入查询充电桩ID" />
      <button class="btn_search" v-on:click="search">搜索</button>

    </tr>
  </table>
</template>

<script>
import axios from "axios";
import Router from "@/router";
import {useRoute} from "vue-router";
import router from "@/router";

export default {
  name: "Ch_status",
  data(){
    return {
      message: [],
      statistics: [],
      current: "",
      statistic: '',
      current_index: 0,
      current_id: '0',
      working: '运行中',
      broken: '正常',
      timer: '',
      kind: '',
    }
  },
  mounted() {
    let vm = this;
    vm.current_index = 0
    vm.get_data()
    vm.timer = setInterval(() => vm.get_data()
      , 5000)

  },
  methods:{
    search(event){
      let search_id = document.getElementById('in').value
      for(const i in this.message){
        if(this.message[i].id == search_id){
          this.current = this.message[i];
          this.statistic =this.statistics[i]
          this.current_index = parseInt(i);
          this.current_id = search_id
          break;
        }
      }
    },
    get_data(){
      let vm = this
        axios
            .get('http://127.0.0.1:5000/admin/charger/status')
            .then(function (response){
              response = response.data
              let pileInfo = response.allPileInfo
              let report = response.allReportInfo
              console.log(response)
              vm.message = pileInfo;
              vm.statistics = report
              vm.current = pileInfo[0];
              vm.statistic = report[0]
              for(const i in pileInfo){
                if(pileInfo[i].id == vm.current_id && report[i].id == vm.current_id){
                  vm.current = pileInfo[i];
                  vm.statistic = report[i]
                  vm.current_index = parseInt(i);
                  console.log(vm.current)
                  break;
                }
              }

              if(vm.current === null){
                vm.current = pileInfo[0];
                vm.statistic = report[0]
                alert("wrong id")
                return
              }
              vm.data_pre()
            })
            .catch(function (error) { // 请求失败处理
              console.log(error);
            })
    },
    data_pre(event){
      switch (this.current.working) {
        case 'False':
          this.working = "关闭";
          break;
        case 'True':
          this.working = "运行中";
          break;
        default:
          break
      }
      switch (this.current.broken) {
        case 'False':
          this.broken = "正常";
          console.log(this.broken)
          break;
        case 'True':
          this.broken = "故障";
          console.log(this.broken)
          break;
        default:
          break
      }
      switch (this.current.kind) {
        case 'T':
          this.kind = "慢充";
          break;
        case 'F':
          this.kind = "快充";
          break;
        default:
          break
      }
    },
    switch_charge(event){
      console.log(this.message)
      if(this.current.working === false || this.working === '关闭'){
        this.current.working = true
        this.working = '运行中'
        axios.post('http://127.0.0.1:5000/admin/charger/open', {'chargerID': this.current.id}).then(
            function (response){
              if(response === 1){

              }else {
                console.log('ERROR!')
              }
            }
        )
      }
      else{
        this.current.working = false
        this.working = '关闭'
        axios.post('http://127.0.0.1:5000/admin/charger/close', {'chargerID': this.current.id}).then(
            function (response){
              if(response === 1){

              }else {
                console.log('ERROR!')
              }
            }
        )
      }

    },
    switch_broken(event){
      console.log(this.broken, this.current.broken)
      if(this.current.broken === false || this.broken === '正常'){
        this.current.broken = true
        this.broken = '故障'
        axios.post('http://127.0.0.1:5000/admin/charger/break', {'chargerID': this.current.id}).then(
            function (response){
              if(response === 1){

              }else {
                console.log('ERROR!')
              }
            }
        )
      }
      else{
        this.current.broken = false
        this.broken = '正常'
        axios.post('http://127.0.0.1:5000/admin/charger/fix', {'chargerID': this.current.id}).then(
            function (response){
              if(response === 1){

              }else {
                console.log('ERROR!')
              }
            }
        )
      }
    },
    next_one(event){
      console.log(this.message.length, this.current_index + 1)
      if(this.message.length <= this.current_index + 1){
        return
      }else{
        this.current_index = this.current_index + 1
        this.current = this.message[this.current_index]
        this.statistic = this.statistics[this.current_index]
        this.current_id = this.current.id
      }
      this.data_pre()
    },
    last_one(event){
      if(0 > this.current_index - 1){
        return
      }
      this.current_index = this.current_index - 1
      this.current = this.message[this.current_index]
      this.statistic = this.statistics[this.current_index]
      this.current_id = this.current.id
      this.data_pre()
    }
  },
  updated() {
  },
  destroyed() {
    clearInterval(this.timer)
  }
}
</script>

<style scoped>

</style>