<template>
  <div id="container">
    <div id="header" style="background-color: #ffa500;">
      <h1 style="margin-bottom: 0; color: blue;">充电桩管理</h1>
    </div>

    <div id="menu" style="background-color: #ffd700;  float:left; width:15%; height:400px">
      <ul>
        <table border="0" align="center" style="height:200px">
          <tr>
            <td>
              <router-link :to="{name: 'Ch_status', params:{'id': this.current.id}}" >充电桩状态</router-link>
            </td>
          </tr>
          <tr>
            <td>
              <router-link :to="{name: 'Ch_service', params:{'id': this.current.id}}" >服务车辆信息</router-link>
            </td>
          </tr>
          <tr>
            <td>
              <router-link :to="{name: 'Ch_statistic', params:{'id': this.current.id}}" >累计数据报表</router-link>
            </td>
          </tr>

        </table>



      </ul>
    </div>
    <router-view></router-view>

    </div>
</template>

<script>
import axios from "axios";
import router from "@/router";
import {useRoute} from "vue-router";

export default {
  name: "Charger",
  data(){
    return {
      message: 'test',
      current: {'id': 0}
    }
  },
  methods :{

  },
  mounted() {
    let vm = this;
    axios
        .get('http://localhost:8081/chargers')
        .then(function (response){
          vm.message = response;
          vm.current = response[0];
          router.push({name: 'Ch_status', params:{'id': 1}})
        })
        .catch(function (error) { // 请求失败处理
          console.log(error);
        });
  },
  updated() {

  }

}
</script>

<style scoped>

</style>