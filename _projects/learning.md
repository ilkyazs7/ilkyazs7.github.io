---
title: Learning
number: '10'
section: research
theme: Machine
year: 2023
period: 2022–2023 Spring
type: Academic
mode: Individual
institution: METU
program: Architecture
course: BS723 Machine Learning Applications in Architecture
city: Ankara
country: TR
instructors:
- Prof. Dr. Arzu Gönenç Sorguç (studio coordinator)
- Müge Krusa Yemiscioglu
- Ozan Yetkin
- Sevval Cologlu
cover: /assets/images/learning/200.png
hidden: false
redirect_from:
- /[10]-learning/
- /projects/10-learning/
summary: ''
blocks:
- type: heading
  text: '[10.i] Unrehearsed Compositions'
- type: text
  text: The project aims to generate a machine learning model that generates audio with predicted audio features of pose data in dance sequences
- type: text
  text: |-
    **problem -** Dance and music are two simultaneous entities that the body fits into when moving. The beat, genre, speed, volume, and many more features of audio affect how a dance choreography is shaped and executed. This is a phenomenon that is affected by many parameters including the genre of the dance, the expressional quality of the dancer themselves, and so on. In that sense, with this project, the relationship between audio and dance is understood through audio’s power to generate how a dance is shaped and it is reversed to investigate how dance itself can generate audio and music. Shortly, the
    problem focuses on how movement in relation to dancing generates sound.
- type: text
  text: '**material -** dance video sequences with audio files/feautures'
- type: text
  text: '**model -** a model that predicts the audio features of pose data in a dance/movement sequence'
- type: embed
  url: https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1925580818&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true
- type: embed
  url: https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1925580815&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true
- type: embed
  url: https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1925580806&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true
- type: embed
  url: https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/1925580800&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true
- type: image
  src: /assets/images/learning/ilkyazsarimehmetoglu-bs723-finalpresentation-4.jpg
- type: text
  text: The machine learning model was aimed as a model that predicts the audio features of pose data in a dance/movement sequence. In that sense, the model sequentially follows these steps as can be seen in the flow chart and model diagram.
- type: text
  text: Generation with prediction – Another goal for the project was to generate a real-time model to interact with to generate sound while dancing in a camera target or Kinect. This was a further goal of the project which was not adapted to the existing data but rather a simulation to be adapted to a real-time model of pose estimation.
- type: image
  src: /assets/images/learning/screenshot-2024-09-16-084834.png
- type: caption
  text: 1. Problem Definition
- type: text
  text: The problem of this project was to look further into audio generation through dance. Dance and music are two simultaneous entities that the body fits into when moving. The beat, genre, speed, volume, and many more features of audio affect how a dance choreography is shaped and executed. This is a phenomenon that is affected by many parameters including the genre of the dance, the expressional quality of the dancer themselves, and so on. In that sense, with this project, the relationship between audio and dance is understood through audio’s power to generate how a dance is shaped and it is reversed to investigate how dance itself can generate audio and music. Shortly, the problem focuses on how movement in relation to dancing generates sound.
- type: image
  src: /assets/images/learning/screenshot-2024-09-16-084841.png
- type: caption
  text: 2. Data & Interpretation
- type: text
  text: For this project, chosen materials are dance video sequences that contain both instances of the moving body of a single person – executing a double choreography of the Break Dance genre and its related audio file. The video sequence is deconstructed as image sequences – by second and the audio file – is extracted into its features by second.
- type: text
  text: 2.1. Image Data - The image sequences were used for Pose Estimation to understand the coordinates of the moving body in relation to the sound data at that particular second. In that sense, for a 128-second dance performance, 128 instances of that sequence were extracted and implemented. The image sequence portion of the video was understood through the specific location of the parts of the dancer’s moving body – both “hinges” of the body such as the knee, elbow, and so on, and other features like the organs on the face and their left, right, upper, bottom corners. Orientation of the body parts, their transitions, and the orientation of facial expressions were taken into consideration with the definition of the locations in a particular sequential second.
- type: text
  text: 2.2. Audio Data – The audio data was gathered in the wav format to be broken down into its volume, spectrogram, and melodic spectrogram features. For the prediction, for this part of the project, melodic spectrogram values were predicted and later on, implemented as audio. In this part, the melodic spectrogram value extraction had specifications as (sample rate=22520, window=520) which are default values that are derived from the nature of the implemented wav file. The raw audio files went into the preparation of such kind – to work on the spectrogram values in further stages.
- type: text
  text: 2.3. Compatibility - The compatibility of the two data images and sound was understood through their ‘time’ feature. The audio data implemented time/frequency as an output where the image data was constructed through time. In the end, it was important that both of the lists shared the same list length.
- type: image
  src: /assets/images/learning/ilkyazsarimehmetoglu-bs723-finalpresentation-5.jpg
- type: image
  src: /assets/images/learning/audio-1.png
- type: image
  src: /assets/images/learning/spectogram-for-audio-1.png
- type: image
  src: /assets/images/learning/mel-spectogram.png
---
