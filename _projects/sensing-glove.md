---
title: 'Sensing Through the Body: Glove for AR Interaction'
number: '00'
section: research
theme: 'Soft Intelligence: Embodied Mind'
year: 2025
period: 2025–2026 Fall
type: Academic
mode: Group
institution: Massachusetts Institute of Technology
institution_short: MIT
course: 3.173 Computing Fabrics
city: Cambridge
country: US
collaborators:
- Clara Emmerling
cover: /assets/images/sensing-glove/thumbnail.png
hover_image: /assets/images/sensing-glove/img-20251208-wa0052.jpg
hidden: false
redirect_from:
- /[00]-sensing-through-the-body-glove-for-ar-interaction/
- /projects/00-sensing-glove/
summary: Human–machine interfaces (HMIs) are increasingly designed to incorporate sensing and haptic output, creating more intuitive and immersive interactions across fields such as healthcare, robotics, and AR/VR. Developments in soft electronics are accelerating this shift, enabling interactions that move beyond rigid devices toward soft, wearable systems.
blocks:
- type: image
  src: /assets/images/sensing-glove/img-20251208-wa0052.jpg
- type: text
  text: Sensing capabilities can be seamlessly integrated into textile-based wearables through digital machine knitting and the incorporation of functional materials. This project focuses on designing a system with an integrated Neural Network fiber for an astronaut’s inner glove which can provide gesture detection for **complex Augmented Reality missions in lunar environments**. The outer glove makes it significantly difficult for performing finger moving gestures or contacting to other surfaces of interactions like buttons. By integrating gesture detection the need for providing a contact surface is eliminated.
- type: text
  text: |-
    **Astronauts Outer Glove:**
    Thick insulated shell, difficult to use
    delicate instruments + equipment
- type: text
  text: |-
    **Astronauts Inner Glove:**
    Smart + gesture-detecting layer used
    for navigation and communication?
- type: image
  src: /assets/images/sensing-glove/screenshot-2026-01-02-130647.png
- type: image
  src: /assets/images/sensing-glove/screenshot-2026-01-02-130652.png
- type: text
  text: The main design concept for the glove was to make it modular and adaptable for different use scenarios and users as there is a need for customization.
- type: image
  src: /assets/images/sensing-glove/diagrams-all-converted.png
  caption: system design diagram
- type: gallery
  items:
  - src: /assets/images/sensing-glove/diagrams-all-converted-01.png
  - src: /assets/images/sensing-glove/diagrams-all-converted-02.png
  caption: 'design idea and implementation: modularizing the glove [01], schematic glove system [02]'
- type: heading
  text: design - 1
- type: gallery
  items:
  - src: /assets/images/sensing-glove/diagrams-all-converted-04.png
  - src: /assets/images/sensing-glove/screenshot-2026-01-02-134348.png
  caption: schematic & prototype
- type: heading
  text: design - 2
- type: gallery
  items:
  - src: /assets/images/sensing-glove/diagrams-all-converted-05.png
  - src: /assets/images/sensing-glove/screenshot-2026-01-02-134647.png
  caption: schematic & prototype
- type: heading
  text: knit prototyping
- type: caption
  text: on domestic single bed silvereed
- type: gallery
  items:
  - src: /assets/images/sensing-glove/screenshot-2026-01-02-134942.png
  - src: /assets/images/sensing-glove/screenshot-2026-01-02-134948.png
  caption: first prototype [01]
- type: gallery
  items:
  - src: /assets/images/sensing-glove/screenshot-2026-01-02-135000.png
  - src: /assets/images/sensing-glove/screenshot-2026-01-02-134955.png
  caption: second [02] third [03]
- type: image
  src: /assets/images/sensing-glove/screenshot-2026-01-02-135902.png
  caption: stitch pattern generation for complete glove garment
- type: heading
  text: knit prototyping stages
- type: image
  src: /assets/images/sensing-glove/screenshot-2026-01-02-140626.png
  size: small
  caption: cast-on [t0]
- type: gallery
  items:
  - src: /assets/images/sensing-glove/screenshot-2026-01-02-140632.png
  - src: /assets/images/sensing-glove/screenshot-2026-01-02-140637.png
  caption: insertion of the NN fiber [t1]
- type: image
  src: /assets/images/sensing-glove/screenshot-2026-01-02-140641.png
  size: small
  caption: and carrying it through the glove skin [t2]
- type: heading
  text: in-fiber neural network (NN)
- type: text
  text: the embedded fiber has an accelerometer that is trained for gesture recognition of different behaviors. the two designs had different gestures for recognition. design 1 gestures were **curl [1] and idle [2]**. whereas for design 2 the gestures were **curl [1], idle [2] and right swipe [3]**.
- type: caption
  text: training set strategy
- type: text
  text: |-
    about 60 samples per gesture class
    samples with different time ranges (from 0.5 to 4s)
- type: image
  src: /assets/images/sensing-glove/screenshot-2026-01-02-142316.png
  caption: design - 1 metrics
- type: image
  src: /assets/images/sensing-glove/screenshot-2026-01-02-142404.png
  caption: design - 2 metrics
- type: image
  src: /assets/images/sensing-glove/flex-pcb-routing-diagram.png
  caption: electronics scheme diagram for embedded pcb
- type: heading
  text: AR interface used with the Sensing Glove
- type: video
  src: /assets/images/sensing-glove/0000.mp4
  caption: 'used software: Unity gesture legend: curling [create element], right swipe [delete element]'
- type: image
  src: /assets/images/sensing-glove/screenshot-2026-01-02-at-10-30-02pm.png
  caption: 'system development for intelligent navigation in lunar environments: AR interface prototype designed by Qilmeg Doudatcz'
- type: image
  src: /assets/images/sensing-glove/img-20251208-wa0048.jpg
  caption: extra +
- type: image
  src: /assets/images/sensing-glove/websiteknitsamples.png
  caption: diverse patterns that could be incorporated in the glove modules for diverse haptics, texture library and tactility
- type: text
  text: The samples showcase differrent patterns that introduce 3D extrustions, some introduce local climaxes within regions of pattern introduction whereas some introduce more homogenous textures throughout the samples. These are couple examples that have just 3 different needle actions executed on the Silvereed manual knitting machine with DesignaKnit software.
- type: gallery
  items:
  - src: /assets/images/sensing-glove/whatsapp-image-2025-12-08-at-04-11-51-1.jpeg
  - src: /assets/images/sensing-glove/whatsapp-image-2025-12-08-at-04-11-51.jpeg
  - src: /assets/images/sensing-glove/whatsapp-image-2025-12-08-at-04-11-53-1.jpeg
  - src: /assets/images/sensing-glove/whatsapp-image-2025-12-08-at-04-11-53.jpeg
---
