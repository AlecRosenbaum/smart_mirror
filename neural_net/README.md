
## Contents

* `nn.py`: A training script for a neural net to be used with the hasy data.
* `input_data.py`: a utility for reading the input HASYv2 data

## Why are we building a neural net?

I have made next to no progress towards getting other tools to work. So, instead I will work to create a basic neural net for handwriting recognition. Handwriting data is quite similar to the example dataset MNIST (for which better than 99% accuracy has been achieved), so this should hopefully yield acceptable results.


## What happens when it's trained?

Tensorflow has methods for serving trained models. The idea would then be to set up a local server for the trained model on the mirror, then the javascript web-frontend would send a 32x32 image (based on a canvas) of each letter written, it would be parsed into a real letter, then sent back to the javascript frontend.


## Environment/Dependencies

This was writting in Python 3.5 within an Anaconda distribution updated with the latest version of tensorflow.

## Notes on the data set

The data set currently being used was recently published with a paper (linked in sources). It includes many characters we don't need, so in the training script it filters the data to only use [characters appectable in gmail usernames](https://support.google.com/a/answer/33386?hl=en)

I haven't uploaded the data set, as it's pretty big and available online. The files used in the data set are:

* `hasy-data`: 168236 png images, each 32px x 32px
* `hasy-data-labels.csv`: Labels for all images.

I am currently still considering methods for expanding this data set and/or converting other data sets to the same format so they can be used in training.


## Sources

* HASY data source: <https://arxiv.org/pdf/1701.08380.pdf>
* The neural net is modified code from <https://www.tensorflow.org/get_started/mnist/pros>