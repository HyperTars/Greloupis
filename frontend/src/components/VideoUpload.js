import React, { Component } from "react";
import Header from "./Header";
import { createVideo } from "./FetchData";

export default class VideoUpload extends Component {
  constructor(props) {
    super(props);
    //this.handleChange = this.handleChange.bind(this);
    //this.handleSubmit = this.handleSubmit.bind(this);

    this.state = {
      video_id: "",
      file: "",
      message: "",
    };
  }

  getVideoID() {
    createVideo().then(
      (response) => {
        console.log(response);
        if (response.video_id) {
          let vid = JSON.stringify(response.video_id);
          this.setState({
            video_id: vid,
          });
          localStorage.setItem("video_id", vid);
        }
      },
      (error) => {
        const resMessage =
          (error.response &&
            error.response.data &&
            error.response.data.message) ||
          error.message ||
          error.toString();

        this.setState({
          message: resMessage,
        });

        console.log(this.state);
        alert("Failed to create video. " + resMessage);
      }
    );
  }

  renderUploadFile() {
    return (
      <div className="upload-file">
        <button>Choose File</button>
      </div>
    );
  }

  render() {
    const { file } = this.state.file;
    return (
      <div>
        <Header />
        <div className="upload">
          {!file ? <UploadInfo /> : this.renderUploadFile()}
        </div>
      </div>
    );
  }
}

class UploadInfo extends Component {
  render() {
    return (
      <form className="upload-page">
        <div className="upload-info">
          <div className="upload-info__progress">
            <div className="upload-info__progress-bar"></div>
            <div className="progress-text">
              <p>Click "Publish" to make your video live!</p>
              <div>{}</div>
            </div>
          </div>
          <div className="upload-info__basicInfo">
            <h4>Video Upload</h4>
            <label className="files">
              Upload video file:
              <input className="files-input" type="file" name="video-files" />
            </label>
          </div>
        </div>
        <div className="upload-page__btnBox">
          <button type="button">Publish</button>
        </div>
      </form>
    );
  }
}
