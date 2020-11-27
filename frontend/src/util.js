import moment from "moment";
let Uuid = require("node-uuid");

// convert timestamp to relative time
export function convertToRelativeTime(timestamp) {
  let t = moment(timestamp).format();
  return moment(t).startOf("minutes").fromNow();
}

// convert second to hour:minute:second format
export function secondTimeConvert(second) {
  if (second < 3600)
    return [parseInt((second / 60) % 60), second % 60]
      .join(":")
      .replace(/\b(\d)\b/g, "0$1");
  else
    return [
      parseInt(second / 60 / 60),
      parseInt((second / 60) % 60),
      second % 60,
    ]
      .join(":")
      .replace(/\b(\d)\b/g, "0$1");
}

// convert timestamp to yy:mm:dd
export function dateConvert(time) {
  let d = new Date(time),
    month = "" + (d.getMonth() + 1),
    day = "" + d.getDate(),
    year = d.getFullYear();

  if (month.length < 2) month = "0" + month;
  if (day.length < 2) day = "0" + day;

  return [year, month, day].join("-");
}

// slice the first and last character of the string
export function getSubstr(rawStr) {
  if (rawStr == null) return rawStr;

  return rawStr.slice(1, -1);
}

// set the max display length of given string
export function ellipsifyStr(rawStr, maxLength = 150) {
  if (rawStr.length <= maxLength) return rawStr;
  return rawStr.slice(0, maxLength) + "...";
}

// check if local storage is missing item
export function isStorageEmpty() {
  return (
    !localStorage.getItem("user_name") ||
    !localStorage.getItem("user_id") ||
    !localStorage.getItem("user_token")
  );
}

// login check and redirect
export function loginCheck() {
  if (isStorageEmpty()) {
    alert("You have not signed in!");
    window.location.replace("/login");
  }
}

// read user avatar from local storage, or use default avatar
export function generateAvatar() {
  if (!localStorage.getItem("user_thumbnail"))
    return "https://greloupis-images.s3.amazonaws.com/avatar-default-1.svg";

  return getSubstr(localStorage.getItem("user_thumbnail"));
}

// read video thumbnail, or use default thumbnail
export function generateThumbnail(thumbnail) {
  return !thumbnail || thumbnail === ""
    ? "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png"
    : thumbnail;
}

// generate uuid
let urlBase64 = (function () {
  let alphabet = { "+": "-", "/": "_" };

  return function urlBase64(buffer) {
    return buffer
      .toString("base64")
      .replace(/[+/]/g, function (token) {
        return alphabet[token];
      })
      .replace(/=+$/, "");
  };
})();

export function uuid() {
  let buffer = Buffer.alloc(16);
  Uuid.v4(null, buffer);
  return urlBase64(buffer);
}
