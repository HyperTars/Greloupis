[![logo](greloupis-horizontal.png)](https://greloupis-frontend.herokuapp.com/)

# Online Video Platform
- Proposal of An Online Video Platform
- NYU CS-GY 9223 DevOps

## Overview
- Nowadays, video has penetrated into every aspect of our lives. We can follow videos to learn how to cook, play musical instruments, enjoy the beauty of various countries, learn knowledge, watch the news, and see how other people live across the world. More or less, video has become an indispensable part of our lives.
- Our project is dedicated to building an online video playing platform, including a variety of cutting-edge and popular features like:
  - Highly available online video player
  - Efficient search system
  - User registration, login and authority system
  - User reviews system
  
- The primary purpose of this project is to create an online video viewing system. In addition, we have also thought and reflected on similar products already on the market. 
  - Netflix is a completely B2C video content provider. The video is completely uploaded by the provider and provided to users. Similarly, there are streaming media providers such as HBO Max and Disney+. They lack or essentially do not allow users to upload their own videos. However, in our opinion, users can produce very high-quality videos nowadays. Many vlog bloggers, short film teams, etc. have professional equipment, and they can shoot amazing pictures. They should have a way to directly show their works to other users without the engagement of publishers. 
  - Some bullet screen video websites (such as niconico, JP. and bilibili, CN.) provide good user communication experience. However, they do not have strong background transcoding algorithms, distributed content delivery system and online adaptive streaming coding algorithms like YouTube and Netflix. 
  - Based on both points mentioned above, our long-term plan is to combine the advantages of all the above video sites to create an online video playback site that meets the needs of users' actual experience in an ultimate way.

### Requirements and Goals of the System

#### Functional Requirements:
- **Users must be able to:**
  - **Account**
    - Create an account.
    - Login the system.
    - Logout from the system.
    - Have own personal account page when logged in.
    - Set account (profile) public and private when logged in.
    - Close account when logged in.
  - **Videos**
    - Upload videos in the system when logged in.
    - Delete videos in the system when logged in.
    - Set videos public or private when logged in.
    - Search videos/users.
    - Play (watch) videos.
    - View total number of views/comments/likes/dislikes/stars/shares to videos.
    - Add comments/likes/dislikes/stars/shares when logged in.
    - View own watch histories/comments/likes/dislikes/stars/shares when logged in.
  
#### Non-Functional Requirements:
- The system should be highly reliable, any video uploaded should not be lost.
- The system should be highly available. Consistency can take a hit (in the interest of availability); if a user doesn’t see a video for a while, it should be fine.
- Users should have a real time experience while watching videos and should not feel any lag.

- *Not in scope*: Video recommendations, subscriptions, watch later, etc.


## Assumptions

- We assume that all videos we collect from the Internet are legal and valid
- We assume that some users will actively contribute their experiences and reviews to the system after they watch a video
- We assume that users will not arbitrarily give their reviews to a video

## Architecture Design

![Architecture Design Diagram](./ArchitectureDesign_resize.png)

## Technology Stack

### Front-end

- We will use `React.js`, which is a component-based JavaScript library for building user interfaces. See [React.js](https://reactjs.org/) for more details.

### Back-end

- We will use `Flask-Rest X`, which is an extension for Python Flask framework that adds support for quickly building REST APIs. See [Flask-Rest X](https://flask-restx.readthedocs.io/en/latest/) for more details.

### Designs: Naming Conventions
- See full [Naming Conentions](NamingConventions.md)

- Python PEP 8
  - Packages: `package_name`
  - Modules: `module`(preferable to stick to 1) or `module_name`
  - Classes: `UpperCaseCamelCase`
  - Exceptions: `ValueError`
  - Global (module-level) Variables: `GLOBAL_VAR`
  - Instance Variables: `instance_var`, `_non_public`, `__mangled`
  - Methods: `method_name`, `_non_public`, `__mangled`
  - First Method Argument: `self` for instance methods, `cls` for class methods.
  - Functions: `function_name`
  - Constants: `CONSTANTS_NAME`

- Database & Model
  - Models: `ModelName`
  - MongoDB: `all_lower_case`

### Designs: Models
- [Models Design](Models.md)

### Designs: APIs
- [APIs Design](APIs.md)

### Designs: Database
- [Database Design](Database.md)

### Testing
- For unit test, we will use:
  - `unittest`, to test Python code
  - `Jest`, to test React code

- We will also use linters listed below to enforce code styling:
  - `flake8` for Python
  - `eslint` for React

- Test Cases
  - [Test Cases](Test.md)

### CI/CD

- We will use `GitHub Action`, which provides convenient continuous integration & deployment services.

### Deploy and Monitor

- We will use `Docker` to set up container for our application for cloud deployment and monitoring in the futurue.

## External API integrations and Data Sources

We will use external data from some mainstream online video platforms, including:

- [Netflix](https://www.netflix.com/)
- [Youtube](https://www.youtube.com/)
- [Bilibili](https://www.bilibili.com/)

## Future Works
- We might allow users to post live comment (danmaku).
- We might allow users to block certain users.
