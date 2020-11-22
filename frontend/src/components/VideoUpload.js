import React, { Component } from "react";
import Header from "./Header";
import { createVideo } from "../components/FetchData";


export default class VideoUpload extends Component {
  constructor(props) {
    super(props);
    //this.handleChange = this.handleChange.bind(this);
    //this.handleSubmit = this.handleSubmit.bind(this);

    this.state = {
      video_id: "",
      file: "",
      message: ""
    };
  }

  getVideoID() {
    vid = createVideo().then(
      (response) => {
        console.log(response);
        if (response.video_id) {
          return JSON.stringify(response.video_id)
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
    )
    this.setState({
      video_id = vid,
    });
    localStorage.setItem("video_id", vid);
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
            <label className="title">
              Title:
              <input
                className="title-input"
                type="text"
                name="video-title"
                placeholder="Add a title to your video"
              />
            </label>
            <label className="description">
              Description:
              <textarea
                maxLength="100"
                className="description-input"
                type="text"
                name="video-description"
                placeholder="Add a description to your video"
              />
            </label>
            <label className="tags">
              Tags:
              <input
                className="tags-input"
                type="text"
                name="video-tags"
                placeholder="(e.g. DevOps, Albert Einstein, flying pig, ...)"
              />
            </label>
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
