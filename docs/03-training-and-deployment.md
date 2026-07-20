# Phase 3: Training & Deployment

## ☁️ Step 5: Edge Impulse Studio & Data Collection

1. Go to **studio.edgeimpulse.com** and create a new project called `Scarecrow-Vision`.
2. Navigate to **Dashboard > Keys** and copy your API Key.
3. Install the Edge Impulse CLI on your Raspberry Pi:
```bash
sudo npm install -g edge-impulse-linux
```

4. Connect the Pi to your cloud project:
```bash
edge-impulse-linux --api-key <YOUR_API_KEY>
```

*(Select your microphone, and it will auto-detect your USB camera on `/dev/video0`).*

### Capturing & Annotating Training Data

Instead of hunting for animals, use the **Phone Monitor Trick**:

1. Open the **Data Acquisition** tab in the Edge Impulse web studio.
2. Search for images of dogs/monkeys on your smartphone.
3. Hold the phone screen up to the Pi's USB webcam and click **Start Sampling** to capture snapshots.
4. Go to the **Labeling queue**.

**Annotation Rule:** Draw bounding boxes *only* around the most consistent feature (e.g., the animal's face), rather than the whole body, which contorts into different shapes.

---

## 🏋️ Step 6: Training the FOMO Model

In Edge Impulse, create an Impulse with an **Image** processing block and an **Object Detection** learning block.

1. **Image Block:** This is where you configure **Data Augmentation**. Check the boxes to randomly flip, rotate, and add noise to your images. This artificially multiplies your dataset so the model doesn't overfit.
2. **Object Detection Block:** Select the **FOMO MobileNetV2 0.35** architecture.

---

## 🚀 Step 7: Deployment & Model Download

We must download the model as an `.eim` (Edge Impulse Model) executable file.

1. Navigate to your project directory and run the downloader on the Pi:
```bash
cd ~/scarecrow-vision
edge-impulse-linux-runner --download modelfile.eim
chmod +x modelfile.eim
```

---

## 🏃 Step 8: Running the Inference Pipeline

Ensure the `MODEL_FILE` variable in your code explicitly points to the local directory (`./modelfile.eim`) so Linux can find it.

Run the pipeline:

```bash
python3 src/scarecrow.py
```

If configured correctly, the Pi will initialize the camera and print bounding box coordinates and confidence scores to the terminal whenever a dog or monkey enters the frame!
