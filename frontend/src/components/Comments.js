import React, { Component } from "react";
import * as func from "../util";
import { createUserVideoComment, deleteUserVideoComment } from "./FetchData";

export default class Comments extends Component {
  state = {
    mainVideoId: "",
    comments: [],
    isAddingComment: false,
  };

  static getDerivedStateFromProps(props, state) {
    if (
      props.mainVideoId !== state.mainVideoId ||
      props.comments !== state.comments
    ) {
      return {
        mainVideoId: props.mainVideoId,
        comments: props.comments,
      };
    }

    return null;
  }

  deleteCommentHandler = () => {
    deleteUserVideoComment(
      this.props.mainVideoId,
      func.getSubstr(localStorage.getItem("user_id"))
    ).then(() => {
      window.location.reload();
    });
  };

  toggleCommentForm = () => {
    this.setState({ isAddingComment: !this.state.isAddingComment });
    this.commentInput.value = "";
  };

  submitCommentHandler = () => {
    if (
      !localStorage.getItem("user_name") ||
      !localStorage.getItem("user_id") ||
      !localStorage.getItem("user_token")
    ) {
      alert("You need to sign in to comment!");
    }

    if (this.commentInput.value) {
      const data = {
        comment: this.commentInput.value,
      };

      createUserVideoComment(
        this.props.mainVideoId,
        func.getSubstr(localStorage.getItem("user_id")),
        data
      );

      this.commentInput.value = "";
    }
    this.toggleCommentForm();
    window.location.reload();
  };

  renderCommentForm() {
    return (
      <form className="comments-form__input">
        <input
          className="comments-form__input-shown"
          type="text"
          name="commentInput"
          ref={(input) => (this.commentInput = input)}
          placeholder="Add a public comment, or update your existed comment on this video..."
          required
        />
        <div className="comments-form__input-buttons">
          <button
            className="cancelBtn"
            type="button"
            onClick={this.toggleCommentForm}
          >
            CANCEL
          </button>
          <button
            className="addBtn"
            type="button"
            onClick={this.submitCommentHandler}
          >
            COMMENT
          </button>
        </div>
      </form>
    );
  }

  renderAddCommentInput() {
    return (
      <form className="comments-form__input">
        <input
          ref={(input) => (this.commentInput = input)}
          className="comments-form__input-hidden"
          onClick={this.toggleCommentForm}
          type="text"
          name="commentInput"
          placeholder="Add a public comment, or update your existed comment on this video..."
        />
      </form>
    );
  }

  render() {
    const comments = this.state.comments;
    const commentsJSX = [];

    if (comments) {
      for (let i = comments.length - 1; i >= 0; i--) {
        commentsJSX.push(
          <CommentBlock
            deleteCommentHandler={this.deleteCommentHandler}
            commentId={i}
            key={i}
            id={i}
            userName={comments[i].user_name}
            timestamp={comments[i].comment_date}
            comment={comments[i].comment}
          />
        );
      }
    }

    return (
      <section className="comments-list">
        <div className="comments-form">
          <img
            className="comments-form__avatar"
            src="/Assets/avatar.jpg"
            alt="Profile Avatar"
          />
          {!this.state.isAddingComment
            ? this.renderAddCommentInput()
            : this.renderCommentForm()}
        </div>
        {commentsJSX}
      </section>
    );
  }
}

// Child Component CommentBlock ------------------------------------------------------------------------------------------------

class CommentBlock extends Component {
  state = {
    commentId: "",
    showDeleteBtn: false,
    showConfirmationWindow: false,
  };

  componentDidUpdate() {
    if (this.state.commentId !== this.props.id) {
      this.setState({
        commentId: this.props.id,
      });
    }
  }

  deleteCommentHandler = () => {
    this.props.deleteCommentHandler(String(this.state.commentId));
    this.displayConfirmWindow(false);
  };

  displayDeleteButton = (bool) => {
    this.setState({
      showDeleteBtn: bool,
    });
  };

  displayConfirmWindow = (bool) => {
    this.setState({
      showConfirmationWindow: bool,
    });
  };

  renderDeleteConfirmationWindow() {
    return (
      <div className="comment-block__confirmation">
        <div>
          <span>Are you sure you want to delete this comment?</span>
          <button onClickCapture={this.deleteCommentHandler}>Yes</button>
          <button onClick={() => this.displayConfirmWindow(false)}>No</button>
        </div>
      </div>
    );
  }

  renderDeleteButton() {
    return (
      <span>
        <img
          onClickCapture={() => this.displayConfirmWindow(true)}
          src="/Assets/delete_forever.svg"
          alt="Icon"
        />
      </span>
    );
  }

  render() {
    const { id, userName, timestamp, comment } = this.props;

    return (
      <li
        ref={(li) => (this.commentBlock = li)}
        id={id}
        className="comment-block"
        onMouseOver={() => {
          if (
            localStorage.getItem("user_name") &&
            this.props.userName ===
              func.getSubstr(localStorage.getItem("user_name"))
          )
            this.displayDeleteButton(true);
        }}
        onMouseLeave={() => this.displayDeleteButton(false)}
      >
        {this.state.showConfirmationWindow
          ? this.renderDeleteConfirmationWindow()
          : null}
        {this.state.showDeleteBtn ? this.renderDeleteButton() : null}
        <img
          className="comment-block__avatar"
          src={`https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png`}
          alt="Profile Avatar"
        />
        <div className="comment-block__content">
          <span className="comment-block__content-name">{userName}</span>
          <span className="comment-block__content-timestamp">
            {func.convertToRelativeTime(timestamp)}
          </span>
          <p className="comment-block__content-comment">{comment}</p>
        </div>
      </li>
    );
  }
}
