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
              <router-link :to="{name: 'Ch_status'}" >充电桩状态</router-link>
            </td>
          </tr>
          <tr>
            <td>
              <router-link :to="{name: 'Ch_service'}" >服务车辆信息</router-link>
            </td>
          </tr>
          <tr>
            <td>
              <router-link :to="{name: 'Ch_statistic'}" >累计数据报表</router-link>
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
      current: '',

    }
  },
  methods :{

  },
  mounted() {
    router.push({name: 'Ch_status'})
  },
  computed:{
    id(){
      const route = useRoute()
      console.log(route.params.id)
      return route.params.id
    }
  },

  updated() {

  }

}
</script>

<style scoped>

</style>