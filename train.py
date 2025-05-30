from ultralytics import YOLO

model = YOLO("yolo11n-cls.pt")
#这里可以更改训练参数（batch  epoch  device  lr0等） 但是worker不建议改，可能会报错，这个是加载图片时的线程，和模型性能关系不大
results = model.train(data="./drug", epochs=120, device=0,batch=32,workers=0,lr0=0.001)