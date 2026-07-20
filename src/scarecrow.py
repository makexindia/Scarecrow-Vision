import cv2
import time
from edge_impulse_linux.image import ImageImpulseRunner

# --- Configuration ---
MODEL_FILE = './modelfile.eim'
CAMERA_PORT = 0
CONFIDENCE_THRESHOLD = 0.60
ACTION_COOLDOWN = 5.0
CPU_REST_TIME = 0.25  # Sleep for 250ms between runs to keep the Pi 2 cool

print(f'Loading model: {MODEL_FILE}')

last_trigger_time = 0

with ImageImpulseRunner(MODEL_FILE) as runner:
    try:
        model_info = runner.init()
        print(f"Loaded runner for {model_info['project']['owner']} / {model_info['project']['name']}")
        print("Pipeline is active. Waiting for targets... (Press Ctrl+C to stop)")
        
        camera = cv2.VideoCapture(CAMERA_PORT)
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        while True:
            # 1. Flush the stale frames that arrived while the CPU was sleeping.
            # Reading 4 times rapidly drops the old buffer frames.
            for _ in range(4):
                camera.read()
            
            # 2. Grab the freshest frame for actual processing
            ret, frame = camera.read()
            if not ret:
                time.sleep(0.01)
                continue
                
            # 3. Run Inference on the fresh frame
            features, _ = runner.get_features_from_image(frame)
            res = runner.classify(features)
            
            # 4. Check for valid targets
            if "bounding_boxes" in res["result"]:
                for bb in res["result"]["bounding_boxes"]:
                    if bb['value'] > CONFIDENCE_THRESHOLD:
                        current_time = time.time()
                        
                        # 5. Debounce logic: Only act if the cooldown period has passed
                        if (current_time - last_trigger_time) > ACTION_COOLDOWN:
                            print(f"\n[ALERT] {bb['label'].upper()} detected! (Confidence: {bb['value']:.2f})")
                            
                            # ---------------------------------------------------------
                            # TODO: Phase 2 - Network Action for ESP8266 + pyotp
                            # ---------------------------------------------------------
                            
                            last_trigger_time = current_time
                            
            # 6. Put the CPU to sleep to prevent thermal throttling
            time.sleep(CPU_REST_TIME)
                            
    except KeyboardInterrupt:
        print("\nStopping the pipeline...")
    finally:
        if runner:
            runner.stop()
        if 'camera' in locals() and camera.isOpened():
            camera.release()
