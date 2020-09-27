# DevOps-Project
![Python](https://img.shields.io/badge/python-3.8-blue)
![Flask](https://img.shields.io/badge/Flask-1.1.2-blue)
![Video.js](https://img.shields.io/badge/Video.js-7.8.4-blue)
![React](https://img.shields.io/badge/React-16.3.1-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0.21-blue)

### Project Proposal
- [Proposal](/Documents/Proposal.md)

### Requirements and Goals of the System

#### Functional Requirements:
1. Users should be able to upload videos.
2. Users should be able to share and view videos.
3. Users should be able to perform searches based on video titles.
4. Our services should be able to record stats of videos, e.g., likes/dislikes, total number of views, etc.
5. Users should be able to add and view comments on videos.


- Users must be able to create an account.
  - Each registered users must have their own personal account page.
  - Users must be able to login the system and logout from the system.
  - Users must be able to upload/delete videos in the system when they login.
  - Users must be able to add comments to videos in the system when they login.
  - Users must be able to watch videos in the system when they login or logout.
  - Users must be able to search videos/users/groups when they login or logout.
  - Users must be able to follow channels.
  - Users must be able like/dislike videos.
  - Users can like or dislike the videos, under this condition, the system should keep numbers of likes, dislikes, comments, views to present these number to users.

#### Non-Functional Requirements:
1. The system should be highly reliable, any video uploaded should not be lost.
2. The system should be highly available. Consistency can take a hit (in the interest of availability); if a user doesn’t see a video for a while, it should be fine.
3. Users should have a real time experience while watching videos and should not feel any lag.

- Not in scope: Video recommendations, most popular videos, channels, subscriptions, watch later, favorites, etc.

### Designs
#### Models Design (Entity)
- See full [Models Design](/Documents/Models.md)

#### Database Design
- See full [Database Design](/Documents/Database.md)

#### APIs Design
- See full [APIs Design](/Documents/APIs.md)

### Tests
- See full [Test Cases](/Documents/Test.md)

#### Components Design
1. Processing Queue: Each uploaded video will be pushed to a processing queue to be de-queued later for encoding, thumbnail generation, and storage.
2. Encoder: To encode each uploaded video into multiple formats.
3. Thumbnails generator: To generate a few thumbnails for each video.
4. Video and Thumbnail storage: To store video and thumbnail files in some distributed file storage.
5. User Database: To store user’s information, e.g., name, email, address, etc.
6. Video metadata storage: A metadata database to store all the information about videos like title, file path in the system, uploading user, total views, likes, dislikes, etc. It will also be used to store all the video comments.

### Contributors
- GitHub | Name | NetID
  --- | --- | ---
  [HyperTars](https://github.com/HyperTars) | Wenzhou Li | [wl2154](mailto:wl2154@nyu.edu)
  [MikeYan01](https://github.com/MikeYan01) | Linyi Yan | [ly1333](mailto:ly1333@nyu.edu)
  [FatBin](https://github.com/FatBin) | Xuanbin Luo | [xl2806](mailto:xl2806@nyu.edu)
