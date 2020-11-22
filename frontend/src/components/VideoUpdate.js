import React, { useState, useEffect } from "react";
import { getVideoInfo, deleteVideo } from "./FetchData";
import { Redirect } from "react-router-dom";
import "../static/css/App.css";

import {
  Form,
  Input,
  Tooltip,
  Row,
  Col,
  Select,
  Button,
  Spin,
  Upload,
  message,
} from "antd";

import { UploadOutlined, QuestionCircleOutlined } from "@ant-design/icons";

import { getSubstr } from "../util";

function VideoUpdate({ videoId }) {
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);
  const [videoData, setVideoData] = useState({});

  useEffect(() => {
    // unlogged in users try to update the video
    if (!localStorage.getItem("user_id")) {
      window.location.href = "/login";
      return;
    }

    getVideoInfo(videoId)
      .then((res) => {
        if (res == null) {
          return;
        }

        // other logged in users try to update the video
        if (res.body.user_id !== getSubstr(localStorage.getItem("user_id"))) {
          alert("Incorrect User!");
          window.location.href = "/";
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

  const { Option } = Select;

  const formItemLayout = {
    labelCol: {
      xs: { span: 6 },
      sm: { span: 4 },
    },
    wrapperCol: {
      xs: { span: 12 },
      sm: { span: 20 },
    },
  };
  const tailFormItemLayout = {
    wrapperCol: {
      xs: {
        span: 24,
        offset: 0,
      },
      sm: {
        span: 16,
        offset: 0,
      },
    },
  };

  const [fileList, updateFileList] = useState([]);
  const uploadProps = {
    fileList,
    name: "file",
    action: "https://www.mocky.io/v2/5cc8019d300000980a055e76",
    headers: {
      authorization: "authorization-text",
    },
    beforeUpload: (file) => {
      if (file.type !== "image/png") {
        message.error(`${file.name} is not a png file`);
      }
      return file.type === "image/png";
    },
    onChange: (info) => {
      // file.status is empty when beforeUpload return false
      updateFileList(info.fileList.filter((file) => !!file.status));
    },
  };

  const VideoUpdateForm = () => {
    const [form] = Form.useForm();

    const onFinish = (values) => {
      console.log("Received values of form: ", values);
    };

    return (
      <Form
        {...formItemLayout}
        form={form}
        name="submit"
        onFinish={onFinish}
        labelAlign="left"
        initialValues={{
          prefix: "1",
        }}
        scrollToFirstError
      >
        <Form.Item
          name="thumbnail"
          label="Video Thumbnail"
          rules={[{ message: "Please upload your video thumbnail!" }]}
        >
          <Upload {...uploadProps}>
            <Button icon={<UploadOutlined />}>Click to Upload</Button>
          </Upload>
        </Form.Item>

        <Form.Item
          name="title"
          label="Video Title"
          rules={[
            {
              message: "Please input your video title!",
              whitespace: true,
            },
          ]}
        >
          <Input
            placeholder="Input your video title: "
            defaultValue={videoData ? videoData["video_title"] : ""}
          />
        </Form.Item>

        <Form.Item name="description" label="Video Description">
          <Input.TextArea
            placeholder="Input your video description: "
            defaultValue={videoData ? videoData["video_description"] : ""}
          />
        </Form.Item>

        <Form.Item
          name="channel"
          label={
            <span>
              Video Channel&nbsp;
              <Tooltip title="Your video channel">
                <QuestionCircleOutlined />
              </Tooltip>
            </span>
          }
          rules={[{ message: "Please input your video channel!" }]}
        >
          <Input
            placeholder="Input your video channel: "
            defaultValue={videoData ? videoData["video_channel"] : ""}
          />
        </Form.Item>

        <Form.Item
          name="tag"
          label={
            <span>
              Video Tag&nbsp;
              <Tooltip title="Input multiple tags, separated by ','">
                <QuestionCircleOutlined />
              </Tooltip>
            </span>
          }
          rules={[{ message: "Please input your video tag!" }]}
        >
          <Input
            placeholder="Input your video tag: "
            defaultValue={videoData ? videoData["video_tag"] : ""}
          />
        </Form.Item>

        <Form.Item
          name="category"
          label={
            <span>
              Video Category&nbsp;
              <Tooltip title="Input multiple categories, separated by ','">
                <QuestionCircleOutlined />
              </Tooltip>
            </span>
          }
          rules={[{ message: "Please input your video category!" }]}
        >
          <Input
            placeholder="Input your video category: "
            defaultValue={videoData ? videoData["video_category"] : ""}
          />
        </Form.Item>

        <Form.Item
          name="language"
          label="Video Language"
          rules={[{ message: "Please input your video language!" }]}
        >
          <Select defaultValue={videoData ? videoData["video_language"] : ""}>
            <Option value="English">English</Option>
            <Option value="Mandarin">Mandarin</Option>
            <Option value="French">French</Option>
            <Option value="German">German</Option>
            <Option value="Hindi">Hindi</Option>
            <Option value="Japanese">Japanese</Option>
            <Option value="Korean">Korean</Option>
            <Option value="Other">Other</Option>
          </Select>
        </Form.Item>

        <Form.Item
          name="status"
          label={
            <span>
              Video Status&nbsp;
              <Tooltip title="Only you can see this video, if the status is set as 'private'">
                <QuestionCircleOutlined />
              </Tooltip>
            </span>
          }
          rules={[{ message: "Please input your video status!" }]}
        >
          <Select defaultValue={videoData ? videoData["video_status"] : ""}>
            <Option value="public">public</Option>
            <Option value="private">private</Option>
          </Select>
        </Form.Item>

        <Form.Item {...tailFormItemLayout}>
          <Button type="primary" htmlType="submit">
            Update Video
          </Button>
        </Form.Item>

        <Button
          type="primary"
          htmlType="submit"
          className="deleteButton"
          onClick={() => {
            deleteVideo(videoId).then(() => {
              alert("Video deleted!");
              window.location.href =
                "/user/" + getSubstr(localStorage.getItem("user_id"));
            });
          }}
        >
          Delete Video
        </Button>
      </Form>
    );
  };

  const loadingFormat = (
    <div className="searchLoading">
      <Spin size="large" />
    </div>
  );

  const errorFormat = <Redirect to="/404"></Redirect>;

  const sampleFormat = (
    <div className="videoUpdate">
      <Row gutter={12}>
        <Col span={6}></Col>
        <Col span={12}>
          <div className="VideoUpdate">
            <h4>{"Video Information: "}</h4>
            <VideoUpdateForm></VideoUpdateForm>
          </div>
        </Col>
        <Col span={6}></Col>
      </Row>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default VideoUpdate;
