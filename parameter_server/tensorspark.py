import parameterwebsocketclient
import pyspark
from operator import add

def train_partition(partition):
	return parameterwebsocketclient.TensorSparkWorker().train_partition(partition)

def test_partition(partition):
	return parameterwebsocketclient.TensorSparkWorker().test_partition(partition)

# you can find the mnist csv files here http://pjreddie.com/projects/mnist-in-csv/
def train_epochs(num_epochs, batch_size):
	training_rdd = sc.textFile('/Users/christophersmith/code/adatao/tensorspark/data/medium_mnist_train.csv')
	for i in range(num_epochs):
		mapped_training = training_rdd.mapPartitions(train_partition)
		mapped_training.collect()
		training_rdd.repartition(training_rdd.count()/batch_size)

def test_all():
	testing_rdd = sc.textFile('./mnist_test.csv')
	mapped_testing = testing_rdd.mapPartitions(test_partition)
	return mapped_testing.reduce(add)/testing_rdd.count()

sc = pyspark.SparkContext()

num_epochs = 3
batch_size = 100
train_epochs(num_epochs, batch_size)

print test_all()