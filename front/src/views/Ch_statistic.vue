<template>
  <table border="1" align="center" style="width:85%; height:400px">
    <tr>
      <td>
        充电桩编号：{{current.id}}
        <button v-on:click="last_one" style="float: left">上一个</button>
        <button v-on:click="next_one" style="float: right">下一个</button>
      </td>

    </tr>
    <tr>
      <td>
        时间：{{current.date}}
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
      <td>累计充电费用：{{current.charge_cost}}</td>
    </tr>
    <tr>
      <td>累计服务费用：{{current.service_cost}}</td>
    </tr>
    <tr>
      <td>累计总费用：{{current.total_cost}}</td>
    </tr>
  </table>
</template>

<script>
import axios from "axios";
import Router from "@/router";
import {useRoute} from "vue-router";

export default {
  name: "Ch_status",
  data(){
    return {
      message: "",
      current: "",
      current_index: 0,
      current_id: '000'
    }
  },
  mounted() {
    let vm = this;
    const route = useRoute()
    //从路由中获取充电桩id
    vm.current_id = route.params.id
    axios
        .get('http://localhost:8081/chargers')
        .then(function (response){
          vm.message = response;
          vm.current = response[0];
          for(const i in response){
            if(response[i].id === vm.current_id){
              vm.current = response[i];
              vm.current_index = i;
              break;
            }
          }

          if(vm.current === null){
            vm.current = response[0];
            alert("wrong id")
          }

        })
        .catch(function (error) { // 请求失败处理
          console.log(error);
        });
  },
  methods:{
    data_pre(event){

    },
    switch_charge(event){

    },
    next_one(event){
      if(this.message.length <= this.current_index + 1){
        return
      }
      this.current_index = this.current_index + 1
      this.current = this.message[this.current_index]
      this.data_pre()
    },
    last_one(event){
      if(0 > this.current_index - 1){
        return
      }
      this.current_index = this.current_index - 1
      this.current = this.message[this.current_index]
      this.data_pre()
    }
  }
}
</script>

<style scoped>

</style>