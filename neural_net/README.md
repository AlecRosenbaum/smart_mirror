
## Contents

* `hasy-data`: 168236 png images, each 32px x 32px
* `hasy-data-labels.csv`: Labels for all images.
* `symbols.csv`: Counts for all symbols included in dataset (includes many non alphanumeric values)
* `nn.py`: A training script for a neural net to be used with the hasy data.


## Why are we building a neural net?

I have made next to no progress towards getting other tools to work. So, instead I will work to create a basic neural net for handwriting recognition. Handwriting data is quite similar to the example dataset MNIST (for which 99% accuracy has been achieved), so this should hopefully yield acceptable results. 

Then, we can set up a local server that just accepts inking data from a javascript/html canvas in the browser, and returns what letter it is.


## Environment/Dependencies

This was writting in Python 3.5 within an Anaconda distribution updated with the latest version of tensorflow.

## Notes on the data set

The data set currently being used was recently published with a paper (linked in sources). It includes many characters we don't need, so in the training script it filters the data to only use [characters appectable in gmail usernames](https://support.google.com/a/answer/33386?hl=en)

I've only uploaded the compressed data set.

## Sources

* HASY data source: <https://arxiv.org/pdf/1701.08380.pdf>
* The neural net is modified code from <https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/layers/cnn_mnist.py>