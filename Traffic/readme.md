#  Experimentation Process
**Starting the Process**
<ul> 
 <li> First, I started with an almost identical configuration (i.e. same number of convolutional and pooling layers, same number of sizes of filters for 
 convolutional layers, etc.) as in handwriting.py from the lecture with one modification. The modification was that I used the sigmoid function as an 
activation function in the hidden layer. It turned out that it doesn't work well, with a result accuracy= 0.0587.
</ul>

**Experimenting with convolutional and pooling layers**
</ul>
<li> Next I experimented with adding one more convolutional and one more pooling layer with same filter size. That means I added 
 tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)), tf.keras.layers.MaxPooling2D(pool_size=(2, 2)).
<li>  Adding both, the convolutional and the pooling layer, doesn't show any positive effect, and the result was an accuracy of 0.0544. So I changed filter size.
</ul>

**Experimenting with different filter sizes**

</ul>
 
<li> First, I tried to reduce the filter size of both convolutional layers to 

tf.keras.layers.Conv2D(16, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)).

<li> That had a huge impact and the result was an accuracy of 0.9735. If I reduced only the filter size of the first convolutional layer from (32, (3, 3)  to (16, (3, 3) the effect was still huge, with an accuracy of 0.9423. That means the accuracy was a slightly worse.

<li> Contrary to the positive effect that occurred when reducing the filter sizes of the two convolutional layers from (32, (3, 3) to (16, (3, 3)), there isn't any positive effect by increasing the filters size of both convolutional layers to (64, (3, 3)). Here the result was an accuracy of 0.0514. Setting only the second convolutional layer to (64, (3, 3)) had no positive effect with an accuracy of 0.0538. 

<li> Furthermore, I observed that an increasing of the pooling filters size from pool_size=(2, 2) to pool_size=(3, 3) had a medium-sized negative effect on the performance of the neuronal network. The outcome was accuracy= 0.8012. A decreasing of the pooling layer filters was not reasonable because the original filter size was pool_size=(2, 2).
</ul>
 
**Experimenting with dropout sizes**

</ul>
<li> If I changed the dropout from 0.5 to 0.3 for the best configuration, I received an accuracy of 0.9734 compared to 0.9735 for a dropout of 0.5. If I enlarged thedropout from 0.5 to 0.7, I observed a huge negative effect, so that the accuracy was only 0.0566. Last I added a new hidden layer with the following properties

<li> tf.keras.layers.Dense(128, activation="sigmoid")
<li> tf.keras.layers.Dropout(0.5)

<li> As a result I recieved an accuracy of 0.8810 compared to 0.9735, which I got for the best configuration.
</ul>
