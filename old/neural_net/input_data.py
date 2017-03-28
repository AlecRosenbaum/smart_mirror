"""Functions for downloading and reading data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip
import math
import re
import os
import csv

from PIL import Image
import numpy
from six.moves import xrange  # pylint: disable=redefined-builtin

from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.framework import dtypes

CSV_FILE = "hasy-data-labels.csv"
UJIPEN_DATA = "ujipenchars2.txt"
NIST_DIR = "nist"


def _read32(bytestream):
  dt = numpy.dtype(numpy.uint32).newbyteorder('>')
  return numpy.frombuffer(bytestream.read(4), dtype=dt)[0]


def conv_img(path):
  """reads an image, converts it to a 3D array [x, y, val]

  Args:
      path: path to an image

  Returns:
      1D array of alpha values from the image
  """
  img = Image.open(path).convert('L')
  arr = numpy.array(img)
  
  return arr.reshape(32, 32, 1)


def conv_label(char):
  labels = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9,
    'K': 10,
    'L': 11,
    'M': 12,
    'N': 13,
    'O': 14,
    'P': 15,
    'Q': 16,
    'R': 17,
    'S': 18,
    'T': 19,
    'U': 20,
    'V': 21,
    'W': 22,
    'X': 23,
    'Y': 24,
    'Z': 25,
    '0': 26,
    '1': 27,
    '2': 28,
    '3': 29,
    '4': 30,
    '5': 31,
    '6': 32,
    '7': 33,
    '8': 34,
    '9': 35,
    # 'a': 36,
    # 'b': 37,
    # 'c': 38,
    # 'd': 39,
    # 'e': 40,
    # 'f': 41,
    # 'g': 42,
    # 'h': 43,
    # 'i': 44,
    # 'j': 45,
    # 'k': 46,
    # 'l': 47,
    # 'm': 48,
    # 'n': 49,
    # 'o': 50,
    # 'p': 51,
    # 'q': 52,
    # 'r': 53,
    # 's': 54,
    # 'u': 55,
    # 'v': 56,
    # 'w': 57,
    # 'x': 58,
    # 'y': 59,
    # 'z': 60,
    '-': 36,
  }
  return labels[char]


def get_hasy_data(csv_path):
  """returns data + labels from the HASYv2 data set"""
  csv_data = load_csv(csv_path)
  data = data_to_list(csv_data)

  n = len(data)

  ret_data = numpy.empty(shape=(n, 32, 32, 1), dtype=numpy.uint8)
  ret_labels = numpy.empty(shape=(n), dtype=numpy.uint8)

  for idx, i in enumerate(data):
    ret_labels[idx] = conv_label(i[0])
    ret_data[idx] = conv_img(i[1])

  return ret_data, ret_labels


def get_ujipen_data(path):
  """returns data + labels from the ujipen data set"""
  data = []
  labels = []
  images = []

  file_data = open(path, 'r').read()
  file_data = file_data.split("WORD ")

  label = re.compile("[0-9A-Z-]")
  points = re.compile(".*POINTS.*")
  for i in file_data:
    if label.match(i[0]):
      strokes = []

      lines = i.split("\n")
      labels.append(conv_label(i[0]))

      for j in lines[1:]:
        if points.match(j):
          strokes.append([int(k) for k in j.split("#")[1].strip().split(" ")])
      data.append(strokes)

  for idx, i in enumerate(data):
    images.append(proc_uji_data(i))
  return images, numpy.asarray(labels, dtype=numpy.uint8)


def proc_uji_data(pen_strokes, output_path=None):
  """process pen strokes data into a 32x32 image

  The pen stroke data is expected in the following format:
  [
    [x1, y1, x2, y2, ...],  # penstroke 1
    [x1, y1, x2, y2, ...],  # penstroke 2
  ]

  Args:
    pen_strokes: 2D array (see format above)
    output_path: where to output the image

  Returns:
    a 32x32 numpy array containing the image data
  """
  ink_data = []

  all_data = []
  for i in pen_strokes:
    all_data += i

  all_data = numpy.reshape(all_data, (-1, 2))

  # pre-process data (crop, scale, center)
  x_max = max([i[0] for i in all_data])
  x_min = min([i[0] for i in all_data])

  y_max = max([i[1] for i in all_data])
  y_min = min([i[1] for i in all_data])

  scale_x = 29 / (x_max - x_min)
  scale_y = 29 / (y_max - y_min)
  if scale_x < scale_y:
    scale = scale_x
    offset_x = 0
    offset_y = 15 - (y_max - y_min) * scale_x/2
  else:
    scale = scale_y
    offset_x = 15 - (x_max - x_min) * scale_y/2
    offset_y = 0

  for data in pen_strokes:
    data = numpy.reshape(data, (-1, 2))
    data = [[int(math.floor((i[0] - x_min)*scale) + 1 + offset_x), int(math.floor((i[1] - y_min)*scale) + 1 + offset_y)] for i in data]

    # interpolate to create continuous lines
    i = 0
    while i < len(data) - 1:
      x_diff = data[i+1][0] - data[i][0]
      y_diff = data[i+1][1] - data[i][1]
      if math.hypot(x_diff, y_diff) > 3:
        # determine new point location
        x_offest = math.floor(x_diff/2)
        y_offest = math.floor(y_diff/2)
        data.insert(i+1, [data[i][0] + x_offest, data[i][1] + y_offest])
      i += 1
    ink_data += data

  # create image
  img_data = numpy.empty(shape=(32, 32, 1), dtype=numpy.uint8)
  # init as all white
  for x in range(img_data.shape[0]):
    for y in range(img_data.shape[1]):
      img_data[x][y][0] = 255

  # apply inking
  for coord in ink_data:
    img_data[coord[1]][coord[0]][0] = 0

    # make lines slightly thicker
    offsets = [
      [0, 1],
      [1, 1],
      [1, 0],
      [1, -1],
      [0, -1],
      [-1, -1],
      [-1, 0],
      [-1, 1],
    ]
    for i in offsets:
      try:
        if not coord[1] % 31 == 0 and not coord[0] % 31 == 0:
          img_data[coord[1] + i[1]][coord[0] + i[0]][0] = 0
      except:
        pass

  # save image
  if output_path is not None:
    img = Image.fromarray(img_data)
    img.save(output_path)

  return img_data


def get_nist_data(csv_path):
  """returns data + labels from the nist data set"""

  raise ValueError("this method isn't implemented yet.")
  # csv_data = load_csv(csv_path)
  # data = data_to_list(csv_data)

  # n = len(data)

  # ret_data = numpy.empty(shape=(n, 32, 32, 1), dtype=numpy.uint8)
  # ret_labels = numpy.empty(shape=(n), dtype=numpy.uint8)

  # for idx, i in enumerate(data):
  #   ret_labels[idx] = conv_label(i[0])
  #   ret_data[idx] = conv_img(i[1])
  pass
  # return ret_data, ret_labels


def load_csv(filepath, delimiter=',', quotechar="'"):
  """
  Load a CSV file.

  Parameters
  ----------
  filepath : str
      Path to a CSV file
  delimiter : str, optional
  quotechar : str, optional

  Returns
  -------
  list of dicts : Each line of the CSV file is one element of the list.
  """
  data = []
  csv_dir = os.path.dirname(filepath)
  with open(filepath, 'r') as csvfile:
    reader = csv.DictReader(
      csvfile,
      delimiter=delimiter,
      quotechar=quotechar)
    for row in reader:
      if 'path' in row:
        row['path'] = os.path.abspath(
          os.path.join(
            csv_dir,
            row['path']))
      data.append(row)
  return data


def data_to_list(data):
  """
  Organize `data` into a list.

  Parameters
  ----------
  data : list of dicts
      Each dict contains the key `latex` which is the class label, and `path`

  Returns
  -------
  ret : 2d list
    [
      [latex, path],
      ...
    ]
  """
  ret = []
  prog = re.compile("[A-Z0-9-]")
  for i in data:
    if not prog.match(i['latex']):
      continue
    ret.append([i['latex'], i['path']])
  return ret


def extract_images(f):
  """Extract the images into a 4D uint8 numpy array [index, y, x, depth].

  Args:
    f: A file object that can be passed into a gzip reader.

  Returns:
    data: A 4D uint8 numpy array [index, y, x, depth].

  Raises:
    ValueError: If the bytestream does not start with 2051.

  """
  print('Extracting', f.name)
  with gzip.GzipFile(fileobj=f) as bytestream:
    magic = _read32(bytestream)
    if magic != 2051:
      raise ValueError('Invalid magic number %d in MNIST image file: %s' %
                       (magic, f.name))
    num_images = _read32(bytestream)
    rows = _read32(bytestream)
    cols = _read32(bytestream)
    buf = bytestream.read(rows * cols * num_images)
    data = numpy.frombuffer(buf, dtype=numpy.uint8)
    data = data.reshape(num_images, rows, cols, 1)
    return data


def dense_to_one_hot(labels_dense, num_classes):
  """Convert class labels from scalars to one-hot vectors."""
  num_labels = labels_dense.shape[0]
  index_offset = numpy.arange(num_labels) * num_classes
  labels_one_hot = numpy.zeros((num_labels, num_classes))
  labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
  return labels_one_hot


def extract_labels(f, one_hot=False, num_classes=10):
  """Extract the labels into a 1D uint8 numpy array [index].

  Args:
    f: A file object that can be passed into a gzip reader.
    one_hot: Does one hot encoding for the result.
    num_classes: Number of classes for the one hot encoding.

  Returns:
    labels: a 1D uint8 numpy array.

  Raises:
    ValueError: If the bystream doesn't start with 2049.
  """
  print('Extracting', f.name)
  with gzip.GzipFile(fileobj=f) as bytestream:
    magic = _read32(bytestream)
    if magic != 2049:
      raise ValueError('Invalid magic number %d in MNIST label file: %s' %
                       (magic, f.name))
    num_items = _read32(bytestream)
    buf = bytestream.read(num_items)
    labels = numpy.frombuffer(buf, dtype=numpy.uint8)
    if one_hot:
      return dense_to_one_hot(labels, num_classes)
    return labels


class DataSet(object):

  def __init__(self,
               images,
               labels,
               fake_data=False,
               one_hot=False,
               dtype=dtypes.float32,
               reshape=True):
    """Construct a DataSet.
    one_hot arg is used only if fake_data is true.  `dtype` can be either
    `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
    `[0, 1]`.
    """
    dtype = dtypes.as_dtype(dtype).base_dtype
    if dtype not in (dtypes.uint8, dtypes.float32):
      raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
                      dtype)
    if fake_data:
      self._num_examples = 10000
      self.one_hot = one_hot
    else:
      assert images.shape[0] == labels.shape[0], (
          'images.shape: %s labels.shape: %s' % (images.shape, labels.shape))
      self._num_examples = images.shape[0]

      # Convert shape from [num examples, rows, columns, depth]
      # to [num examples, rows*columns] (assuming depth == 1)
      if reshape:
        assert images.shape[3] == 1
        images = images.reshape(images.shape[0],
                                images.shape[1] * images.shape[2])
      if dtype == dtypes.float32:
        # Convert from [0, 255] -> [0.0, 1.0].
        images = images.astype(numpy.float32)
        images = numpy.multiply(images, 1.0 / 255.0)
    self._images = images
    self._labels = labels
    self._epochs_completed = 0
    self._index_in_epoch = 0

  @property
  def images(self):
    return self._images

  @property
  def labels(self):
    return self._labels

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_completed(self):
    return self._epochs_completed

  def next_batch(self, batch_size, fake_data=False, shuffle=True):
    """Return the next `batch_size` examples from this data set."""
    if fake_data:
      fake_image = [1] * 784
      if self.one_hot:
        fake_label = [1] + [0] * 9
      else:
        fake_label = 0
      return [fake_image for _ in xrange(batch_size)], [
          fake_label for _ in xrange(batch_size)
      ]
    start = self._index_in_epoch
    # Shuffle for the first epoch
    if self._epochs_completed == 0 and start == 0 and shuffle:
      perm0 = numpy.arange(self._num_examples)
      numpy.random.shuffle(perm0)
      self._images = self.images[perm0]
      self._labels = self.labels[perm0]
    # Go to the next epoch
    if start + batch_size > self._num_examples:
      # Finished epoch
      self._epochs_completed += 1
      # Get the rest examples in this epoch
      rest_num_examples = self._num_examples - start
      images_rest_part = self._images[start:self._num_examples]
      labels_rest_part = self._labels[start:self._num_examples]
      # Shuffle the data
      if shuffle:
        perm = numpy.arange(self._num_examples)
        numpy.random.shuffle(perm)
        self._images = self.images[perm]
        self._labels = self.labels[perm]
      # Start next epoch
      start = 0
      self._index_in_epoch = batch_size - rest_num_examples
      end = self._index_in_epoch
      images_new_part = self._images[start:end]
      labels_new_part = self._labels[start:end]
      return numpy.concatenate((images_rest_part, images_new_part), axis=0) , numpy.concatenate((labels_rest_part, labels_new_part), axis=0)
    else:
      self._index_in_epoch += batch_size
      end = self._index_in_epoch
      return self._images[start:end], self._labels[start:end]


def read_data_sets(train_dir,
                   fake_data=False,
                   one_hot=False,
                   dtype=dtypes.float32,
                   reshape=True,
                   validation_size=5000):
  if fake_data:

    def fake():
      return DataSet([], [], fake_data=True, one_hot=one_hot, dtype=dtype)

    train = fake()
    validation = fake()
    test = fake()
    return base.Datasets(train=train, validation=validation, test=test)

  hasy_images, hasy_labels = get_hasy_data(CSV_FILE)
  uji_images, uji_labels = get_ujipen_data(UJIPEN_DATA)
  images = numpy.concatenate(hasy_images, uji_images)
  labels = numpy.concatenate(hasy_labels, uji_labels)
  labels = dense_to_one_hot(labels, 37)

  print("data size", len(labels))

  # divide between training and eval
  pct_train = .8
  idx_test = math.ceil(((1-pct_train)/2)*len(labels))
  idx_validate = math.ceil((1-pct_train)*len(labels))

  test_images = images[:idx_test]
  test_labels = labels[:idx_test]
  validation_images = images[idx_test+1:idx_validate]
  validation_labels = labels[idx_test+1:idx_validate]
  train_images = images[idx_validate+1:]
  train_labels = labels[idx_validate+1:]

  train = DataSet(train_images, train_labels, dtype=dtype, reshape=reshape)
  validation = DataSet(validation_images,
                       validation_labels,
                       dtype=dtype,
                       reshape=reshape)
  test = DataSet(test_images, test_labels, dtype=dtype, reshape=reshape)

  return base.Datasets(train=train, validation=validation, test=test)


def load_mnist(train_dir='MNIST-data'):
  return read_data_sets(train_dir)