import moment from "moment";

// convert timestamp to relative time
export function convertToRelativeTime(timestamp) {
  let t = moment(timestamp).format();
  return moment(t).startOf("minutes").fromNow();
}

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

export function dateConvert(time) {
  let d = new Date(time),
    month = "" + (d.getMonth() + 1),
    day = "" + d.getDate(),
    year = d.getFullYear();

  if (month.length < 2) month = "0" + month;
  if (day.length < 2) day = "0" + day;

  return [year, month, day].join("-");
}

export function getSubstr(rawStr) {
  if (rawStr == null) return rawStr;

  return rawStr.slice(1, -1);
}

export function ellipsifyStr(rawStr, maxLength = 150) {
  if (rawStr.length <= maxLength) return rawStr;
  return rawStr.slice(0, maxLength) + "...";
}

export function isStorageEmpty() {
  return (
    !localStorage.getItem("user_name") ||
    !localStorage.getItem("user_id") ||
    !localStorage.getItem("user_token")
  );
}

export function loginCheck() {
  if (isStorageEmpty()) {
    alert("You have not signed in!");
    window.location.replace("/login");
  }
}

export function generateAvatar() {
  if (!localStorage.getItem("user_thumbnail"))
    return "https://greloupis-images.s3.amazonaws.com/avatar-default-1.svg";

  return getSubstr(localStorage.getItem("user_thumbnail"));
}

export function generateThumbnail(thumbnail) {
  return !thumbnail || thumbnail === ""
    ? "https://gw.alipayobjects.com/zos/rmsportal/mqaQswcyDLcXyDKnZfES.png"
    : thumbnail;
}
