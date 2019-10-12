<template>
    <div>
    <el-row type="flex" justify="center" style="margin-bottom:10px">
    <el-col :span="12">
      <el-input v-model="email" placeholder="请输入云之家账号">用户名</el-input>
    </el-col>
    </el-row>
    <el-row type="flex" justify="center" style="margin-bottom:10px">
    <el-col :span="12">
      <el-input type="password" v-model="password" placeholder="请输入云之家密码">密码</el-input>
    </el-col>
      </el-row>
      <el-row type="flex" justify="center" >
     <el-col :span="24">
     <el-button type="primary" @click="login">登录</el-button>
    </el-col>
     </el-row>
  </div>
</template>

<script>
  export default {
    name: "LicenseLogin",
     data () {
        return {
          msg: 'Welcome to Your Vue.js App',
          email:'',
          password:'',
        }
  },
  methods: {
    login(){
         var url = "http://www.easlicense.tk:80/login";
            var postdata = {"email": this.email, "password": this.password};
            this.$http.post(url,postdata,{emulateJSON:true}).then((res) =>{
                 if(res.data == "success"){
                       this.$message({
                          message: '登录成功！',
                          type: 'success'
                       });
                       this.$router.push('ApplyForm');
                 }else{
                       this.$message({
                          message: '登陆失败，请核对信息！',
                          type: 'warning'
                        });
                 }
            }, (res) => {
                // 响应错误回调
                this.$message.error('服务器响应失败！');
          });
        },
    testcookie(){
      var url = "http://www.easlicense.tk:80/testcookie";
      this.$axios.get(url).then((res)=>{
                 if(res.body == "success"){
                       this.$message({
                          message: '请求cookie成功！',
                          type: 'success'
                       });
                 }else{
                       this.$message({
                          message: '请求cookie失败！',
                          type: 'warning'
                        });
                 }

            });
    }
   }
}
</script>

<style scoped>

</style>
