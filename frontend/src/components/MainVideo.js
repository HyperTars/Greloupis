import React, { Component } from "react";
import { dateConvert } from "../util";
import {
  createUserVideoLike,
  deleteUserVideoLike,
  createUserVideoDislike,
  deleteUserVideoDislike,
  createUserVideoStar,
  deleteUserVideoStar,
} from "./FetchData";
import * as func from "../util";

const VIDEO_INFO_LIMIT = 1000;

class MainVideo extends Component {
  state = {
    isLike: false,
    isDislike: false,
    isStar: false,
    showMore: false,
    showLess: false,
  };

  static getDerivedStateFromProps(props, state) {
    if (
      state.isLike !== props.videoLike ||
      state.isDislike !== props.videoDislike ||
      state.isStar !== props.videoStar
    ) {
      return {
        isLike: props.videoLike,
        isDislike: props.videoDislike,
        isStar: props.videoStar,
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
    func.loginCheck();

    // like a video
    if (!this.props.videoLike && this.props.mainVideo.video_id) {
      createUserVideoLike(
        this.props.mainVideo.video_id,
        func.getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          this.setState({
            isLike: true,
          });
        })
        .then(() => {
          window.location.reload();
        });
    }

    // undo a like
    else if (this.props.videoLike && this.props.mainVideo.video_id) {
      deleteUserVideoLike(
        this.props.mainVideo.video_id,
        func.getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          this.setState({
            isLike: false,
          });
        })
        .then(() => {
          window.location.reload();
        });
    }
  };

  dislikeHandler = () => {
    func.loginCheck();

    // dislike a video
    if (!this.props.videoDisLike && this.props.mainVideo.video_id) {
      createUserVideoDislike(
        this.props.mainVideo.video_id,
        func.getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          this.setState({
            isDislike: true,
          });
        })
        .then(() => {
          window.location.reload();
        });
    }

    // undo a dislike
    else if (this.props.videoDisLike && this.props.mainVideo.video_id) {
      deleteUserVideoDislike(
        this.props.mainVideo.video_id,
        func.getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          this.setState({
            isDislike: false,
          });
        })
        .then(() => {
          window.location.reload();
        });
    }
  };

  starHandler = () => {
    func.loginCheck();

    // star a video
    if (!this.props.videoStar && this.props.mainVideo.video_id) {
      createUserVideoStar(
        this.props.mainVideo.video_id,
        func.getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          this.setState({
            isStar: true,
          });
        })
        .then(() => {
          window.location.reload();
        });
    }

    // undo a star
    else if (this.props.videoStar && this.props.mainVideo.video_id) {
      deleteUserVideoStar(
        this.props.mainVideo.video_id,
        func.getSubstr(localStorage.getItem("user_id"))
      )
        .then(() => {
          this.setState({
            isStar: false,
          });
        })
        .then(() => {
          window.location.reload();
        });
    }
  };

  render() {
    const { mainVideo } = this.props;
    const mainVideoCopy = { ...mainVideo };

    const {
      video_id,
      video_raw_content,
      video_thumbnail,
      video_title,
      video_view,
      video_like,
      video_dislike,
      video_upload_date,
    } = mainVideoCopy;

    return (
      <section id={video_id} className="main-video">
        <div className="main-video__content">
          <video
            controls
            src={video_raw_content}
            type="mp4/video"
            poster={video_thumbnail}
          ></video>
        </div>

        <div className="main-video__description">
          <div className="description-title">{video_title}</div>
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
                  />
                  <span>{video_like}</span>
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
                  />
                  <span>{video_dislike}</span>
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
              <img
                className="author-details__avatar"
                src="/Assets/avatar.jpg"
                alt="Avatar"
              />
              <div className="author-details__info">
                <p className="author-details__info-date">
                  Published on {dateConvert(video_upload_date)}
                </p>
              </div>
            </div>
          </div>
          <div className="main-video__details-info">
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
