<template>
  <div>
    <div>
        <el-row class="myrow">
            <el-card class="box-card">
              <div class="mycard">
              <div class="mycardleft">
               <img :src=photoUrl class="myimage">
             </div>
             <div class="mycardright">
              <div class="myinfo">
                          <div class="myinforow">
                            <div class="myinforowleft"><span>用户名：</span></div>
                            <div class="myinforowright">
                              <div v-model="name" class="myinfofield">
                              {{ name }}
                              </div>
                            </div>
                            </div>
                <div class="myinforow">
                             <div class="myinforowleft"><span>部门：</span></div>
                            <div  class="myinforowright">
                            <div v-model="department" class="myinfofield">
                              {{department}}
                            </div>
                             </div>
                </div>

                <div class="myinforow">
                <div class="myinforow">
                            <div class="myinforowleft"><span>职位：</span></div>
                            <div  class="myinforowright">
                            <div v-model="jobTitle" class="myinfofield">
                                {{ jobTitle }}
                              </div>
                            </div>
                </div>
                </div>

                <div class="myinforow">
                          <div class="myinforowleft"><span>工号：</span></div>
                        <div  class="myinforowright">
                          <div v-model="jobNo" class="myinfofield">
                              {{ jobNo }}
                          </div>
                          </div>
                </div>
              </div>

                </div>
                </div>
            </el-card>
        </el-row>
    </div>
        <div>
        <el-row class="myrow">
           <div class="myrowcontent">
             <div class="myrowspan">
                 <span class="myrowspan">特征码：</span>
             </div>
             <div class="myrowcomponet">
                 <el-input v-model="serverSpecialCode" placeholder="请输入服务器特征码"></el-input>
             </div>
           </div>
        </el-row>
        <el-row class="myrow">
            <div class="myrowcontent">
              <div class="myrowspan">
                 <span class="myrowspan">版本：</span>
              </div>
              <div class="myrowcomponet">
                <el-select v-model="version" placeholder="请选择EAS版本" >
                <el-option label="8.5" value="8.5"></el-option>
                <el-option label="8.2" value="8.2"></el-option>
                <el-option label="8.0" value="8.0"></el-option>
                <el-option label="7.5" value="7.5"></el-option>
              </el-select>
              </div>
            </div>
        </el-row>
        <el-row class="myrow">
            <div class="myrowcontent">
                  <div class="myrowspan">
                  <span class="myrowspan">站点数：</span>
                  </div>
              <div class="myrowcomponet">
                  <el-input-number size="medium"  v-model="stationNumber" :step="1" style="width: 217.5px"></el-input-number>
              </div>
            </div>
        </el-row>
          <el-row class="myrow">
              <div class="myrowcontent">
            <el-button type="primary" plain class="myapplybtn" @click="applyLicense">
              <span>申请</span>
            </el-button>
              </div>
          </el-row>
        </div>

    </div>
</template>

<script>
    import appInstance from '../App.vue';
    export default {
        name: "ApplyForm",
        data () {
            return {
              serverSpecialCode:'',
              version:'',
              stationNumber:'5',
              name:'',
              department:'',
              jobTitle:'',
              photoUrl:'',
              jobNo:'',
              email:'zengliang_duan@kingdee.com',
            }
        },
        created () {
            this.fetchMyInfo()
        },
        mounted () {
            console.log(1)
        },
        methods:{
          applyLicense: function (event) {
            const loading = this.$loading({
              lock: true,
              text: 'License申请中，请耐心等待提交申请成功提示...',
              spinner: 'el-icon-loading',
              background: 'rgba(0, 0, 0, 0.7)'
            });
            // `this` 在方法里指向当前 Vue 实例
            var url = appInstance.projectConfg.baseUrl+"/applyLicense";
            var postdata = {
              "version": this.version,
              "serverSpecialCode": this.serverSpecialCode,
              "stationNumber":this.stationNumber,
              "email":this.email
            };
            this.$http.post(url,postdata,{ emulateJSON: true },).then((response) => {
              loading.close();
              if(response.body.status == "success"){
                       this.$message({
                          message: '申请成功！',
                          type: 'success'
                       });
                       this.$router.push('LicenseDownload');
                 }else{
                       this.$message({
                          message: '申请失败！',
                          type: 'warning'
                        });
                 }
            }, (response) => {
                // 响应错误回调
                loading.close();
                this.$message.error('服务器响应失败！');
            });
          },
          fetchMyInfo: function(event){
            var url = appInstance.projectConfg.baseUrl+"/fetchMyInfo";
            this.$http.get(url,).then((response) => {
              var myInfo = response.body.myInfo
              this.name = myInfo.name
              this.department = myInfo.department
              this.jobTitle = myInfo.jobTitle
              this.photoUrl = myInfo.photoUrl
              this.jobNo = myInfo.jobNo
              this.email = myInfo.email
              console.log(response)
            });
          },
        }

}
</script>

<style scoped>


  .box-card {
    width: 480px;
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
  }

  .mycard{
     display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    flex-grow: 1;
  }

  .mycardleft{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    width: 50%;
    flex-grow: 0;
  }

  .myimage{
    width:200px;
  }

  .myinfo{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    height: 100%;
    flex-grow: 0;
    flex-wrap: wrap;
  }

  .mycardright{
    display: flex;
    flex-direction: column;
    flex-wrap:nowrap;
    width: 50%;
    flex-grow: 1;
    justify-content: center;
  }

  .myinforow{
     display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
  }

  .myinfofield {
    font-size: 14px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }

  .myinforowleft{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    width: 30%;
  }

  .myinforowright{
    display: flex;
    flex-direction: row;
    justify-content: center;
    width: 70%;
    align-items: center;
  }

  .myrow {
    display: flex;
    flex-direction: row;
    justify-content: center;
    flex-grow: 1;
    margin-bottom: 20px;
  }


  .myrowcontent{
    display: flex;
    flex-grow: 0;
    align-items: center;
    width: 480px;
  }

  .myrowspan{
    display: flex;
    flex-grow: 1;
    flex-direction: row;
    justify-content: flex-start;
  }

  .myrowcomponet{
    display: flex;
    flex-grow: 1;
    flex-direction: row;
    justify-content: flex-end;
  }

  .myapplybtn{
    display: flex;
    flex-grow: 1;
    flex-direction: row;
    justify-content: center;
  }

</style>
