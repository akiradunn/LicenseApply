<template>
  <div class="downloadLayoutClass">
    <div class="downLoadClass">
      <el-button style="wdith:480px" type="primary" @click="downLoad">下载License<i class="el-icon-upload el-icon--right"></i></el-button>
    </div>
  </div>
</template>

<script>
    import appInstance from '../App.vue';
    export default {
        name: "LicenseDownload",
        data () {
              return {
                licenseLogoUrl: './assets/photo.png',
                licenseFileUrl:'',
                isGenerateLicenseFile:false,
              }
          },
        created () {
            this.genLicenseAttach();
        },
        mounted () {
            console.log(1);
        },
        methods: {
          genLicenseAttach: function (event) {
             const loading = this.$loading({
              lock: true,
              text: 'License文件生成中，请耐心等待文件生成成功提示...',
              spinner: 'el-icon-loading',
              background: 'rgba(0, 0, 0, 0.7)'
            });
            // `this` 在方法里指向当前 Vue 实例
            var url = appInstance.projectConfg.baseUrl+"/genLicenseAttach";
            this.$http.get(url).then((response) => {
              if (response.body.status == "success") {
                this.isGenerateLicenseFile = true;
                this.$message({
                          message: '生成附件成功！',
                          type: 'success'
                 });
              }
            });
            setTimeout(() => {
              loading.close();
            }, 2000);
          },
          downLoad:function (event) {
            //document.cookie.split(";")[6].split("=")[1];
            if(this.isGenerateLicenseFile){
              window.open(appInstance.projectConfg.baseUrl+"/getLicenseFile",'_blank');
            }else{
              this.$message({
                          message: 'License附件还未生成，请耐心等候！',
                          type: 'warning'
                 });
            }
          }
        }
    }
</script>

<style scoped>
  .downloadLayoutClass{
    display: flex;
    flex-direction: row;
    justify-content: center;
    height:30%;
  }
  .downLoadClass{
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width:580px;
  }
</style>
