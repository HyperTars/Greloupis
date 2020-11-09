import moment from "moment";
const numeral = require("numeral");

// function to convert numbers
// 1000 -> 1k && 1100 -> 1.1k and so on
// abbreviate all nums in an array
export function abbreviateAllNumsInArr(arr) {
  arr.forEach((obj) => {
    abbreviateAllNumsInObj(obj);
  });
}

// abbreviate all nums in an obj
export function abbreviateAllNumsInObj(obj, exception) {
  for (let prop in obj) {
    if (prop === exception) {
      obj[prop] = numeral(obj[prop]).format("0,0");
    }
    if (typeof obj[prop] == "number") {
      obj[prop] = abbreviateNum(obj[prop]);
    }
  }
}

// abbreviate nums individually
export function abbreviateNum(num) {
  if (
    (num >= 1000 && num < 1100) ||
    (num >= 10000 && num < 10100) ||
    (num >= 100000 && num < 100100) ||
    (num >= 1000000 && num < 1100000) ||
    (num >= 10000000 && num < 10100000)
  ) {
    return numeral(num).format("0a");
  } else if (num < 1000) {
    return num;
  }
  return numeral(num).format("0.0a");
}

// fetch request
export function fetchRequest(methodType, url, func = console.log, body = null) {
  if (methodType === "GET") {
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        func(data);
      })
      .catch((err) => console.error("YOU GOT AN ERROR: ", err));
  } else if (methodType === "POST") {
    // debugger;
    fetch(url, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "content-type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        func(data);
      })
      .catch((err) => console.error("YOU GOT AN ERROR: ", err));
  } else if (methodType === "DELETE") {
    fetch(url, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        func(data);
      })
      .catch((err) => console.error("YOU GOT AN ERROR: ", err));
  } else if (methodType === "PUT") {
    fetch(url, {
      method: "PUT",
    })
      .then((response) => response.json())
      .then((data) => {
        func(data);
      })
      .catch((err) => console.error("YOU GOT AN ERROR: ", err));
  }
}

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
