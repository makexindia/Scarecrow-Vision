import cv2
import time
import threading
from flask import Flask, Response
from edge_impulse_linux.image import ImageImpulseRunner

app = Flask(__name__)

# --- Configuration ---
MODEL_FILE = './modelfile.eim'
CAMERA_PORT = 0

# --- Zero-Copy State Management ---
# Global pointers to the latest NumPy arrays. 
# Under the CPython GIL, pointer reassignment is an atomic operation.
latest_raw_frame = None
latest_detect_frame = None

# OS-level synchronization primitives to prevent CPU polling
detection_condition = threading.Condition()

def inference_producer():
    """Producer thread: Runs continuously, updates pointers, and signals consumers."""
    global latest_raw_frame, latest_detect_frame
    
    print("Starting inference engine...")
    with ImageImpulseRunner(MODEL_FILE) as runner:
        runner.init()
        camera = cv2.VideoCapture(CAMERA_PORT)
        
        while True:
            ret, frame = camera.read()
            if not ret:
                time.sleep(0.01) # Briefly yield to OS if camera buffers are empty
                continue
                
            # Point to the newest frame (atomic, no memory copy overhead)
            latest_raw_frame = frame
                
            # Run inference
            features, cropped = runner.get_features_from_image(frame)
            res = runner.classify(features)
            
            # Check for high-confidence detections
            if "bounding_boxes" in res["result"]:
                detection_made = False
                for bb in res["result"]["bounding_boxes"]:
                    if bb['value'] > 0.50:
                        detection_made = True
                        x, y, w, h = bb['x'], bb['y'], bb['width'], bb['height']
                        
                        # Mutate the 1-channel 'cropped' buffer in-place
                        cv2.rectangle(cropped, (x, y), (x + w, y + h), 255, 1)
                        cv2.putText(cropped, bb['label'], (x, y - 2), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, 0, 1)
                
                if detection_made:
                    # Update detection pointer and instantly wake any sleeping web threads
                    with detection_condition:
                        latest_detect_frame = cropped
                        detection_condition.notify_all()

def generate_raw_stream():
    """Consumer: Wakes blindly at 1Hz to grab whatever the latest frame pointer is."""
    global latest_raw_frame
    
    while True:
        # Grab the reference instantly to avoid locking the producer
        frame_ref = latest_raw_frame 
        
        if frame_ref is not None:
            # Encoding happens outside any locks
            ret, buffer = cv2.imencode('.jpg', frame_ref)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            
        time.sleep(1.0) # Hardware throttle for raw telemetry

def generate_event_stream():
    """Consumer: Sleeps at 0% CPU until the Condition lock is notified by a detection."""
    global latest_detect_frame
    
    while True:
        with detection_condition:
            # Block the thread completely until producer calls notify_all()
            detection_condition.wait() 
            frame_ref = latest_detect_frame
            
        # Lock is released. Encode the JPEG independently.
        if frame_ref is not None:
            ret, buffer = cv2.imencode('.jpg', frame_ref)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# --- Flask Routes ---
@app.route('/')
def index():
    # CSS handles the visual upscaling (image-rendering: pixelated) 
    # shifting the rendering cost from the Pi's CPU to the client's GPU.
    return '''
    <html>
        <body style="background-color: #111; color: #ddd; font-family: monospace;">
            <h2>Edge Inference Console</h2>
            <div style="display: flex; gap: 20px;">
                <div>
                    <h3>Event Stream (Real-Time Hits)</h3>
                    <img src="/event_feed" style="width: 480px; image-rendering: pixelated; image-rendering: crisp-edges; border: 1px solid #444;" />
                </div>
                <div>
                    <h3>Raw Telemetry (1 FPS Heartbeat)</h3>
                    <img src="/raw_feed" style="width: 320px; border: 1px solid #444;" />
                </div>
            </div>
        </body>
    </html>
    '''

@app.route('/raw_feed')
def raw_feed():
    return Response(generate_raw_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/event_feed')
def event_feed():
    return Response(generate_event_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    threading.Thread(target=inference_producer, daemon=True).start()
    print("\n--- Optimized Pipeline Active ---")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
