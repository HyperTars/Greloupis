import React, { Component } from "react";
import { dateConvert } from "../util";

const VIDEO_INFO_LIMIT = 150;

class MainVideo extends Component {
  state = {
    isLike: false,
    isDislike: false,
    descPlus: false,
    showMore: false,
    showLess: false,
  };

  componentDidUpdate() {
    const description = this.props.description;
    const { showMore, showLess, descPlus } = this.state;
    if (description) {
      if (description.length > VIDEO_INFO_LIMIT && !descPlus) {
        this.setState({
          descPlus: true,
          showMore: true,
          showLess: false,
        });
      } else if (description.length < VIDEO_INFO_LIMIT) {
        if ((showMore && showLess) || showMore || showLess) {
          this.setState({
            descPlus: false,
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
    if (!this.state.isLike) {
      this.props.likeHandler();
      this.setState({
        isLike: true,
      });
    }
  };

  dislikeHandler = () => {
    if (!this.state.isDislike) {
      this.props.dislikeHandler();
      this.setState({
        isDislike: true,
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
                  <img src="/Assets/like.svg" alt="Icon" />
                  <span>{video_like}</span>
                </button>
                <span className="tooltip likes__tooltip">Love this</span>
              </div>
              <div className="dislikes">
                <button onClick={this.dislikeHandler} className="dislikes-btn">
                  <img src="/Assets/dislike.svg" alt="Icon" />
                  <span>{video_dislike}</span>
                </button>
                <span className="tooltip dislikes__tooltip">Dislike this</span>
              </div>
              <div className="star">
                <button className="star-btn">
                  <img src="/Assets/star.svg" alt="Icon" />
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
              ? this.state.descPlus && this.state.showMore
                ? this.renderDescription()
                : this.state.descPlus && !this.state.showMore
                ? this.renderFullDescription()
                : this.renderFullDescription()
              : null}
            {this.props.description
              ? this.state.descPlus && this.state.showMore
                ? this.renderShowMoreToggle()
                : this.state.descPlus && this.state.showLess
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
