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
        充电桩类型：{{current.kind}}
        <br>
        当前充电区服务车辆数：{{current.service_length}}
      </td>

    </tr>
    <tr>
      <td>累计充电次数：{{current.used_times}}</td>

    </tr>
    <tr>
      <td>充电总时长：{{current.used_minutes}}</td>
    </tr>
    <tr>
      <td>充电总电量：{{current.used_vol}}</td>
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
      current: "",
      current_index: 0,
      current_id: '0',
      working: '运行中',
      broken: '正常',
      timer: '',
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
          this.current_index = i;
          this.current_id = search_id
          break;
        }
      }
    },
    get_data(){
      let vm = this
        axios
            .get('http://localhost:8081/chargers')
            .then(function (response){
              vm.message = response;

              vm.current = response[0];
              for(const i in response){
                if(response[i].id == vm.current_id){
                  vm.current = response[i];
                  vm.current_index = i;
                  console.log(vm.current)
                  break;
                }
              }

              if(vm.current === null){
                vm.current = response[0];
                alert("wrong id")
                return
              }
              switch (vm.current.working) {
                case 0:
                  vm.working = "关闭";
                  break;
                case 1:
                  vm.working = "运行中";
                  break;
                default:
                  break
              }
              switch (vm.current.broken) {
                case 0:
                  vm.broken = "正常";
                  break;
                case 1:
                  vm.broken = "故障";
                  break;
                default:
                  break
              }
              console.log(vm.current)
            })
            .catch(function (error) { // 请求失败处理
              console.log(error);
            })
    },
    data_pre(event){

      switch (this.current.working) {
        case 0:
          this.working = "关闭";
          break;
        case 1:
          this.working = "运行中";
          break;
        default:
          break
      }
      switch (this.current.broken) {
        case 0:
          this.broken = "正常";
          break;
        case 1:
          this.broken = "故障";
          break;
        default:
          break
      }
    },
    switch_charge(event){
      if(this.current.working === 0){
        this.current.working = 1
        this.working = '运行中'
        axios.post('/charger/open', {'chargerID': this.current.id}).then(
            function (response){
              console.log(response)
            }
        )
      }
      else{
        this.current.working = 0
        this.working = '关闭'
        axios.post('/charger/close', {'chargerID': this.current.id}).then(
            function (response){
              console.log(response)
            }
        )
      }

    },
    switch_broken(event){
      if(this.current.broken === 0){
        this.current.broken = 1
        this.broken = '故障'
        axios.post('/charger/break', {'chargerID': this.current.id}).then(
            function (response){
              console.log(response)
            }
        )
      }
      else{
        this.current.broken = 0
        this.broken = '正常'
        axios.post('/charger/fix', {'chargerID': this.current.id}).then(
            function (response){
              console.log(response)
            }
        )
      }
    },
    next_one(event){
      this.current_index = this.current_index + 1
      if(this.message.length <= this.current_index){
        return
      }else{
        this.current = this.message[this.current_index]
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