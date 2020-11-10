import moment from "moment";

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
