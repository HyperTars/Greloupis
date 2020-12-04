[![logo](greloupis-horizontal.png)](https://greloupis-frontend.herokuapp.com/)

# Greloupis - TestFlow

## Table of Content
- [Greloupis - TestFlow](#greloupis---testflow)
  - [Table of Content](#table-of-content)
    - [Search](#search)
    - [User](#user)
    - [Video](#video)
    - [Error Pages](#error-pages)
  - [Scripts](#scripts)

### Search
- Top (Trending)
- Search public video
- Search public & private users

### User    
- Register, Login, Logout
- Login, Logout
- Upload video (should be done first, check it later)
- Check video uploaded, histories
- Check private user profile
- Check private video
- Update user profile
- Update video

### Video
- Video Playback, switch resolution
- Video Replay
- Last Position
- Like, Dislike, Star
    - Like then dislike
    - Cancel
- Comment
    - Delete comment

### Error Pages
- Access private video (403)
- Access deleted video (404)
    - Access public then access again after deleting it
- Run local without backend (500)


## Scripts

Lots of people nowadays watch videos online. 

i Videos are typically transcoded and sent via content delivery network. 

ii Besides, users may not only want to watch videos, but also want to publish their own videos and share with others. People will make some operations, for example posting likes, leaving their comments or simply adding videos to their favorite lists. 

iii Finally, users expect to have easy and clean video watching experience, typically this means that the UI of the website should be user-friendly, and there should not be any annoying advertisement. 

So, based on these points, we designed a great online video platform which satisfies all needs we mentioned before. Let’s have a look. 

(1. Search)

i (Top list) When users visit our home page, they will see the top 10 hit videos of the whole website. The sorting index is the video view count, so users can easily know what are the recent trending videos.

ii (Smart Search) Then we talk about search. Simply click on the search button, we will show users all public videos and users. Our search is smart because it can match the keywords with multiple attributes. For example, we can search videos by title, tags, categories and channel. Let’s say we search “shanghai” and we can see that 1 video is matched by video title. We then search “technology” and see that 5 videos are matched because they are all related to technology category.

(2. User)

i (User create, login, logout) Now let’s create a new user called demoUser… And now we have logged in, since we can visit the user profile page now. The left part is user’s personal information, and the right part is several collections, including uploaded video collections, watched collections, starred collections, etc. Let’s log out and check normal log in function… also works. 

ii We may update some user information. For example lets upload an avatar, and also modify our user status to “public”, so other users can see my profile.

(3. Video)
i (Video upload) Suppose we want to upload a video now. We have listed all the video format we support, so please ensure that the uploaded video format is in the range. I upload a test video, and click “Publish”. You can see that we have a message box on the top and an upload progress bar… Now it’s finished. 

ii (Video update) So now, users will be prompted to update the video information immediately. Meanwhile, our video has been uploaded to AWS and it’s now being transcoded. We need to wait several minutes until the video is ready for streaming. Let’s not update but return to user profile to check our video status.. You can see that the video is marked as “pending”, and if we clicked into the video it will show that “the video is being transcoded and cannot be played now”. OK now back to the video update, click “manage video” to make some changes, notice that we have tooltips to instruct users how to correctly input information…

iii (Video play 1) Now we see that video status is “public”, which means that video is ready to be played and all users have access to this video. Click into the video. We can see the information we input just now. Let’s start to play…	
    i You can see that we are using video streaming so we will just retrieve part of the video.
    
    ii We have several control buttons, like play / pause, rewind by 10 seconds, volume control, full screen, and resolution switching. Users can even customize keyboards shortcuts to control videos.
	
    iii Our website can remember user’s watching process. For example we have now played {number} seconds... Let’s close this video and return back, the video will automatically switches to this number and is ready to be played from here. (We can even try again…)
    
iv (Video play 2) Now lets talk about video operations. We open another video(Shanghai). Still you can see the video can be played smoothly. Users can post like, dislike, or they can star this video to their collections. They can even write some comments, and of course they can be deleted afterwards. We now get back to the user profile, and previous operations have been saved.

(4. Access)
We now want to talk about accessibility, because we want to give user enough privacy and also ensure the safety of our website.

i (User access)  The first part is user access. As mentioned earlier, user can either set status as “public” or “private”. Let’s visit a private user. You can see that only user avatar, name and public videos will be displayed, while other information will be hidden.

ii (Video access) Also video can be set as private, only video author can see the video. If other users try to access, 403 error will be returned.

iii (Random access) If users try to randomly access a URL of our website, 404 error will be returned.

(5. Delete)

Finally, if users want to delete a video, they can go to manage video and delete it. But please be careful to do so! Now both video and its related operations is deleted. Users can even delete their accounts. But again, please be careful!

That’s the end of our presentation. Thank you!