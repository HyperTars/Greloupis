import React, { PureComponent } from "react";
import { dateConvert, loginCheck, getSubstr } from "../util";
import {
  createUserVideoLike,
  deleteUserVideoLike,
  createUserVideoDislike,
  deleteUserVideoDislike,
  createUserVideoStar,
  deleteUserVideoStar,
  updateUserVideoProcess,
} from "./FetchData";
import { Link } from "react-router-dom";
import { Tag } from "antd";
import ReactJWPlayer from "react-jw-player";

const VIDEO_INFO_LIMIT = 1000;

class MainVideo extends PureComponent {
  state = {
    isLike: false,
    isDislike: false,
    isStar: false,
    showMore: false,
    showLess: false,
    likeNum: 0,
    dislikeNum: 0,
  };

  static getDerivedStateFromProps(props, state) {
    if (
      state.isLike !== props.videoLike ||
      state.isDislike !== props.videoDisLike ||
      state.isStar !== props.videoStar ||
      state.likeNum !== props.mainVideo.video_like ||
      state.dislikeNum !== props.mainVideo.video_dislike
    ) {
      return {
        isLike: props.videoLike,
        isDislike: props.videoDisLike,
        isStar: props.videoStar,
        likeNum: props.mainVideo.video_like,
        dislikeNum: props.mainVideo.video_dislike,
      };
    }

    return null;
  }
  componentDidUpdate() {
    const description = this.props.description;
    const { showMore, showLess } = this.state;
    if (description) {
      if (description.length > VIDEO_INFO_LIMIT) {
        if (!showMore || showLess) {
          this.setState({
            showMore: true,
            showLess: false,
          });
        }
      } else if (description.length < VIDEO_INFO_LIMIT) {
        if ((showMore && showLess) || showMore || showLess) {
          this.setState({
            showMore: false,
            showLess: false,
          });
        }
      }
    }
  }
  toggleHandler = () => {
    this.setState({
      showMore: !this.state.showMore,
      showLess: !this.state.showLess,
    });
  };
  renderDescription() {
    return (
      <p className="main-video__info">
        {this.props.description.slice(0, VIDEO_INFO_LIMIT) + "...."}
      </p>
    );
  }
  renderFullDescription() {
    return <p className="main-video__info">{this.props.description}</p>;
  }
  renderShowMoreToggle() {
    return (
      <div onClick={this.toggleHandler} className="show-more-toggle">
        <img src="/Assets/expand_more.svg" alt="Icon" />
        SHOW MORE
      </div>
    );
  }
  renderShowLessToggle() {
    return (
      <div onClick={this.toggleHandler} className="show-more-toggle">
        <img src="/Assets/expand_less.svg" alt="Icon" />
        SHOW LESS
      </div>
    );
  }
  likeHandler = () => {
    loginCheck();

    if (this.state.isDislike) {
      let originNum = this.state.dislikeNum;
      // eslint-disable-next-line
      this.state.isDislike = false;
      // eslint-disable-next-line
      this.state.dislikeNum = originNum - 1;

      document.getElementById("dislike-image").src = "/Assets/dislike.svg";
      document.getElementById(
        "dislike-number"
      ).innerHTML = this.state.dislikeNum;
    }

    // like a video
    if (!this.state.isLike && this.props.mainVideo.video_id) {
      createUserVideoLike(
        this.props.mainVideo.video_id,
        getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          let originNum = this.state.likeNum;
          // eslint-disable-next-line
          this.state.isLike = true;
          // eslint-disable-next-line
          this.state.likeNum = originNum + 1;

          document.getElementById("like-image").src = "/Assets/like-black.svg";
          document.getElementById("like-number").innerHTML = this.state.likeNum;
        })
        .catch(() => {});
    }

    // undo a like
    else if (this.state.isLike && this.props.mainVideo.video_id) {
      deleteUserVideoLike(
        this.props.mainVideo.video_id,
        getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          let originNum = this.state.likeNum;
          // eslint-disable-next-line
          this.state.isLike = false;
          // eslint-disable-next-line
          this.state.likeNum = originNum - 1;

          document.getElementById("like-image").src = "/Assets/like.svg";
          document.getElementById("like-number").innerHTML = this.state.likeNum;
        })
        .catch(() => {});
    }
  };
  dislikeHandler = () => {
    loginCheck();

    if (this.state.isLike) {
      let originNum = this.state.likeNum;
      // eslint-disable-next-line
      this.state.isLike = false;
      // eslint-disable-next-line
      this.state.likeNum = originNum - 1;

      document.getElementById("like-image").src = "/Assets/like.svg";
      document.getElementById("like-number").innerHTML = this.state.likeNum;
    }

    // dislike a video
    if (!this.state.isDislike && this.props.mainVideo.video_id) {
      createUserVideoDislike(
        this.props.mainVideo.video_id,
        getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          let originNum = this.state.dislikeNum;
          // eslint-disable-next-line
          this.state.isDislike = true;
          // eslint-disable-next-line
          this.state.dislikeNum = originNum + 1;

          document.getElementById("dislike-image").src =
            "/Assets/dislike-black.svg";
          document.getElementById(
            "dislike-number"
          ).innerHTML = this.state.dislikeNum;
        })
        .catch(() => {});
    }

    // undo a dislike
    else if (this.state.isDislike && this.props.mainVideo.video_id) {
      deleteUserVideoDislike(
        this.props.mainVideo.video_id,
        getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          let originNum = this.state.dislikeNum;
          // eslint-disable-next-line
          this.state.isDislike = false;
          // eslint-disable-next-line
          this.state.dislikeNum = originNum - 1;

          document.getElementById("dislike-image").src = "/Assets/dislike.svg";
          document.getElementById(
            "dislike-number"
          ).innerHTML = this.state.dislikeNum;
        })
        .catch(() => {});
    }
  };
  starHandler = () => {
    loginCheck();

    // star a video
    if (!this.state.isStar && this.props.mainVideo.video_id) {
      createUserVideoStar(
        this.props.mainVideo.video_id,
        getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          // eslint-disable-next-line
          this.state.isStar = true;

          document.getElementById("star-image").src = "/Assets/star-black.svg";
        })
        .catch(() => {});
    }

    // undo a star
    else if (this.state.isStar && this.props.mainVideo.video_id) {
      deleteUserVideoStar(
        this.props.mainVideo.video_id,
        getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          // eslint-disable-next-line
          this.state.isStar = false;

          document.getElementById("star-image").src = "/Assets/star.svg";
        })
        .catch(() => {});
    }
  };

  render() {
    const { mainVideo } = this.props;
    const mainVideoCopy = { ...mainVideo };

    const {
      user_id,
      user_name,
      user_thumbnail,
      video_id,
      video_duration,
      video_uri,
      video_thumbnail,
      video_title,
      video_view,
      video_like,
      video_dislike,
      video_upload_date,
      video_channel,
      video_category,
      video_tag,
    } = mainVideoCopy;

    const playList = {
      playlist: [
        {
          image: video_thumbnail,
          duration: video_duration,
          sources: [
            {
              file: video_uri ? video_uri.video_uri_high : "",
              type: "video/mp4",
              height: 1080,
              width: 1920,
              label: "FHD 1080p",
            },
            {
              file: video_uri ? video_uri.video_uri_mid : "",
              type: "video/mp4",
              height: 720,
              width: 1280,
              label: "HD 720p",
            },
            {
              file: video_uri ? video_uri.video_uri_low : "",
              type: "video/mp4",
              height: 360,
              width: 540,
              label: "SD 540p",
            },
          ],
        },
      ],
    };

    return (
      <section id={video_id} className="main-video">
        <div className="main-video__content">
          {video_uri && video_uri.video_uri_high !== "" ? (
            <ReactJWPlayer
              playerId="jw-player"
              playerScript="https://content.jwplatform.com/libraries/jvJ1Gu3c.js"
              playlist={playList}
              onVideoLoad={() => {
                if (
                  localStorage.getItem("user_id") &&
                  this.props.videoProcess.process
                ) {
                  document.getElementsByTagName(
                    "video"
                  )[0].currentTime = parseInt(
                    this.props.videoProcess.process,
                    10
                  );
                }
              }}
              onTime={() => {
                if (localStorage.getItem("user_id")) {
                  updateUserVideoProcess(
                    video_id,
                    getSubstr(localStorage.getItem("user_id")),
                    {
                      process: parseInt(
                        document.getElementsByTagName("video")[0].currentTime,
                        10
                      ),
                    }
                  );
                }
              }}
              onOneHundredPercent={() => {
                if (localStorage.getItem("user_id")) {
                  updateUserVideoProcess(
                    video_id,
                    getSubstr(localStorage.getItem("user_id")),
                    {
                      process: 0,
                    }
                  );
                  document.getElementsByTagName("video")[0].currentTime = 0;
                }
              }}
            />
          ) : (
            <div></div>
          )}
        </div>

        <div className="main-video__description">
          <div className="description-title">
            <Tag>{video_channel}</Tag>
            {video_title}
          </div>
          <div className="description-reaction">
            <p className="description-reaction__views">{video_view} views</p>
            <div className="description-reaction__icons">
              <div className="likes">
                <button onClick={this.likeHandler} className="likes-btn">
                  <img
                    src={
                      this.props.videoLike
                        ? "/Assets/like-black.svg"
                        : "/Assets/like.svg"
                    }
                    alt="Icon"
                    id="like-image"
                  />
                  <span id="like-number">{video_like}</span>
                </button>
                <span className="tooltip likes__tooltip">Like this</span>
              </div>
              <div className="dislikes">
                <button onClick={this.dislikeHandler} className="dislikes-btn">
                  <img
                    src={
                      this.props.videoDisLike
                        ? "/Assets/dislike-black.svg"
                        : "/Assets/dislike.svg"
                    }
                    alt="Icon"
                    id="dislike-image"
                  />
                  <span id="dislike-number">{video_dislike}</span>
                </button>
                <span className="tooltip dislikes__tooltip">Dislike this</span>
              </div>
              <div className="star">
                <button onClick={this.starHandler} className="star-btn">
                  <img
                    src={
                      this.props.videoStar
                        ? "/Assets/star-black.svg"
                        : "/Assets/star.svg"
                    }
                    alt="Icon"
                    id="star-image"
                  />
                  <span>Star</span>
                </button>
                <span className="tooltip star__tooltip">Star this</span>
              </div>
            </div>
          </div>
        </div>

        <div className="main-video__details">
          <div className="main-video__details-author">
            <div className="author-details">
              <Link to={`/user/${user_id}`}>
                <img
                  className="author-details__avatar"
                  src={user_thumbnail}
                  alt="Avatar"
                />
              </Link>
              <div className="author-details__info">
                <p className="author-details__info-date">
                  <Link to={`/user/${user_id}`}>{user_name + " "}</Link>
                  Published on {dateConvert(video_upload_date)}
                </p>
              </div>
            </div>
          </div>
          <div className="main-video__details-info">
            {video_category && video_category.length > 0
              ? video_category.map((e) => {
                  return (
                    <Link to={`/search?keyword=${e}`}>{"#" + e + " "}</Link>
                  );
                })
              : ""}
            {video_tag && video_tag.length > 0
              ? video_tag.map((e) => {
                  return (
                    <Link to={`/search?keyword=${e}`}>{"#" + e + " "}</Link>
                  );
                })
              : ""}
            {this.props.description
              ? this.state.showMore
                ? this.renderDescription()
                : !this.state.showMore
                ? this.renderFullDescription()
                : this.renderFullDescription()
              : null}
            {this.props.description
              ? this.state.showMore
                ? this.renderShowMoreToggle()
                : this.state.showLess
                ? this.renderShowLessToggle()
                : null
              : null}
          </div>
        </div>
      </section>
    );
  }
}

export default MainVideo;
