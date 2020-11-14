import React, { Component } from "react";
import "../static/css/App.css";
import { Link } from "react-router-dom";

class Header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: "",
    };
  }

  render() {
    const logoPath = "/Assets/logo/svg/greloupis-horizontal-blue-fill-b.svg";
    const uploadPath = "/Assets/upload.svg";
    const avatarPath = "/Assets/avatar.jpg";

    return (
      <nav className="header">
        <Link to="/">
          <div className="header-logo">
            <img className="header-logo__img" src={logoPath} alt="Logo"></img>
            <span className="tooltip header-searchBar__button-tooltip">
              Home Page
            </span>
          </div>
        </Link>

        <form className="header-searchBar" action="/search">
          <input
            className="header-searchBar__input"
            type="text"
            name="keyword"
            placeholder="Search"
            value={this.state.value}
            onChange={(e) => {
              this.setState({
                value: e.target.value,
              });
            }}
          ></input>

          <div className="header-searchBar__button">
            <button className="header-searchBar__button-icon" type="submit">
              <img src="/Assets/search.svg" alt="Search Icon"></img>
            </button>

            <span className="tooltip header-searchBar__button-tooltip">
              Search
            </span>
          </div>
        </form>

        <div className="header-profile">
          <Link to="/video/upload">
            <div className="header-profile__upload">
              <img
                className="header-profile__upload-icon"
                src={uploadPath}
                alt="Content Upload Button"
              ></img>
              <span className="tooltip header-tooltip-text">
                Upload a new video
              </span>
            </div>
          </Link>

          <Link to="/dashboard">
            <div className="header-profile__avatar">
              <img
                className="header-profile__avatar-img"
                src={avatarPath}
                alt="Profile Avatar"
              ></img>
              <span className="tooltip header-tooltip-text">View Profile</span>
            </div>
          </Link>
        </div>
      </nav>
    );
  }
}

export default Header;
