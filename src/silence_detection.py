#!/usr/bin/python

#import matplotlib.pyplot as plt
import numpy
import scipy.io.wavfile as wav
import sys
import wave

#Variable inputs to Silence Detection module
WindowSize = 5		#milliseconds
SilenceThreshold = 350 	#milliseconds

try:
	#Read wav file	

	(SamplingRate,Wavdata) = wav.read("../wav/" + sys.argv[1] );
	TotalSamples = len(Wavdata);

	Wavobj = wave.open("../wav/" + sys.argv[1],'r');
	BytesPerSample = Wavobj.getsampwidth();
	SamplesPerFrame = int((SamplingRate*WindowSize)/1000); 		#Samples per frame = (samples/second)*(seconds/frame)
	
	#Normalize data to range [-1,+1)
	
	if BytesPerSample == 1:
		Wavdata = (Wavdata-128)/128.0;
	elif BytesPerSample == 2:
		Wavdata = Wavdata/32768.0;
	elif BytesPerSample == 3:
		Wavdata = Wavdata/(2.0^23);
	elif BytesPerSample == 4:
		Wavdata = Wavdata/32768.0; 			#Why? Shouldn't the scaling factor be 2^32?
	
	
	#Energy computation
	
	Energy = Wavdata*Wavdata;
	EnergyFrameAvg = numpy.empty(TotalSamples,'float64');
	
	i = 0;
	while i < TotalSamples:
		Fsum = numpy.sum(Energy[i:min(i+SamplesPerFrame,TotalSamples):1]);
	        Fenergy = Fsum/SamplesPerFrame;
		EnergyFrameAvg[i:min(i+SamplesPerFrame,TotalSamples):1] = Fenergy*1000;	#scaled by 1000 to simplify thresholding
	        i = i+SamplesPerFrame;
	
	#plt.plot(EnergyFrameAvg);
	#plt.show();

	#Thresholding the energy vector 
	#Silence regions indicated by 1 and speech regions by 0
	
	SilBinaryMat = numpy.ones(TotalSamples,'uint16');
	SpeechSamples = EnergyFrameAvg >= 0.085
	SilBinaryMat[SpeechSamples] = 0
	SilBinMat = SilBinaryMat.tolist();
#	plt.plot(SilBinaryMat);
#	plt.fill_between(numpy.arange(0,TotalSamples),SilBinaryMat);
#	plt.show();
	
	#Thresholding the silence binary vector on duration of silence region

	i=1;
	SilSampleCount = (SilenceThreshold/WindowSize)*SamplesPerFrame;
	while i<TotalSamples:
		if SilBinMat[i] == 1:			
			SilBeginIndex = i;
			count = SilSampleCount;
			while i<TotalSamples and SilBinMat[i] == 1:
				count = count-1;
				i = i+1;
			if count > 0:
				for j in range(SilBeginIndex,i):
					SilBinMat[j] = 0;
		i = i+1;

##	plt.plot(SilBinaryMat);
##	plt.fill_between(numpy.arange(0,TotalSamples),SilBinaryMat);
##	plt.show();

	#Computing break points
	#Break points for audio are the middle points of silence regions

	BreakPoints = [];
	i=0;
	j=0;
	while i<TotalSamples:
		if SilBinMat[i] == 1:			
			j=i;
			while j<TotalSamples and SilBinMat[j+1] == 1:
				i = i+1;
				j = j+2;
			BreakPoints.append(i/float(SamplingRate));	
			i=j;
		i = i+1;
	print "Break points obtained successfully ..."
	print "Writing to file ../etc/" + sys.argv[2] + "/trim_pts.txt ..."
	f = open('../etc/'+sys.argv[2]+'/'+'trim_pts.txt','w');
	for pt in BreakPoints:
		f.write(str(pt) + "\n");
	f.close();

except IOError:
	print "Error opening file"
	sys.exit(1)
except wave.Error:
	print "Not a WAV file"
	sys.exit(1)
except ValueError:
	print "Not a WAV file"
	sys.exit(1)
