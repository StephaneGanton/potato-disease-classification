<template>
  <div class="container-fluid main-container">
    <div class="row">
      <div class="col-md-4 offset-md-4">
          <div class="card" :class="[image ? 'image-card' : 'image-card-empty']">
    
            <div v-if="image" class="div-image">
                <img :src="preview" class="media" alt="img_zone">
            </div>
            <div v-else>
                <DropZone class="dropzone"
                  @addedFile = "onSelectFile"
                  :maxFiles="1"
                  :acceptedFiles="['image']"
                  :dropzoneClassName="file-input"
                />
              </div>

              <div v-if="data" class="data py-2 ">
                <div class="card">
                  <div class="card-body ">
                    <div class="card-title text-center pred-title bg-success">Prediction</div>
                    <div class="card-text detail">
                      <table class="table table-responsive text-center table-container">
                        <thead>
                          <tr class="table-row">
                            <th class="table-cell1" scope="col">Class</th>
                            <th class="table-cell" scope="col">Confidence</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>{{ data.class }}</td>
                            <td>{{ (data.confidence * 100).toFixed(2) }}%</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="isLoading" class="loader-div mt-4">
                <span>Predicting....</span>
              </div>
          </div>
      </div>
    </div>
    <div class="row">
      <div v-if="data" class="col-md-4 offset-md-4 mt-2 text-center">
        <button @click="clearData" class="btn btn-lg btn-warning"> Clear Result</button>
      </div>
    </div>
  </div>
</template>

<script>


import { DropZone } from "dropzone-vue";
import axios from "axios"
export default {
  name: 'HomeView',
  components: {
    DropZone,
  },

  data() {
    return {
      API_URL: "http://localhost:9000/predict",
      files: null,
      selectedFile: null,
      preview: null,
      data: null,
      image: false,
      isLoading: false,
      tableHeaders: [
        { text: 'Label', value: 'class' },
        { text: 'Confidence', value: 'confidence' },
      ],
    };
  },

  methods: {
    async sendFile() {
      if (this.image) {
        var formData = new FormData();
        formData.append("file", this.selectedFile);

        try {
          let res = await axios.post(this.API_URL, formData);
          if (res.status === 200) {
            this.data = res.data;
          }
        } catch (error) {
          console.error(error);
        }
        this.isLoading = false;
      }
    },
    clearData() {
      this.data = null;
      this.image = false;
      this.selectedFile = null;
      this.preview = null;
    },
    onSelectFile(files) {
      if (!files || files.length === 0) {
        this.selectedFile = null;
        this.image = false;
        this.data = null;
        return;
      }
      this.selectedFile = files.file;
      this.files = files
      //console.log("selectedFile... :", this.selectedFile);
      this.data = null;
      this.image = true;
    },

    updatePreview() {
      if (!this.selectedFile) {
        this.preview = undefined;
        return;
      }
      
      this.preview = URL.createObjectURL(this.selectedFile);
      this.isLoading = true;
      this.sendFile();
    },
  },
  watch: {
    selectedFile: 'updatePreview',
  },
  created() {
    this.updatePreview();
  },
  
}
</script>


<style scoped>


.main-container {
  background-image: url("@/assets/bg.png");
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  height: 90vh;
  margin-top: 8px;
}
.image-card {
  margin: auto;
  margin-top: 5vh;
  max-width: 400px;
  height: 500px;
  background-color: transparent;
  box-shadow: 0px 9px 70px 0px rgba(0, 0, 0, 0.3) !important;
  border-radius: 15px;
}
.image-card-empty {
  top: 25vh;
  position: relative;
  /*width: 200px;;*/
  height: 200px;
  background-color: white;
  text-align: center;
  padding: 10px;
}
.dropzone{
  position: absolute;
  background-color: whitesmoke;
  opacity: .2;
  border: 6px black dashed;
  width: 95%;
  height:90%;
  padding-top: 18%;
  content: "";
  /*padding-bottom: 15%;*/
}

.div-image{
  width: auto;
  height: 69%;
}

.div-image .media{
  width: 100%;
  height: 100%;
}

.pred-title{
  color: yellow;
  
  font-size: 18px;
  padding-bottom: 0;
  margin-bottom: 0px;
}

.data{
  margin-top: -10px;
}

.table-container {
  background-color: transparent !important;
  box-shadow: none !important;
}
.table {
  background-color: transparent !important;
}
.table-head {
  background-color: transparent !important;
}
.table-row {
  background-color: transparent !important;
}
.table-cell1 {
  font-size: 18px;
  background-color: transparent !important;
  border-color: transparent !important;
  color: #000000a6 !important;
  font-weight: bolder;
  padding: 1px 0px 1px 16px;
}
.detail {
  
  background-color: white;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}
.loader {
  color: #be6a77 !important;
}
</style>

