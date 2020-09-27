# Database Design

Video metadata storage - MySql
Videos metadata can be stored in a SQL database. The following information should be stored with each video:
VideoID
Title
Description
Size
Thumbnail Uploader/User
Total number of likes Total number of dislikes Total number of views

For each video comment, we need to store following information:
CommentID VideoID
UserID Comment TimeOfCreation

User data storage - MySql
UserID, Name, email, address, age, registration details etc.