import React, { useState, useEffect } from "react";
import { getUserInfo, deleteUser, deleteVideo } from "./FetchData";
import { Redirect, Link } from "react-router-dom";
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
  List,
  Avatar,
  Space,
  Upload,
  message,
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
} from "../util";
import logout from "./Logout";

function UserProfile({ userId }) {
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);
  const [userData, setUserData] = useState([]);

  const [videoData, setVideoData] = useState([]);

  const [userLike, setUserLike] = useState([]);
  const [userDislike, setUserDislike] = useState([]);
  const [userStar, setUserStar] = useState([]);
  const [userComment, setUserComment] = useState([]);

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

        if (JSON.stringify(res.body["video"]) !== "[{}]")
          setVideoData(res.body["video"]);
        if (JSON.stringify(res.body["video_op"]) !== "[{}]") {
          setUserLike(
            res.body["video_op"].filter((element) => element.like === true)
          );
          setUserDislike(
            res.body["video_op"].filter((element) => element.dislike === true)
          );
          setUserStar(
            res.body["video_op"].filter((element) => element.star === true)
          );
          setUserComment(
            res.body["video_op"].filter((element) => element.comment !== "")
          );
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
      sm: { span: 6 },
    },
    wrapperCol: {
      xs: { span: 24 },
      sm: { span: 24 },
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

  const deleteUserHandler = () => {
    deleteUser(userId).then(() => {
      alert("Account deleted!");
      logout();
      window.location.href = "/";
    });
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

  const RegistrationForm = () => {
    const [form] = Form.useForm();

    const onFinish = (values) => {
      console.log("Received values of form: ", values);
    };

    const prefixSelector = (
      <Form.Item name="prefix" noStyle>
        <Select style={{ width: 70 }}>
          <Option value="1">+1</Option>
          <Option value="86">+86</Option>
        </Select>
      </Form.Item>
    );

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
          name="avatar"
          label="Avatar"
          rules={[{ message: "Please upload your avatar!" }]}
        >
          {isLocalUser ? (
            <Upload {...uploadProps}>
              <Button icon={<UploadOutlined />}>Click to Upload</Button>
            </Upload>
          ) : (
            <Avatar src={userData ? userData["user_thumbnail"] : "/"} />
          )}
        </Form.Item>

        <Form.Item
          name="nickname"
          label={
            <span>
              Name&nbsp;
              <Tooltip title="What do you want others to call you?">
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
              defaultValue={userData ? userData["user_name"] : "..."}
            />
          ) : (
            <Input
              defaultValue={userData ? userData["user_name"] : "..."}
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="email"
          label="Email:"
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
              defaultValue={userData ? userData["user_email"] : "..."}
            />
          ) : (
            <Input
              defaultValue={userData ? userData["user_email"] : "..."}
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

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
                  : "..."
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_first_name"]
                  : "..."
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
                  : "..."
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_last_name"]
                  : "..."
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
                  : "..."
              }
              addonBefore={prefixSelector}
              style={{ width: "100%" }}
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_phone"]
                  : "..."
              }
              style={{ width: "100%" }}
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
                  : "..."
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_street1"]
                  : "..."
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
                  : "..."
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_street2"]
                  : "..."
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
                  : "..."
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_city"]
                  : "..."
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
                  : "..."
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_state"]
                  : "..."
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
                  : "..."
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_country"]
                  : "..."
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
                  : "..."
              }
            />
          ) : (
            <Input
              defaultValue={
                userData["user_detail"]
                  ? userData["user_detail"]["user_zip"]
                  : "..."
              }
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        <Form.Item
          name="status"
          label="Status"
          rules={[{ message: "Please select your status!" }]}
        >
          {isLocalUser ? (
            <Select
              placeholder="Select your user status: "
              defaultValue={userData ? userData["user_status"] : "..."}
            >
              <Option value="public">public</Option>
              <Option value="private">private</Option>
              <Option value="closed">closed</Option>
            </Select>
          ) : (
            <Input
              defaultValue={userData ? userData["user_status"] : "..."}
              style={{ width: "100%" }}
              disabled
              bordered={false}
            />
          )}
        </Form.Item>

        {/* <Form.Item
          name="password"
          label="Password"
          rules={[
            {
              required: true,
              message: "Please input your password!",
            },
          ]}
          hasFeedback
        >
          <Input.Password />
        </Form.Item>

        <Form.Item
          name="confirm"
          label="Confirm Password"
          dependencies={["password"]}
          hasFeedback
          rules={[
            {
              required: true,
              message: "Please confirm your password!",
            },
            ({ getFieldValue }) => ({
              validator(rule, value) {
                if (!value || getFieldValue("password") === value) {
                  return Promise.resolve();
                }
                return Promise.reject(
                  "The two passwords that you entered do not match!"
                );
              },
            }),
          ]}
        >
          <Input.Password />
        </Form.Item> */}

        {isLocalUser ? (
          <div>
            <Form.Item {...tailFormItemLayout}>
              <Button type="primary" htmlType="submit">
                Update Account
              </Button>
            </Form.Item>
          </div>
        ) : (
          <div></div>
        )}

        {isLocalUser ? (
          <Button
            type="primary"
            htmlType="submit"
            className="deleteButton"
            onClick={deleteUserHandler}
          >
            Delete Account
          </Button>
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
      <Row gutter={12}>
        <Col span={8}>
          <div className="userProfile">
            <h4>{"User Profiles: "}</h4>
            <RegistrationForm></RegistrationForm>
          </div>
        </Col>

        <Col span={16}>
          <div className="userProfile">
            <h4>{"User Videos: "}</h4>
            {videoData == null ? (
              <Spin />
            ) : (
              <List
                itemLayout="vertical"
                size="large"
                pagination={{
                  pageSize: 2,
                }}
                dataSource={videoData}
                renderItem={(item) => (
                  <List.Item
                    actions={[
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
                      isLocalUser ? (
                        <Button
                          className="deleteButton"
                          onClick={() => {
                            deleteVideo(item.video_id).then(() => {
                              alert("Video deleted!");
                              window.location.reload();
                            });
                          }}
                        >
                          Delete Video
                        </Button>
                      ) : (
                        <div></div>
                      ),
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

            <h4>{"User Stars: "}</h4>
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

            <h4>{"User Comments: "}</h4>
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
                      description={item.comment}
                    />
                  </List.Item>
                )}
              />
            )}

            <h4>{"User Likes: "}</h4>
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

            <h4>{"User Dislikes: "}</h4>
            {userDislike == null ? (
              <Spin />
            ) : (
              <List
                grid={{ gutter: 12, column: 2 }}
                itemLayout="vertical"
                size="large"
                pagination={{
                  pageSize: 2,
                }}
                dataSource={userDislike}
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
                        "Dislike on " + dateConvert(item.dislike_date)
                      }
                    />
                  </List.Item>
                )}
              />
            )}
          </div>
        </Col>
      </Row>
    </div>
  );

  return loading ? loadingFormat : errorMsg ? errorFormat : sampleFormat;
}

export default UserProfile;
