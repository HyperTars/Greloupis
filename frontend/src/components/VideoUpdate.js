import React, { useState, useEffect } from "react";
import { getVideoInfo, updateVideoInfo, deleteVideo } from "./FetchData";
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
  Card,
} from "antd";

import { UploadOutlined, QuestionCircleOutlined } from "@ant-design/icons";

import { getSubstr, uuid } from "../util";

let AWS = require("aws-sdk");
let CURRENT_UUID = uuid();

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

        // set tag and catogory to string
        let tagStr = "";
        res.body.video_tag.forEach((e) => {
          tagStr += e + ",";
        });
        res.body.video_tag = tagStr === "" ? "" : tagStr.slice(0, -1);

        let categoryStr = "";
        res.body.video_category.forEach((e) => {
          categoryStr += e + ",";
        });
        res.body.video_category =
          categoryStr === "" ? "" : categoryStr.slice(0, -1);

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
      sm: { span: 6 },
    },
    wrapperCol: {
      xs: { span: 12 },
      sm: { span: 18 },
    },
  };

  const [fileList, updateFileList] = useState([]);
  const [thumbnailName, setThumbnailName] = useState("");
  const [hasThumbnail, setHasThumbnail] = useState(false);

  const VideoUpdateForm = () => {
    const [form] = Form.useForm();

    const submitHandler = (values) => {
      // tag and category to list again, trim blank space
      if (values.tag.length > 0) {
        let tagArray = [];

        values.tag.split(",").forEach((e) => {
          tagArray.push(e.trim());
        });

        values.tag = tagArray;
      }

      if (values.category.length > 0) {
        let categoryArray = [];

        values.category.split(",").forEach((e) => {
          categoryArray.push(e.trim());
        });

        values.category = categoryArray;
      }

      updateVideoInfo(videoId, {
        video_thumbnail: hasThumbnail
          ? "https://greloupis-images.s3.amazonaws.com/thumbnail-" +
            CURRENT_UUID +
            "-" +
            thumbnailName
          : videoData.video_thumbnail,
        video_title: values.title !== videoData.video_title ? values.title : "",
        video_description: values.description,
        video_channel: values.channel,
        video_tag: values.tag,
        video_category: values.category,
        video_language: values.language,
        video_status: values.status,
      }).then(() => {
        alert("Successfully update video information!");
        window.location.href =
          "/user/" + getSubstr(localStorage.getItem("user_id"));
      });
    };

    const uploadProps = {
      fileList,
      name: "file",
      listType: "picture",
      action: "https://www.mocky.io/v2/5cc8019d300000980a055e76",
      beforeUpload: (file) => {
        if (
          file.type !== "image/png" &&
          file.type !== "image/jpg" &&
          file.type !== "image/jpeg"
        ) {
          message.error(`${file.name} is not a png/jpg/jpeg file!`);
        }

        let fileObj = document.getElementById("submit_thumbnail").files[0];

        // upload to s3
        AWS.config.update({
          // accessKeyId: AWS.config.credentials.accessKeyId,
          // secretAccessKey: AWS.config.credentials.secretAccessKey,
          accessKeyId: "AKIA3OYIJQ4LRR5D4QMP",
          secretAccessKey: "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",
          region: AWS.config.region,
        });

        if (fileObj) {
          let upload = new AWS.S3.ManagedUpload({
            params: {
              Bucket: "greloupis-images",
              Key: "thumbnail-" + CURRENT_UUID + "-" + fileObj.name,
              Body: fileObj,
              ACL: "public-read",
            },
          });
          let promise = upload.promise();
          promise.then(() => {
            console.log("Successfully uploaded thumbnail");
          });
        }

        return (
          file.type === "image/png" ||
          file.type === "image/jpg" ||
          file.type === "image/jpeg"
        );
      },
      onChange: (info) => {
        info.fileList = info.fileList.slice(-1); // only submit 1 file at most
        updateFileList(info.fileList.filter((file) => !!file.status));
        setThumbnailName(info.fileList.length > 0 ? info.fileList[0].name : "");
        setHasThumbnail(info.fileList.length > 0 ? true : false);
      },
    };

    return (
      <Form
        {...formItemLayout}
        form={form}
        name="submit"
        onFinish={submitHandler}
        labelAlign="left"
        initialValues={{
          thumbnail: videoData ? videoData["video_thumbnail"] : "",
          title: videoData ? videoData["video_title"] : "",
          description: videoData ? videoData["video_description"] : "",
          channel: videoData ? videoData["video_channel"] : "",
          tag: videoData ? videoData["video_tag"] : "",
          category: videoData ? videoData["video_category"] : "",
          language: videoData ? videoData["video_language"] : "",
          status: videoData ? videoData["video_status"] : "",
        }}
      >
        <Form.Item
          id="thumbnailUpload"
          name="thumbnail"
          label={
            <span>
              Video Thumbnail&nbsp;
              <Tooltip title="Support image in .png, .jpg and .jpeg format">
                <QuestionCircleOutlined />
              </Tooltip>
            </span>
          }
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
            maxLength={1000}
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
            <Option value="Arabian">Arabian</Option>
            <Option value="English">English</Option>
            <Option value="French">French</Option>
            <Option value="German">German</Option>
            <Option value="Hindi">Hindi</Option>
            <Option value="Italian">Italian</Option>
            <Option value="Japanese">Japanese</Option>
            <Option value="Korean">Korean</Option>
            <Option value="Mandarin">Mandarin</Option>
            <Option value="Portuguese">Portuguese</Option>
            <Option value="Russian">Russian</Option>
            <Option value="Spanish">Spanish</Option>
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

        <Form.Item className="video-button-form">
          <Button
            type="primary"
            htmlType="submit"
            onSubmit={submitHandler}
            className="video-update-button"
          >
            Update Video
          </Button>
          <Button
            type="primary"
            className="deleteButton video-update-button"
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
        </Form.Item>
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
            <Card title="Video Information">
              <VideoUpdateForm></VideoUpdateForm>
            </Card>
          </div>
        </Col>
        <Col span={6}></Col>
      </Row>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default VideoUpdate;
