import React, { useState, useEffect } from "react";
import { getUserInfo } from "./FetchData";
import { Redirect } from "react-router-dom";

function UserProfile({ userId }) {
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    getUserInfo(userId)
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
  }, [userId]);

  const loadingFormat = (
    <div className="topMargin">
      <div>Loading......</div>
    </div>
  );

  const errorFormat = <Redirect to="/404"></Redirect>;

  const sampleFormat = (
    <div className="topMargin">
      <div>
        User name: {!userData ? "Loading" : userData["user"][0]["user_name"]}
      </div>

      <div>
        User email: {!userData ? "Loading" : userData["user"][0]["user_email"]}
      </div>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default UserProfile;
