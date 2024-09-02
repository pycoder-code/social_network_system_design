# Tourist Social Network - System Design
## Functional requirements:
- registration of users
- publishing posts with images and descriptions
- viewing publications of other users
- comments on posts
- rating posts
- subscribe to other users and receive updates
- search for popular travel destinations
- feeds

## Non-functional requirements:
- DAU = 10 000 000
- availability 99,95% (4ч23м)
- geo CIS countries
- data is always stored
- no seasonality
- no more than 1c creation post
- no limit subscribe
- max 5 images one post
- max size image 500 кб
- max 3000 desc
- max 200 title
- one post - one day
- 5 post view - one day 
    

## load:
RPS(write):<br>
<code>
    10 000 000 * 1/86 400 = 116
</code>

RPS(read)<br>
<code>
    max_images_in_post = 5<br/>
    (10 000 000 * (6 * 5)/86 400 = 3500
</code>


Traffic(write)<br/>
<code>
images = 5 * 500кБ = 2500 KБ<br/>
desc = 3000 * 4Б  = 12 KB<br/>
title = 200 * 4Б = 0.8 КБ<br/>
116*(2500+12+0.8) = 290 000 КБ/с    
</code>


Traffic(read)<br/>
<code>
3500*(2500+12+0.8) = 8 794 800 КБ/с
</code>

Connections<br/>
<code>
10 000 000 * 0.1 = 1 000 000
</code>