import os.path

from django.http import JsonResponse, StreamingHttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from computervision.detection.anomaly import AnomalyDetection
from django.core.exceptions import ValidationError
from backend.settings import BASE_DIR
import cv2
import asyncio
from PIL import Image

# Create your views here.
class DetectAnamolyView(View):
    def get(self, request, *args, **kwargs):
        source_url = request.GET.get('url', None)
        if not source_url:
            return HttpResponseNotFound()

        if source_url.startswith("http://localhost:8000") or source_url.startswith("http://127.0.0.1:8000"):
            if "sifal" in source_url:
                source_url = "/Users/sureshchand/Desktop/Personal/nymna/backend/static/sifal.mp4"
            elif "maitighar" in source_url:
                source_url = "/Users/sureshchand/Desktop/Personal/nymna/backend/static/maitighar.mp4"

        anomaly_detection = AnomalyDetection(source_url, classes=["person"], conf=0.5)
        return StreamingHttpResponse(anomaly_detection.get_frame_trims(), content_type='multipart/x-mixed-replace; boundary=frame')


class PlayerView(View):
    async def stream_images(self, image_files, frame_rate=0.001):
        for image_file in image_files:
            print(image_file)
            frame = cv2.imread(image_file, 1)
            if frame is None:
                continue

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Yield the frame for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            await asyncio.sleep(0.05)

    async def get(self, request, *args, **kwargs):
        folder_name = kwargs.pop('folder', None)
        if not folder_name:
            return HttpResponseNotFound()

        folder_path = os.path.join(BASE_DIR, "static", folder_name)
        if not os.path.exists(folder_path):
            return HttpResponseNotFound()

        image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        sorted_files = sorted(image_files, key=lambda x: os.path.getctime(x))
        return StreamingHttpResponse(self.stream_images(sorted_files), content_type='multipart/x-mixed-replace; boundary=frame')
