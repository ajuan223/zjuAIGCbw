from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n-cls.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data="./drug", epochs=120, device=0,batch=32,workers=0,lr0=0.001)