
## Contents

* `nn.py`: A training script for a neural net to be used with the hasy data.
* `input_data.py`: a utility for reading input data
* `data_transform.py`: a utility used for expanding the data set to include digitally handwritten characters stored in "ujipen" format

## Why are we building a neural net?

I have made next to no progress towards getting other tools to work. So, instead I will work to create a basic neural net for handwriting recognition. Handwriting data is quite similar to the example dataset MNIST (for which better than 99% accuracy has been achieved), so this should hopefully yield acceptable results.


## What happens when it's trained?

Tensorflow has methods for serving trained models. The idea would then be to set up a local server for the trained model on the mirror, then the javascript web-frontend would send a 32x32 image (based on a canvas) of each letter written, it would be parsed into a real letter, then sent back to the javascript frontend.


## Environment/Dependencies

This was writting in Python 3.5 within an Anaconda distribution updated with the latest version of tensorflow.

## Notes on the data set

The data set currently being used was recently published with a paper (linked in sources). It includes many characters we don't need, so in the training script it filters the data to only use [characters appectable in gmail usernames](https://support.google.com/a/answer/33386?hl=en)

I haven't uploaded the data sets, as they're pretty big and available online. The datasets used are:

### HASYv2
* `hasy-data`: 168236 png images, each 32px x 32px
* `hasy-data-labels.csv`: Labels for all images.

### UJI pen characters

* `ujipenchars2.txt`: a file of UJI pen characters stored as x/y coordinates

I am currently still considering methods for expanding this data set and/or converting other data sets to the same format so they can be used in training.

### NIST handprinted forms and characters

All images are provided divided by character type in 128x128 format. They were converted to 32x32 using the command from the base directory (this took a little while):
`find . -wholename "*/train*/*.png" | xargs -l -i convert {} -resize 32x32 {}`
`find . -wholename "*/train*/*.png" | xargs -l -i convert {} -crop 64x64+32+32 -resize 32x32 cropped_centered_data/{}`


## Sources

* HASY data source: <https://arxiv.org/pdf/1701.08380.pdf>
* UJI pen data source: [homepage](https://archive.ics.uci.edu/ml/datasets/UJI+Pen+Characters+%28Version+2%29), [data](https://archive.ics.uci.edu/ml/machine-learning-databases/uji-penchars/version2/ujipenchars2.txt)
* NIST data source: [homepage](https://www.nist.gov/srd/nist-special-database-19), [data](https://s3.amazonaws.com/nist-srd/SD19/by_class.zip)
* The neural net is modified code from <https://www.tensorflow.org/get_started/mnist/pros>