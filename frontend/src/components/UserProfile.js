import React, { useState, useEffect } from "react";
import { getUserInfo, updateUserInfo, deleteUser } from "./FetchData";
import { Redirect, Link } from "react-router-dom";
import Grid from "@material-ui/core/Grid";

import {
  Form,
  Input,
  Tooltip,
  Row,
  Col,
  Select,
  Button,
  Spin,
  List,
  Avatar,
  Space,
  Upload,
  message,
  Card,
  Badge,
  Popconfirm,
} from "antd";

import {
  EyeOutlined,
  LikeOutlined,
  StarOutlined,
  FieldTimeOutlined,
  CalendarOutlined,
  QuestionCircleOutlined,
  UploadOutlined,
} from "@ant-design/icons";

import {
  getSubstr,
  secondTimeConvert,
  dateConvert,
  ellipsifyStr,
  generateThumbnail,
  uuid,
} from "../util";
import logout from "./Logout";

let AWS = require("aws-sdk");
let CURRENT_UUID = uuid();

function UserProfile({ userId }) {
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);
  const [userData, setUserData] = useState([]);

  const [videoData, setVideoData] = useState([]);

  const [userLike, setUserLike] = useState([]);
  const [userStar, setUserStar] = useState([]);
  const [userComment, setUserComment] = useState([]);
  const [userProcess, setUserProcess] = useState([]);

  // is current user the logged in user stored in local browser
  const isLocalUser = userId === getSubstr(localStorage.getItem("user_id"));

  useEffect(() => {
    getUserInfo(userId)
      .then((res) => {
        if (res == null) {
          return;
        }

        setLoading(false);
        setUserData(res.body["user"]);

        let videoList = res.body["video"];
        let likeList = res.body["video_op"].filter(
          (element) => element.like === true
        );
        let starList = res.body["video_op"].filter(
          (element) => element.star === true
        );
        let processList = res.body["video_op"].filter(
          (element) => element.process > 0
        );
        let commentList = res.body["video_op"].filter(
          (element) => element.comment !== ""
        );

        videoList.sort((a, b) => {
          let dataA = new Date(a.video_upload_date);
          let dataB = new Date(b.video_upload_date);
          if (dataA === dataB) return 0;
          return dataA > dataB ? -1 : 1;
        });

        likeList.sort((a, b) => {
          let dataA = new Date(a.like_date);
          let dataB = new Date(b.like_date);
          if (dataA === dataB) return 0;
          return dataA > dataB ? -1 : 1;
        });

        starList.sort((a, b) => {
          let dataA = new Date(a.star_date);
          let dataB = new Date(b.star_date);
          if (dataA === dataB) return 0;
          return dataA > dataB ? -1 : 1;
        });

        processList.sort((a, b) => {
          let dataA = new Date(a.process_date);
          let dataB = new Date(b.process_date);
          if (dataA === dataB) return 0;
          return dataA > dataB ? -1 : 1;
        });

        commentList.sort((a, b) => {
          let dataA = new Date(a.comment_date);
          let dataB = new Date(b.comment_date);
          if (dataA === dataB) return 0;
          return dataA > dataB ? -1 : 1;
        });

        if (JSON.stringify(res.body["video"]) !== "[{}]")
          setVideoData(videoList);
        if (JSON.stringify(res.body["video_op"]) !== "[{}]") {
          setUserLike(likeList);
          setUserStar(starList);
          setUserProcess(processList);
          setUserComment(commentList);
        }
      })
      .catch((e) => {
        setLoading(false);
        setErrorMsg(e.message);
      });
  }, [userId]);

  const { Option } = Select;

  const formItemLayout = {
    labelCol: {
      xs: { span: 8 },
      sm: { span: 8 },
    },
    wrapperCol: {
      xs: { span: 18 },
      sm: { span: 24 },
    },
  };

  const deleteUserHandler = () => {
    deleteUser(userId).then(() => {
      alert("Account deleted!");
      logout();
      window.location.href = "/";
    });
  };

  const [fileList, updateFileList] = useState([]);
  const [thumbnailName, setThumbnailName] = useState("");
  const [hasThumbnail, setHasThumbnail] = useState(false);

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

      let fileObj = document.getElementById("submit_avatar").files[0];

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
            Key: "avatar-" + CURRENT_UUID + "-" + fileObj.name,
            Body: fileObj,
            ACL: "public-read",
          },
        });
        let promise = upload.promise();
        promise.then(() => {
          console.log("Successfully uploaded avatar");
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

  const RegistrationForm = () => {
    const [form] = Form.useForm();

    const submitHandler = (values) => {
      let dataObj = {
        user_thumbnail: hasThumbnail
          ? "https://greloupis-images.s3.amazonaws.com/avatar-" +
            CURRENT_UUID +
            "-" +
            thumbnailName
          : userData.user_thumbnail,
        user_first_name: values.first_name,
        user_last_name: values.last_name,
        user_phone: values.phone,
        user_street1: values.street1,
        user_street2: values.street2,
        user_city: values.city,
        user_state: values.state,
        user_country: values.country,
        user_zip: values.zip,
        user_status: values.status,
      };

      if (userData.user_name !== values.nickname)
        dataObj["user_name"] = values.nickname;
      if (userData.user_email !== values.email)
        dataObj["user_email"] = values.email;
      if (values.password !== "") dataObj["user_password"] = values.password;

      updateUserInfo(userId, dataObj)
        .then(() => {
          if (dataObj["user_thumbnail"] !== userData.user_thumbnail) {
            localStorage.setItem(
              "user_thumbnail",
              '"' + dataObj["user_thumbnail"] + '"'
            );
          }

          alert("Successfully update user profile!");
          window.location.reload();
        })
        .catch((e) => {
          message.error(e.message);
        });
    };

    return (
      <Form
        {...formItemLayout}
        form={form}
        name="submit"
        onFinish={submitHandler}
        labelAlign="left"
        layout={isLocalUser ? "vertical" : "horizontal"}
        initialValues={{
          avatar: userData ? userData["user_thumbnail"] : "",
          nickname: userData ? userData["user_name"] : "",
          email: userData ? userData["user_email"] : "",
          password: "",
          first_name: userData["user_detail"]
            ? userData["user_detail"]["user_first_name"]
            : "",
          last_name: userData["user_detail"]
            ? userData["user_detail"]["user_last_name"]
            : "",
          phone: userData["user_detail"]
            ? userData["user_detail"]["user_phone"]
            : "",
          street1: userData["user_detail"]
            ? userData["user_detail"]["user_street1"]
            : "",
          street2: userData["user_detail"]
            ? userData["user_detail"]["user_street2"]
            : "",
          city: userData["user_detail"]
            ? userData["user_detail"]["user_city"]
            : "",
          state: userData["user_detail"]
            ? userData["user_detail"]["user_state"]
            : "",
          country: userData["user_detail"]
            ? userData["user_detail"]["user_country"]
            : "",
          zip: userData["user_detail"]
            ? userData["user_detail"]["user_zip"]
            : "",
          status: userData ? userData["user_status"] : "",
        }}
        scrollToFirstError
      >
        <Form.Item
          name="avatar"
          label={
            <span>
              Avatar&nbsp;
              <Tooltip title="Support image in .png, .jpg and .jpeg format">
                <QuestionCircleOutlined />
              </Tooltip>
            </span>
          }
          rules={[{ message: "Please upload your avatar!" }]}
        >
          {isLocalUser ? (
            <Upload {...uploadProps}>
              <Button icon={<UploadOutlined />}>Click to Upload</Button>
            </Upload>
          ) : (
            <Avatar src={userData ? userData["user_thumbnail"] : ""} />
          )}
        </Form.Item>

        <Form.Item
          name="nickname"
          label={
            <span>
              Name&nbsp;
              <Tooltip title="Your nickname on Greloupis">
                <QuestionCircleOutlined />
              </Tooltip>
            </span>
          }
          rules={[
            {
              message: "Please input your user name!",
              whitespace: true,
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your nickname: "
              defaultValue={userData ? userData["user_name"] : ""}
            />
          ) : (
            <Input
              defaultValue={userData ? userData["user_name"] : ""}
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="email"
          label="Email"
          rules={[
            {
              type: "email",
              message: "The input is not valid E-mail!",
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your email address: "
              defaultValue={userData ? userData["user_email"] : ""}
            />
          ) : (
            <Input
              defaultValue={userData ? userData["user_email"] : ""}
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        {isLocalUser ? (
          <Form.Item
            name="password"
            label="New Password"
            rules={[
              {
                message: "Please input your password!",
              },
            ]}
          >
            <Input.Password placeholder="Input your new password: " />
          </Form.Item>
        ) : (
          <div></div>
        )}

        <Form.Item
          name="first_name"
          label="First Name"
          rules={[
            {
              message: "Please input your first name!",
              whitespace: true,
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your first name: "
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_first_name"]
                  : ""
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_first_name"]
                  : ""
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="last_name"
          label="Last Name"
          rules={[
            {
              message: "Please input your last name!",
              whitespace: true,
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your last name: "
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_last_name"]
                  : ""
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_last_name"]
                  : ""
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="phone"
          label="Phone"
          rules={[{ message: "Please input your phone number!" }]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your phone number: "
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_phone"]
                  : ""
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_phone"]
                  : ""
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="street1"
          label="Street 1"
          rules={[
            {
              message: "Please input your user street 1!",
              whitespace: true,
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your Street address or P.O. Box: "
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_street1"]
                  : ""
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_street1"]
                  : ""
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="street2"
          label="Street 2"
          rules={[
            {
              message: "Please input your user street 2!",
              whitespace: true,
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your Apt, suite, unit, building, floor, etc.: "
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_street2"]
                  : ""
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_street2"]
                  : ""
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="city"
          label="City"
          rules={[
            {
              message: "Please input your user city!",
              whitespace: true,
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your city name: "
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_city"]
                  : ""
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_city"]
                  : ""
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="state"
          label="State"
          rules={[
            {
              message: "Please input your user state!",
              whitespace: true,
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your state name: "
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_state"]
                  : ""
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_state"]
                  : ""
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="country"
          label="Country"
          rules={[
            {
              message: "Please input your user country!",
              whitespace: true,
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your country name: "
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_country"]
                  : ""
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_country"]
                  : ""
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="zip"
          label="Zip"
          rules={[
            {
              message: "Please input your user zip!",
              whitespace: true,
            },
          ]}
        >
          {isLocalUser ? (
            <Input
              placeholder="Input your zip code: "
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_zip"]
                  : ""
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_zip"]
                  : ""
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="status"
          label={
            <span>
              Status&nbsp;
              <Tooltip title="Other users can only see user avatar, name and public videos, if the status is set as 'private'">
                <QuestionCircleOutlined />
              </Tooltip>
            </span>
          }
          rules={[{ message: "Please select your status!" }]}
        >
          {isLocalUser ? (
            <Select
              placeholder="Select your user status: "
              defaultValue={userData ? userData["user_status"] : ""}
            >
              <Option value="public">public</Option>
              <Option value="private">private</Option>
            </Select>
          ) : (
            <Input
              defaultValue={userData ? userData["user_status"] : ""}
              style={{ width: "100%" }}
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        {isLocalUser ? (
          <div>
            <Form.Item className="profile-button-form">
              <Button
                type="primary"
                htmlType="submit"
                className="profile-button"
              >
                Update Profiles
              </Button>

              <Popconfirm
                title="Are you sure to delete the account?"
                onConfirm={deleteUserHandler}
                onCancel={() => {}}
                okText="Yes"
                cancelText="No"
              >
                <Button type="primary" className="deleteButton profile-button">
                  Delete Account
                </Button>
              </Popconfirm>
            </Form.Item>
          </div>
        ) : (
          <div></div>
        )}
      </Form>
    );
  };

  const loadingFormat = (
    <div className="searchLoading">
      <Spin size="large" />
    </div>
  );

  const errorFormat = <Redirect to="/404"></Redirect>;

  const IconText = ({ icon, text }) => (
    <Space>
      {React.createElement(icon)}
      {text}
    </Space>
  );

  const sampleFormat = (
    <div className="topMargin">
      <Row gutter={0}>
        <Col span={8}>
          <div className="userProfile">
            <Card title={isLocalUser ? "My Profiles" : "User Profiles"}>
              <RegistrationForm></RegistrationForm>
            </Card>
          </div>
        </Col>

        <Col span={16}>
          <div className="userProfile">
            <Card title={isLocalUser ? "My Videos" : "User Videos"}>
              {videoData == null ? (
                <Spin />
              ) : (
                <List
                  itemLayout="vertical"
                  size="large"
                  pagination={{
                    pageSize: 3,
                  }}
                  dataSource={videoData}
                  renderItem={(item) => (
                    <List.Item
                      actions={[
                        <IconText
                          icon={EyeOutlined}
                          text={item.video_view}
                          key="list-vertical-star-o"
                          className="profile-icon-text"
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
                    >
                      <List.Item.Meta
                        title={
                          <Grid className="profile-video-line">
                            <Link
                              to={"/video/" + item.video_id}
                              className="profile-video-title"
                            >
                              {item.video_title}
                              <Badge
                                status={
                                  item.video_raw_status === "streaming"
                                    ? "success"
                                    : "warning"
                                }
                                text={item.video_raw_status}
                              />
                            </Link>
                            {isLocalUser ? (
                              <Link to={`/video/update/${item.video_id}`}>
                                <Button className="navigateButton profile-manage-video">
                                  Manage Video
                                </Button>
                              </Link>
                            ) : (
                              <div></div>
                            )}
                          </Grid>
                        }
                        avatar={
                          <Link to={"/video/" + item.video_id}>
                            <img
                              width={160}
                              alt="logo"
                              src={generateThumbnail(item.video_thumbnail)}
                            />
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

            <Card
              title={
                isLocalUser ? "My Watching History" : "User Watching History"
              }
            >
              {userProcess == null ? (
                <Spin />
              ) : (
                <List
                  grid={{ gutter: 12, column: 2 }}
                  itemLayout="vertical"
                  size="large"
                  pagination={{
                    pageSize: 4,
                  }}
                  dataSource={userProcess}
                  renderItem={(item) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={
                          <Link to={"/video/" + item.video_id}>
                            <Avatar
                              shape="square"
                              size={54}
                              src={generateThumbnail(item.video_thumbnail)}
                            />
                          </Link>
                        }
                        title={
                          <Link to={"/video/" + item.video_id}>
                            {item.video_title}
                          </Link>
                        }
                        description={
                          "Last watched on " + dateConvert(item.process_date)
                        }
                      />
                    </List.Item>
                  )}
                />
              )}
            </Card>

            <Card title={isLocalUser ? "My Stars" : "User Stars"}>
              {userStar == null ? (
                <Spin />
              ) : (
                <List
                  grid={{ gutter: 12, column: 2 }}
                  itemLayout="vertical"
                  size="large"
                  pagination={{
                    pageSize: 2,
                  }}
                  dataSource={userStar}
                  renderItem={(item) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={
                          <Link to={"/video/" + item.video_id}>
                            <Avatar
                              shape="square"
                              size={54}
                              src={generateThumbnail(item.video_thumbnail)}
                            />
                          </Link>
                        }
                        title={
                          <Link to={"/video/" + item.video_id}>
                            {item.video_title}
                          </Link>
                        }
                        description={"Star on " + dateConvert(item.star_date)}
                      />
                    </List.Item>
                  )}
                />
              )}
            </Card>

            <Card title={isLocalUser ? "My Comments" : "User Comments"}>
              {userComment == null ? (
                <Spin />
              ) : (
                <List
                  itemLayout="vertical"
                  size="large"
                  pagination={{
                    pageSize: 2,
                  }}
                  dataSource={userComment}
                  renderItem={(item) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={
                          <Link to={"/video/" + item.video_id}>
                            <Avatar
                              shape="square"
                              size={54}
                              src={generateThumbnail(item.video_thumbnail)}
                            />
                          </Link>
                        }
                        title={
                          <Link to={"/video/" + item.video_id}>
                            {item.video_title}
                          </Link>
                        }
                        description={ellipsifyStr(item.comment)}
                      />
                    </List.Item>
                  )}
                />
              )}
            </Card>

            <Card title={isLocalUser ? "My Likes" : "User Likes"}>
              {userLike == null ? (
                <Spin />
              ) : (
                <List
                  grid={{ gutter: 12, column: 2 }}
                  itemLayout="vertical"
                  size="large"
                  pagination={{
                    pageSize: 2,
                  }}
                  dataSource={userLike}
                  renderItem={(item) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={
                          <Link to={"/video/" + item.video_id}>
                            <Avatar
                              shape="square"
                              size={54}
                              src={generateThumbnail(item.video_thumbnail)}
                            />
                          </Link>
                        }
                        title={
                          <Link to={"/video/" + item.video_id}>
                            {item.video_title}
                          </Link>
                        }
                        description={"Like on " + dateConvert(item.like_date)}
                      />
                    </List.Item>
                  )}
                />
              )}
            </Card>
          </div>
        </Col>
      </Row>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default UserProfile;
