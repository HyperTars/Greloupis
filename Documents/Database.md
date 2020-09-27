# Database Design

**Video metadata storage - MySql**
Videos metadata can be stored in a SQL database. The following information should be stored with each video:
VideoID
Title
userID
categoryID
Description
Size
likes / dislikes
number of displayed
Thumbnail Uploader/User
upload date
Total number of likes Total number of dislikes Total number of views
contentStatus(pending, processed, fail, rejected)
status(public, private, deleted)
quality(low, middle, high)

**For each video comment, we need to store following information:**
CommentID VideoID
UserID Comment CommentDate


**User data storage - MySql**
UserID, Name, email, address, age, registration date, last login
status(public, private, closed)