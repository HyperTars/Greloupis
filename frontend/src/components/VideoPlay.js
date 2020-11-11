import React, { useState, useEffect } from "react";
import { Redirect } from "react-router-dom";
import MainVideo from "./MainVideo";
import Comments from "./Comments";
import * as func from "../util";
import { getVideoInfo, getVideoComments } from "./FetchData";
import { Spin } from "antd";

const API_KEY = "?api_key=12345678";
const baseURL = "http://localhost:8080";

function VideoPlay({ videoId }) {
  const [mainVideo, setMainVideo] = useState({});
  const [videoComments, setVideoComments] = useState([]);
  const [errorMsg, setErrorMsg] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    console.log(videoId);
    getVideoInfo(videoId)
      .then((res) => {
        if (res == null) return;

        setMainVideo(res.body[0]);
        setIsLoading(false);
      })
      .catch((e) => {
        setIsLoading(false);
        setErrorMsg(e.message);
      });
  }, [videoId]);

  useEffect(() => {
    getVideoComments(videoId).then((res) => {
      if (res == null) return;
      setVideoComments(res.body);
    });
  }, [videoId]);

  const errorFormat = <Redirect to="/404"></Redirect>;
  if (errorMsg) return errorFormat;

  const likeHandler = () => {
    func.fetchRequest(
      "PUT",
      `${baseURL}/videos/${this.state.mainVideo.id}/likes${API_KEY}`
    );
    this.setState({
      mainVideo: {
        ...this.state.mainVideo,
        thumbsUp: this.state.mainVideo.thumbsUp + 1,
      },
    });
  };

  const dislikeHandler = () => {
    func.fetchRequest(
      "PUT",
      `${baseURL}/videos/${this.state.mainVideo.id}/dislikes${API_KEY}`,
      (data) => {
        console.log(data);
      }
    );
    this.setState({
      mainVideo: {
        ...this.state.mainVideo,
        thumbsDown: this.state.mainVideo.thumbsDown + 1,
      },
    });
  };

  return (
    <main>
      {isLoading ? (
        <div className="searchLoading">
          <Spin size="large" />
        </div>
      ) : null}
      {mainVideo ? (
        <section id="main-video-content">
          <MainVideo
            mainVideo={mainVideo}
            likeHandler={likeHandler}
            dislikeHandler={dislikeHandler}
            description={mainVideo.video_description}
            id={mainVideo.video_id}
          />
          <Comments comments={videoComments} mainVideoId={mainVideo.video_id} />
        </section>
      ) : null}
    </main>
  );
}

export default VideoPlay;
