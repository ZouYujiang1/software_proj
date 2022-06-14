<template>

  <el-row>
    <el-col
        v-for="(o, index) in 10"
        :key="o"
        :span="5"
        :offset="index % 4 == 0 ? 0 : 1"
    >
      <el-card :body-style="{ padding: '0px' }" style="margin-top: 20px">
        <table class="ui celled table" border="1">
          <thead>
          <tr>
            <th></th>
            <th>标题</th>
            <th>类型</th>
            <th>概要</th>
            <th>更新时间</th>
            <th>操作</th>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>1</td>
            <td>2</td>
            <td>3</td>
            <td>4</td>
            <td>5</td>
            <td>

            </td>
          </tr>
          </tbody>
          <tfoot>

          </tfoot>
        </table>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: "Index"
}
</script>

<style scoped>

</style>