import numpy as np 
import cv2
#read the NetFromcaffe 
cvNet = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt','MobileNetSSD_deploy.caffemodel')
#print(cvNet)
image_path = 'example_05.jpg'
intial_confidence=0.25
# Input image
image = cv2.imread(image_path)
(h, w) = image.shape[:2]
#print(h)
#print(w)
# Use the given image as input, which needs to be blob(s).
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.006666667, (300, 300), 150, swapRB=True)
cvNet.setInput(blob)
print("Blob shape: {}".format(blob.shape))
print(blob)
# Runs a forward pass to compute the net output
detections = cvNet.forward()
N=np.arange(0, detections.shape[2])
print("detection shape:[1 ,1, N , 7]")
print(detections)
#confidence = inference_results[0, 0, i, 2]   # extract the confidence (i.e., probability) 
#idx = int(inference_results[0, 0, i, 1])   # extract the index of the class label
#boxPoints = inference_results[0, 0, i, 3:7]
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
# loop over the detections
for i in np.arange(0, detections.shape[2]):
	# extract the confidence (i.e., probability) associated with the
	# prediction
	confidence = detections[0, 0, i, 2]

	if confidence > intial_confidence:
		# extract the index of the class label from the `detections`,
		# then compute the (x, y)-coordinates of the bounding box for
		# the object
		idx = int(detections[0, 0, i, 1])
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		# display the prediction
		label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
		print("[INFO] {}".format(label))
		cv2.rectangle(image, (startX, startY), (endX, endY),
			COLORS[idx], 2)
		y = startY - 15 if startY - 15 > 15 else startY + 15
		cv2.putText(image, label, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

# show the output image
cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows() 

