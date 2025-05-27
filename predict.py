from ultralytics import YOLO

model = YOLO("best.pt") 

# Predict with the model
results = model("./drug/test") 