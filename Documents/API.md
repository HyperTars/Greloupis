# APIs Design
- [API Design](https://docs.google.com/spreadsheets/d/1hoKAh89rNywF343tU5lzeamFmidxdYJ39CW_uUCCRLw/edit?usp=sharing)

### User Auth

### Video
#### Upload Video
- Parameters
  - Name | Type | Note
  - apiKey | string | This will be used to, among other things, throttle users based on their allocated quota.
  - videoTitle | string | video title
  - videoDesc | string | (optional) video description
  - videoTags | string[] | (optional) video tags
  - videoCategory | string | category of video, e.g., Movie, Vlog, Song, News, Tech, etc.
  - videoLanguage | string | e.g., English, Mandarin, Hindi, etc.
  - videoStatus | string | e.g., public, private, limited share.
  - videoContents | stream | video to be uploaded.

- Returns
  - (default) 202 (request accepted), once the video encoding is completed the user is notified through email with a link to access the video. We can also expose a queryable API to let users know the current status of their uploaded video.

#### Stream Video
streamVideo(api_dev_key, video_id, offset, codec, resolution)

api_dev_key (string): The API developer key of a registered account of our service.
video_id (string): A string to identify the video.
offset (number): We should be able to stream video from any offset; this offset would be a time in seconds from the beginning of the video. If we support playing/pausing a video from multiple devices, we will need to store the offset on the server. This will enable the users to start watching a video on any device from the same point where they left off. codec (string) & resolution(string): We should send the codec andresolution info in the API from the client to support play/pause from multiple devices. Imagine you are watching a video on your TV’s Netflix
app, paused it, and started watching it on your phone’s Netflix app. In this case, you would need codec and resolution, as both these devices have a different resolution and use a different codec.

Returns: (STREAM)
A media stream (a video chunk) from the given offset.


### Watch History

### Search
#### Search Video
searchVideo(api_dev_key, search_query, user_location, maximum_videos
_to_return, page_token)

api_dev_key (string): The API developer key of a registered account of our service.
search_query (string): A string containing the search terms. user_location (string): Optional location of the user performing the search.
maximum_videos_to_return (number): Maximum number of results returned in one request.
page_token (string): This token will specify a page in the result set that should be returned.

Returns: (JSON)
A JSON containing information about the list of video resources matching the search query. Each video resource will have a video title, a thumbnail, a video creation date, and a view count.

### Video Op

### (TBD) Recommendation