import React, { useState, useEffect } from "react";
import {
  getUserInfo,
  searchVideo,
  updateVideoViews,
  updateUserVideoProcess,
} from "./FetchData";

function Dashboard({ endpoint }) {
  let test_user_id = "5f88f883e6ac4f89900ac983";
  let test_keyword = "ih";
  let test_video_id = "5f8da0af45a235561c15910c";

  const [loading, setLoading] = useState(true);

  const [errorMsg, setErrorMsg] = useState(null);

  const [userData, setUserData] = useState(null);
  const [searchResult, setSearchResult] = useState(null);
  const [updateResult, setUpdateResult] = useState(null);
  const [updateProcess, setUpdateProcess] = useState(null);

  useEffect(() => {
    getUserInfo(endpoint, test_user_id)
      .then((res) => {
        if (res == null) {
          return;
        }

        console.log(res);
        setLoading(false);
        setUserData(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [endpoint, test_user_id]);

  useEffect(() => {
    searchVideo(endpoint, test_keyword)
      .then((res) => {
        if (res == null) {
          return;
        }

        console.log(res);
        setSearchResult(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [endpoint, test_keyword]);

  useEffect(() => {
    updateVideoViews(endpoint, test_video_id)
      .then((res) => {
        if (res == null) {
          return;
        }

        console.log(res);
        setUpdateResult(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [endpoint, test_video_id]);

  useEffect(() => {
    updateUserVideoProcess(endpoint, test_video_id, test_user_id, {
      process: parseInt(Math.random() * 1000 + 1, 10),
    })
      .then((res) => {
        if (res == null) {
          return;
        }

        console.log(res);
        setUpdateProcess(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [endpoint, test_video_id, test_user_id]);

  const loadingFormat = (
    <div>
      <div>Loading......</div>
    </div>
  );

  const errorFormat = (
    <div>
      <div>Error: {errorMsg}</div>
    </div>
  );

  const sampleFormat = (
    <div>
      <div>
        User name: {!userData ? "Loading" : userData["user"][0]["user_name"]}
      </div>

      <div>
        User email: {!userData ? "Loading" : userData["user"][0]["user_email"]}
      </div>

      <div>
        Search video title:{" "}
        {!searchResult ? "Loading" : searchResult[0]["video_title"]}
      </div>

      <div>
        Update video view result:{" "}
        {!updateResult ? "Loading" : updateResult["view_count"]}
      </div>

      <div>
        Update video process result:{" "}
        {!updateProcess ? "Loading" : updateProcess["process"]}
      </div>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default Dashboard;
