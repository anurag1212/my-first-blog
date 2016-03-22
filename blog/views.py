from django.shortcuts import render,redirect
from django import forms

from .forms import TextForm 


import sklearn.datasets
import sklearn.metrics
import sklearn.cross_validation
import sys
import os
import glob
import scipy.sparse as sp
import sklearn.feature_extraction.text
import sklearn.svm
from sklearn.feature_extraction.text import TfidfVectorizer


# Create your views here.
from django.http import HttpResponse

def form(request):
	if request.method=="POST":
		form=TextForm(request.POST)
		if form.is_valid():
			text=form.cleaned_data['text']
			form.save(commit=True)
			return index(request)
	else :
		form=TextForm()
	print request.POST.get('text')
	return render(request,'form.html',{'form':form})


def return_data(request):
	print "InNow"
	clf = sklearn.svm.LinearSVC()

	training_files = sklearn.datasets.load_files("/home/husen/Desktop/SVM/dataset_training")
	f=open("/home/husen/Desktop/SVM/dataset_prediction/test/test.txt",'w+')
	text=request.POST.get('text')
	f.write(text)
	f.close()
	print "Text ",text
	
	#print training_files.data

	predict_files = sklearn.datasets.load_files("/home/husen/Desktop/SVM/dataset_prediction")

	print "Predict",predict_files.data

	vectorizer = TfidfVectorizer(encoding='utf-8')
	X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
	print("n_samples: %d, n_features: %d" % X_t.shape)
	assert sp.issparse(X_t)



	X_p = vectorizer.transform((open(f).read() for f in predict_files.filenames))

	print X_p
	clf.fit(X_t, training_files.target)
	y_predicted=""
	y_predicted = clf.predict(X_p)
	print "OUT",y_predicted
	if y_predicted[0]==0:
		
		return render(request,'output.html',{'pred':"Dont be a bully bitch"})
	else:
		return render(request,'output.html',{'pred':"Dont be a noob"})
