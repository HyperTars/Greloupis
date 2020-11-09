import React, { useState, useEffect } from "react";
import { getVideoInfo } from "./FetchData";
import { Redirect } from "react-router-dom";

function VideoPlay({ videoId }) {
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);
  const [videoData, setVideoData] = useState(null);

  useEffect(() => {
    getVideoInfo(videoId)
      .then((res) => {
        if (res == null) {
          return;
        }

        setLoading(false);
        setVideoData(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [videoId]);

  const loadingFormat = (
    <div className="topMargin">
      <div>Loading......</div>
    </div>
  );

  const errorFormat = <Redirect to="/404"></Redirect>;

  const sampleFormat = (
    <div className="topMargin">
      <div>
        Video title: {!videoData ? "Loading" : videoData[0]["video_title"]}
      </div>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default VideoPlay;
