import React, { useState, useEffect } from "react";
import { searchTopVideo } from "./FetchData";
import { Spin, List, Space, Card } from "antd";
import { Link } from "react-router-dom";
import ErrorPage from "./ErrorPage";
import {
  EyeOutlined,
  LikeOutlined,
  StarOutlined,
  FieldTimeOutlined,
  CalendarOutlined,
  UserOutlined,
} from "@ant-design/icons";
import {
  secondTimeConvert,
  dateConvert,
  ellipsifyStr,
  generateThumbnail,
} from "../util";

function Home() {
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);
  const [errorCode, setErrorCode] = useState(null);
  const [videoResult, setVideoResult] = useState(null);

  useEffect(() => {
    searchTopVideo("video_view")
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
        setVideoResult(
          videoArray.length > 10 ? videoArray.slice(0, 10) : videoArray
        );
      })
      .catch((e) => {
        setLoading(false);
        setErrorCode(e.message.slice(0, 3));
        setErrorMsg(e.message.slice(3));
      });
  }, []);

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

  const errorFormat = <ErrorPage errCode={errorCode}></ErrorPage>;

  const sampleFormat = (
    <div className="topMargin">
      <div className="searchPart">
        <Card title="Top 10 Hit Videos">
          {videoResult == null ? (
            <Spin />
          ) : (
            <List
              itemLayout="vertical"
              size="large"
              pagination={{
                hideOnSinglePage: true,
              }}
              dataSource={videoResult}
              renderItem={(item) => (
                <List.Item
                  actions={[
                    <IconText
                      icon={UserOutlined}
                      text={
                        <Link to={"/user/" + item.user_id}>
                          {item.user_name}
                        </Link>
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
                      <img
                        width={160}
                        alt="logo"
                        src={generateThumbnail(item.video_thumbnail)}
                      />
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
        </Card>
      </div>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default Home;
