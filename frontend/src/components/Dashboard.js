import React, { useState, useEffect } from "react";
import {
  getUserInfo,
  updateVideoViews,
  updateUserVideoProcess,
} from "./FetchData";

function Dashboard() {
  let test_user_id = "5f88f883e6ac4f89900ac983";
  let test_video_id = "5f8da0af45a235561c15910c";

  const [loading, setLoading] = useState(true);

  const [errorMsg, setErrorMsg] = useState(null);

  const [userData, setUserData] = useState(null);
  const [updateResult, setUpdateResult] = useState(null);
  const [updateProcess, setUpdateProcess] = useState(null);

  useEffect(() => {
    getUserInfo(test_user_id)
      .then((res) => {
        if (res == null) {
          return;
        }

        setLoading(false);
        setUserData(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [test_user_id]);

  useEffect(() => {
    updateVideoViews(test_video_id)
      .then((res) => {
        if (res == null) {
          return;
        }

        setUpdateResult(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [test_video_id]);

  useEffect(() => {
    updateUserVideoProcess(test_video_id, test_user_id, {
      process: parseInt(Math.random() * 1000 + 1, 10),
    })
      .then((res) => {
        if (res == null) {
          return;
        }

        setUpdateProcess(res.body);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [test_video_id, test_user_id]);

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
        User name: {!userData ? "Loading" : userData["user"][0]["user_name"]}
      </div>

      <div>
        User email: {!userData ? "Loading" : userData["user"][0]["user_email"]}
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
