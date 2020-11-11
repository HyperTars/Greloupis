import React, { useState, useEffect } from "react";
import { Redirect } from "react-router-dom";
import MainVideo from "./MainVideo";
import Comments from "./Comments";
import * as func from "../util";
import {
  getVideoInfo,
  getVideoComments,
  getVideoLikes,
  getVideoDislikes,
  getVideoStars,
  updateVideoViews,
} from "./FetchData";
import { Spin } from "antd";

function VideoPlay({ videoId }) {
  const [mainVideo, setMainVideo] = useState({});
  const [videoComments, setVideoComments] = useState([]);
  const [videoLikes, setVideoLikes] = useState(false);
  const [videoDisLikes, setVideoDisLikes] = useState(false);
  const [videoStars, setVideoStars] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    updateVideoViews(videoId);

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

    // TODO: watching history
  }, [videoId]);

  useEffect(() => {
    getVideoComments(videoId).then((res) => {
      if (res == null) return;
      setVideoComments(res.body);
    });

    getVideoLikes(videoId).then((res) => {
      if (res == null) return;
      res.body.forEach((element) => {
        if (
          element.user_id === func.getSubstr(localStorage.getItem("user_id"))
        ) {
          setVideoLikes(true);
        }
      });
    });

    getVideoDislikes(videoId).then((res) => {
      if (res == null) return;
      res.body.forEach((element) => {
        if (
          element.user_id === func.getSubstr(localStorage.getItem("user_id"))
        ) {
          setVideoDisLikes(true);
        }
      });
    });

    getVideoStars(videoId).then((res) => {
      if (res == null) return;
      res.body.forEach((element) => {
        if (
          element.user_id === func.getSubstr(localStorage.getItem("user_id"))
        ) {
          setVideoStars(true);
        }
      });
    });
  }, [videoId]);

  const errorFormat = <Redirect to="/404"></Redirect>;
  if (errorMsg) return errorFormat;

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
            videoLike={videoLikes}
            videoDisLike={videoDisLikes}
            videoStar={videoStars}
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
