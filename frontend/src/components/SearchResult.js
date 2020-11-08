import React, { useState, useEffect } from "react";
import { searchUser, searchVideo } from "./FetchData";

function SearchResult() {
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);
  const [userResult, setUserResult] = useState(null);
  const [videoResult, setVideoResult] = useState(null);

  let keyword =
    window.location.search.substring(1) &&
    window.location.search.substring(1).split("=").length > 1
      ? window.location.search.substring(1).split("=")[1]
      : "";

  useEffect(() => {
    searchUser(keyword)
      .then((res) => {
        if (res == null) {
          return;
        }
        setLoading(false);
        setUserResult(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [keyword]);

  useEffect(() => {
    searchVideo(keyword)
      .then((res) => {
        if (res == null) {
          return;
        }
        setLoading(false);
        setVideoResult(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [keyword]);

  const loadingFormat = (
    <div className="topMargin">
      <div>Loading......</div>
    </div>
  );

  const errorFormat = (
    <div className="topMargin">
      <div>Error: {errorMsg}</div>
    </div>
  );

  const sampleFormat = (
    <div className="topMargin">
      <div>
        Search user title:{" "}
        {!userResult
          ? "Loading"
          : userResult.length === 0
          ? "No matched result"
          : userResult[0]["user_name"]}
      </div>

      <div>
        Search video title:{" "}
        {!videoResult
          ? "Loading"
          : videoResult.length === 0
          ? "No matched result"
          : videoResult[0]["video_title"]}
      </div>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default SearchResult;
