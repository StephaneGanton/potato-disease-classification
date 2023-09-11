<template>
  <div>
    <v-app-bar app color="#be6a77" dark>
      <v-toolbar-title>CodeBasics: Potato Disease Classification</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-avatar>
        <img src="@/assets/cblogo.PNG" alt="CodeBasics Logo" />
      </v-avatar>
    </v-app-bar>

    <v-container fluid class="main-container">
      <v-row class="grid-container" justify="center">
        <v-col cols="12">
          <v-card :class="[image ? 'image-card' : 'image-card-empty']">
            <v-card-text>
              <div v-if="image">
                <v-img :src="preview" class="media" />
              </div>
              <div v-else>
                <v-dropzone
                  acceptedFiles="image/*"
                  dropzoneText="Drag and drop an image of a potato plant leaf to process"
                  @vdropzone-file="onSelectFile()"
                ></v-dropzone>
              </div>
              <div v-if="data">
                <v-card>
                  <v-card-text class="detail">
                    <v-data-table
                      :items="[data]"
                      :headers="tableHeaders"
                      hide-actions
                      class="table-container"
                    >
                      <template v-slot:items="props">
                        <tr class="table-row">
                          <td class="table-cell1">{{ props.item.class }}</td>
                          <td class="table-cell1">{{ (props.item.confidence * 100).toFixed(2) }}%</td>
                        </tr>
                      </template>
                    </v-data-table>
                  </v-card-text>
                </v-card>
              </div>
              <div v-if="isLoading">
                <v-card class="detail">
                  <v-card-text>
                    <v-progress-circular
                      :color="'#be6a77'"
                      :indeterminate="true"
                      class="loader"
                    ></v-progress-circular>
                    <v-divider></v-divider>
                    <v-subheader>Processing</v-subheader>
                  </v-card-text>
                </v-card>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col class="button-grid" v-if="data">
          <v-btn @click="clearData" color="primary" dark>
            <v-icon left>mdi-close</v-icon> Clear
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
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
        let formData = new FormData();
        formData.append('file', this.selectedFile);
        try {
          let res = await axios.post(process.env.VUE_APP_API_URL, formData);
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
      console.log(files);
      if (!files || files.length === 0) {
        this.selectedFile = null;
        this.image = false;
        this.data = null;
        return;
      }
      this.selectedFile = files[0];
      this.data = null;
      this.image = true;
    },
  },
  watch: {
    selectedFile: 'updatePreview',
  },
  created() {
    this.updatePreview();
  },
  methods: {
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
};
</script>

<style scoped>
.main-container {
  background-image: url("@/assets/bg.png");
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  height: 93vh;
  margin-top: 8px;
}
.image-card {
  margin: auto;
  max-width: 400px;
  height: 500px;
  background-color: transparent;
  box-shadow: 0px 9px 70px 0px rgba(0, 0, 0, 0.3) !important;
  border-radius: 15px;
}
.image-card-empty {
  height: auto;
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
  font-size: 14px;
  background-color: transparent !important;
  border-color: transparent !important;
  color: #000000a6 !important;
  font-weight: bolder;
  padding: 1px 24px 1px 16px;
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
