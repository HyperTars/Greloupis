import React, { Component } from "react";
import "../static/css/App.css";
import { Link } from "react-router-dom";
import { getSubstr, generateAvatar } from "../util";
import { Menu, Dropdown } from "antd";
import VideoCallIcon from "@material-ui/icons/VideoCall";
import SearchIcon from "@material-ui/icons/Search";

const isLoggedIn = localStorage.getItem("user_id") != null;
const currentUserId = getSubstr(localStorage.getItem("user_id"));

const menu1 = (
  <Menu>
    <Menu.Item key="Profile">
      <a href={`/user/${currentUserId}`}>View Profile</a>
    </Menu.Item>

    <Menu.Item key="Logout">
      <a href="/logout" className="logout-alert">
        Logout
      </a>
    </Menu.Item>
  </Menu>
);

const menu2 = (
  <Menu>
    <Menu.Item key="Login">
      <a href="/login">Login</a>
    </Menu.Item>
    <Menu.Item key="Register">
      <a href="/register">Register</a>
    </Menu.Item>
  </Menu>
);

class Header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: "",
    };
  }

  render() {
    //const logoPath = "/Assets/logo/greloupis-horizontal-blue-fill-b.svg"
    const logoPath = "/Assets/logo/greloupis-horizontal.png";
    const avatarPath = generateAvatar();

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
            placeholder="Search user name, video title, video channel, etc."
            value={this.state.value}
            onChange={(e) => {
              this.setState({
                value: e.target.value,
              });
            }}
          ></input>

          <div className="header-searchBar__button">
            <button className="header-searchBar__button-icon" type="submit">
              <SearchIcon className="header-searchBar__search-icon" />
            </button>

            <span className="tooltip header-searchBar__button-tooltip">
              Search
            </span>
          </div>
        </form>

        <div className="header-profile">
          <Link to="/video/upload">
            <div className="header-profile__upload">
              <VideoCallIcon className="header-profile__upload-icon" />
              <span className="tooltip header-tooltip-text">
                Upload a new video
              </span>
            </div>
          </Link>

          <div className="header-profile__avatar">
            <Dropdown overlay={isLoggedIn ? menu1 : menu2} trigger={["click"]}>
              <a
                className="ant-dropdown-link"
                onClick={(e) => e.preventDefault()}
                href="/"
              >
                <img
                  className="header-profile__avatar-img"
                  src={avatarPath}
                  alt="Profile Avatar"
                ></img>
                <span className="tooltip header-tooltip-text">
                  View Profile
                </span>
              </a>
            </Dropdown>
          </div>
          {/* </Link> */}
        </div>
      </nav>
    );
  }
}

export default Header;
