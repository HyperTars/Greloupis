# DevOps-Project
![Python](https://img.shields.io/badge/python-3.8-blue)
![Flask](https://img.shields.io/badge/Flask-1.1.2-blue)
![Video.js](https://img.shields.io/badge/Video.js-7.8.4-blue)
![React](https://img.shields.io/badge/React-16.3.1-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4.0-blue)

- **`source` folder is currently unavailable, please check `source_rest_plus` to see our runnable [app.py](/source_rest_plus/app.py).**
- **We've just replaced REST-Plus with REST-X in `source_rest_plus`, we will gradually migrate them to the `source` folder in the future.**


### Project Proposal
- [Proposal](/Documents/Proposal.md)


### Designs
#### Coding Style: Naming Convention
- See full [Naming Convention](/Documents/NamingConventions.md)

#### Models Design (Entity)
- See full [Models Design](/Documents/Models.md)

#### Database Design
- See full [Database Design](/Documents/Database.md)

#### APIs Design
- Swagger API yml file [Swagger API file](/Documents/swagger.yml)
- Overview document [APIs Design](/Documents/APIs.md)

#### Components Design
1. Processing Queue: Each uploaded video will be pushed to a processing queue to be de-queued later for encoding, thumbnail generation, and storage.
2. Encoder: To encode each uploaded video into multiple formats.
3. Thumbnails generator: To generate a few thumbnails for each video.
4. Video and Thumbnail storage: To store video and thumbnail files in some distributed file storage.
5. User Database: To store user’s information, e.g., name, email, address, etc.
6. Video metadata storage: A metadata database to store all the information about videos like title, file path in the system, uploading user, total views, likes, dislikes, etc. It will also be used to store all the video comments.


### Tests
- See full [Test Cases](/Documents/Test.md)



### Contributors
- GitHub | Name | NetID
  --- | --- | ---
  [HyperTars](https://github.com/HyperTars) | Wenzhou Li | [wl2154](mailto:wl2154@nyu.edu)
  [MikeYan01](https://github.com/MikeYan01) | Linyi Yan | [ly1333](mailto:ly1333@nyu.edu)
  [FatBin](https://github.com/FatBin) | Xuanbin Luo | [xl2806](mailto:xl2806@nyu.edu)
