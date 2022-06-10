<template>
  <table border="1" align="center" style="width:85%; height:400px">
    <tr>
      <td>
        充电桩编号：{{current.id}}
        <button v-on:click="last_one" style="float: left">上一个</button>
        <button v-on:click="next_one" style="float: right">下一个</button>
      </td>

    </tr>
    <tr v-for="car in cars">
      <td>
        用户ID：{{car.client_id}}
      </td>
      <td>
        车辆电容量：{{car.car_vol}}
      </td>
      <td>
        请求充电量：{{car.request_vol}}
      </td>
      <td>
        排队时间（分钟）：{{car.queue_minutes}}
      </td>

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

export default {
  name: "Ch_status",
  data(){
    return {
      message: "",
      current: "",
      cars: [],
      current_index: 0,
      timer: '',
    }
  },
  mounted() {
    let vm = this;
    const route = useRoute()
    //从路由中获取充电桩id
    vm.current_id = route.params.id
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
                  break;
                }
              }

              if(vm.current === null){
                vm.current = response[0];
                alert("wrong id")
                return
              }
              vm.cars = vm.current.in_service
            })
            .catch(function (error) { // 请求失败处理
              console.log(error);
            });
    },
    data_pre(event){
      this.cars = this.current.in_service
    },
    next_one(event){
      if(this.message.length <= this.current_index + 1){
        return
      }
      this.current_index = this.current_index + 1
      this.current = this.message[this.current_index]
      this.current_id = this.current.id
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