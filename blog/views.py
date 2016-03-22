from django.shortcuts import render
from django.utils import timezone
from .models import Post
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

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def return_data(request):
	print ("InNow")
	clf = sklearn.svm.LinearSVC()

	training_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_training")
	f=open("/home/ubuntu/Desktop/SVM/dataset_prediction/test/test.txt",'w+')
	text=request.POST.get('input')
	f.write(text)
	f.close()
	print ("Text ",text)
	
	#print training_files.data

	predict_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_prediction")

	print ("Predict",predict_files.data)

	vectorizer = TfidfVectorizer(encoding='utf-8')
	X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
	print("n_samples: %d, n_features: %d" % X_t.shape)
	assert sp.issparse(X_t)



	X_p = vectorizer.transform((open(f).read() for f in predict_files.filenames))

	print (X_p)
	clf.fit(X_t, training_files.target)
	y_predicted=""
	y_predicted = clf.predict(X_p)
	print ("OUT",y_predicted)
	if y_predicted[0]==0:
		
		return render(request,'output.html',{'pred':"Dont be a bully bitch"})
	else:
		return render(request,'output.html',{'pred':"Dont be a noob"})
