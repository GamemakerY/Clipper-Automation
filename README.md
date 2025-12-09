# EchoClip (WIP)

A complete automated solution to convert long-form content to multiple short-form clips and to upload them with just a single click.

This is what the script does right now:

Autonomously downloads a video with the given link
Gets the transcripts of the video, feeds it to AI which generates a list of ideas along with exact timestamp. The list is exported as a json file.
Uses that data to crop it in a short format and trim the video into segments and then add captions on top of it.

Right now, each of the steps are separate functions which have to be manually parsed. It shall all be unified in the final version.


---

## Status: Work In Progress (WIP)

This project is currently under active development. Expect changes, bugs, and missing features. Contributions and feedback are welcome!

---

<img width="725" height="636" alt="image" src="https://github.com/user-attachments/assets/af9fa2ee-3f95-48c2-824f-7944dc3d0913" />


<div align="center">
  <a href="https://moonshot.hackclub.com" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/35ad2be8c916670f3e1ac63c1df04d76a4b337d1_moonshot.png" 
         alt="This project is part of Moonshot, a 4-day hackathon in Florida visiting Kennedy Space Center and Universal Studios!" 
         style="width: 100%;">
  </a>
</div>
