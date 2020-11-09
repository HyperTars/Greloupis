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
