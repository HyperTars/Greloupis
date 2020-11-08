import React, { useState, useEffect } from "react";
import { searchUser, searchVideo } from "./FetchData";
import { Spin, List, Avatar } from "antd";

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
        if (res == null || res.body == null) {
          return;
        }

        let userArray = [];
        res.body.forEach((element) => {
          userArray.push({
            user_name: element.user_name,
            user_thumbnail: element.user_thumbnail,
          });
        });

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

  const data = [
    {
      title: "Ant Design Title 1",
    },
    {
      title: "Ant Design Title 2",
    },
    {
      title: "Ant Design Title 3",
    },
    {
      title: "Ant Design Title 4",
    },
  ];

  const loadingFormat = (
    <div className="searchLoading">
      <Spin size="large" />
    </div>
  );

  const errorFormat = (
    <div className="topMargin">
      <div>Error: {errorMsg}</div>
    </div>
  );

  const sampleFormat = (
    <div className="topMargin">
      <h3>{"Matched Videos: "}</h3>

      <List
        itemLayout="horizontal"
        dataSource={data}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta
              avatar={
                <Avatar src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />
              }
              title={<a href="https://ant.design">{item.title}</a>}
              description="Ant Design, a design language for background applications, is refined by Ant UED Team"
            />
          </List.Item>
        )}
      />

      <h3>{"Matched Users: "}</h3>

      <List
        itemLayout="horizontal"
        dataSource={data}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta
              avatar={
                <Avatar src="https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png" />
              }
              title={<a href="https://ant.design">{item.title}</a>}
              description="Ant Design, a design language for background applications, is refined by Ant UED Team"
            />
          </List.Item>
        )}
      />

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
