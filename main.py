from vom.components.vom import VOM

# MODEL SETUP
#model = torch.hub.load('.', 'custom', path='runs/train/nano6/weights/best.pt', device='cpu', source='local')
#model.conf = 0.5

# FRAME RATE SETUP
#frame_rate = 15
#frame_counter = 0
#if frame_counter % frame_rate == 0:

# IMAGE SETUP
#frame = Image.fromarray(frame)
#frame = frame.resize((1080,720))
#results = model(frame)

#results.ims
#results.render() #??
#im = results.ims[0]
##im = Image.fromarray(im)
#print(results)
#show('stream',im)

source = 0 # WEBCAM
source = 'vom/DATA/videos/overweg_AA.mp4'
#source = 'vom/DATA/videos/overweg_BA.mp4'
#source = 'vom/DATA/videos/oss.mp4'

monitor = VOM(source)
monitor.run()