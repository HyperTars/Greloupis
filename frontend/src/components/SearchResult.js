import React, { useState, useEffect } from "react";
import { searchUser, searchVideo } from "./FetchData";
import { Spin, List, Avatar, Space } from "antd";
import { Link } from "react-router-dom";
import {
  EyeOutlined,
  LikeOutlined,
  StarOutlined,
  FieldTimeOutlined,
  CalendarOutlined,
  UserOutlined,
} from "@ant-design/icons";
import { secondTimeConvert, dateConvert, ellipsifyStr } from "../util";

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
            user_id: element.user_id,
            user_name: element.user_name,
            user_thumbnail: element.user_thumbnail,
          });
        });

        setLoading(false);
        setUserResult(userArray);
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

        let videoArray = [];
        res.body.forEach((element) => {
          videoArray.push({
            user_id: element.user_id,
            user_name: element.user_name,
            video_id: element.video_id,
            video_title: element.video_title,
            video_raw_content: element.video_raw_content,
            video_thumbnail: element.video_thumbnail,
            video_duration: element.video_duration,
            video_description: element.video_description,
            video_upload_date: element.video_upload_date,
            video_view: element.video_view,
            video_like: element.video_like,
            video_star: element.video_star,
            video_comment: element.video_comment,
          });
        });

        setLoading(false);
        setVideoResult(videoArray);
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [keyword]);

  const IconText = ({ icon, text }) => (
    <Space>
      {React.createElement(icon)}
      {text}
    </Space>
  );

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
      <div className="searchPart">
        <h4>{"Matched Videos: "}</h4>

        {videoResult == null ? (
          <Spin />
        ) : (
          <List
            itemLayout="vertical"
            size="large"
            pagination={{
              pageSize: 3,
            }}
            dataSource={videoResult}
            renderItem={(item) => (
              <List.Item
                actions={[
                  <IconText
                    icon={UserOutlined}
                    text={
                      <Link to={"/user/" + item.user_id}>{item.user_name}</Link>
                    }
                    key="list-vertical-user-o"
                  />,
                  <IconText
                    icon={EyeOutlined}
                    text={item.video_view}
                    key="list-vertical-view-o"
                  />,
                  <IconText
                    icon={StarOutlined}
                    text={item.video_star}
                    key="list-vertical-star-o"
                  />,
                  <IconText
                    icon={LikeOutlined}
                    text={item.video_like}
                    key="list-vertical-like-o"
                  />,

                  <IconText
                    icon={CalendarOutlined}
                    text={dateConvert(item.video_upload_date)}
                    key="list-vertical-date"
                  />,
                  <IconText
                    icon={FieldTimeOutlined}
                    text={secondTimeConvert(item.video_duration)}
                    key="list-vertical-time"
                  />,
                ]}
                extra={
                  <Link to={"/video/" + item.video_id}>
                    <img width={160} alt="logo" src={item.video_thumbnail} />
                  </Link>
                }
              >
                <List.Item.Meta
                  title={
                    <Link to={"/video/" + item.video_id}>
                      {item.video_title}
                    </Link>
                  }
                  description={
                    item.video_description !== "" ? (
                      ellipsifyStr(item.video_description)
                    ) : (
                      <br />
                    )
                  }
                />
                {item.content}
              </List.Item>
            )}
          />
        )}
      </div>

      <div className="searchPart">
        <h4>{"Matched Users: "}</h4>

        {userResult == null ? (
          <Spin />
        ) : (
          <List
            grid={{ gutter: 24, column: 3 }}
            itemLayout="horizontal"
            dataSource={userResult}
            renderItem={(item) => (
              <List.Item>
                <List.Item.Meta
                  avatar={
                    <Link to={"/user/" + item.user_id}>
                      <Avatar src={item.user_thumbnail} />
                    </Link>
                  }
                  title={
                    <Link to={"/user/" + item.user_id}>{item.user_name}</Link>
                  }
                />
              </List.Item>
            )}
          />
        )}
      </div>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default SearchResult;
