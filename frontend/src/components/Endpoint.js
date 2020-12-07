export const HEROKU_ENDPOINT = "https://greloupis-backend.herokuapp.com";
export const LOCAL_ENDPOINT = "http://localhost:5000";
export const GITHUB_REPO = "https://https://github.com/HyperTars/Online-Video-Platform";
export const S3_RAW_VIDEO_BUCKET = "https://vod-watchfolder-ovs-lxb.s3-us-west-1.amazonaws.com/";
export const S3_AVATAR_BUCKET = "https://greloupis-images.s3.amazonaws.com/avatar-";
export const S3_VIDEO_THUMBNAIL_BUCKET = "https://greloupis-images.s3.amazonaws.com/thumbnail-";

export function backendPoint() {
  if (process.env.NODE_ENV === "development") return LOCAL_ENDPOINT;
  return HEROKU_ENDPOINT;
}