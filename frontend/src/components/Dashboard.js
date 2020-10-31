import React, { useState, useEffect } from "react";
import { getUserInfoById, searchVideoByKeyword } from "./FetchData";

function Dashboard({ endpoint }) {
  let test_user_id = "5f88f883e6ac4f89900ac983";
  let test_keyword = "ih";

  const [loading, setLoading] = useState(true);

  const [errorMsg, setErrorMsg] = useState(null);

  const [userData, setUserData] = useState(null);
  const [searchResult, setSearchResult] = useState(null);

  useEffect(() => {
    getUserInfoById(endpoint, test_user_id)
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
    searchVideoByKeyword(endpoint, test_keyword)
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
      <div>"Hello world"</div>

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
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default Dashboard;
