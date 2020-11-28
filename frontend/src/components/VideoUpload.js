import React, { Component } from "react";
import Header from "./Header";
import { createVideo, updateVideoInfo } from "./FetchData";
import { message } from "antd";

let AWS = require("aws-sdk");

export default class VideoUpload extends Component {
  constructor(props) {
    super(props);

    this.state = {
      video_id: "",
      video_raw_content: "",
      video_duration: 0,
      video_raw_size: 0,
      fileObj: "",
    };
  }

  uploadHandler = () => {
    let file = document.getElementById("submit_file").files[0];
    let temp_video_size = 0;
    let temp_video_duration = 0;

    if (
      file.type !== "video/mp4" &&
      file.type !== "video/avi" &&
      file.type !== "video/rmvb" &&
      file.type !== "video/mov"
    ) {
      alert(`${file.name} is not a .rmvb / .mp4 / .avi / .mov file!`);
      window.location.reload();
    }

    // get size
    temp_video_size = parseFloat((file.size / 1048576).toFixed(2));

    // get duration
    let test_video = document.getElementById("test_video");
    test_video.src = URL.createObjectURL(file);

    test_video.addEventListener("loadedmetadata", () => {
      temp_video_duration = parseInt(test_video.duration, 10);

      this.setState({
        fileObj: file,
        video_raw_size: temp_video_size,
        video_duration: temp_video_duration,
        video_title: "",
        video_raw_content: "",
      });
    });

    document.getElementById("submit_file").files.value = "";
  };

  submitHandler = () => {
    if (this.state.fileObj) {
      // acquire video ID
      createVideo()
        .then((res) => {
          if (res == null || res.body == null) return;
          this.setState({
            video_id: res.body.video_id,
          });
          // upload to s3
          AWS.config.update({
            // accessKeyId: AWS.config.credentials.accessKeyId,
            // secretAccessKey: AWS.config.credentials.secretAccessKey,
            accessKeyId: "AKIA4KCXIGUZXUOBYG3E",
            secretAccessKey: "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",
            region: "us-west-1",
          });
          let upload = new AWS.S3.ManagedUpload({
            params: {
              Bucket: "vod-watchfolder-ovs-lxb",
              Key: this.state.video_id + "." + this.state.fileObj.type.slice(6),
              Body: this.state.fileObj,
              ACL: "public-read",
            },
          });
          upload.promise();
          alert("Successfully uploaded video!");
          // update some system generated data, then route to update page
          let updateData = {
            video_duration: this.state.video_duration,
            video_id: this.state.video_id,
            video_raw_content:
              "https://vod-watchfolder-ovs-lxb.s3-us-west-1.amazonaws.com/" +
              this.state.video_id +
              "." +
              this.state.fileObj.type.slice(6),
            video_raw_size: this.state.video_raw_size,
            video_title: this.state.video_id,
          };
          updateVideoInfo(this.state.video_id, updateData).then(() => {
            let path = {
              pathname: `/video/update/${this.state.video_id}`,
            };
            this.props.history.push(path);
          });
        })
        .catch((e) => {
          message.error(e.message);
        });
    } else {
      message.error("You have not uploaded video!");
    }
  };

  render() {
    return (
      <div>
        <Header />
        <div className="upload">
          <form className="upload-page">
            <div className="upload-info">
              <div className="upload-info__progress">
                <div className="upload-info__progress-bar"></div>
                <div className="progress-text">
                  <p>Click "Publish" to upload your video!</p>
                </div>
              </div>
              <div className="upload-info__basicInfo">
                <h4>Video Upload</h4>
                <label className="files">
                  Upload video file: (Format supported: .mp4, .rmvb, .avi, .mov)
                  <input
                    className="files-input"
                    type="file"
                    name="video-files"
                    id="submit_file"
                    onChange={this.uploadHandler}
                  />
                </label>
                <video style={{ display: "none" }} id="test_video"></video>
              </div>
            </div>
            <div className="upload-page__btnBox">
              <button type="button" onClick={this.submitHandler}>
                Publish
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }
}
