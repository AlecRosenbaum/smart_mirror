import math
import re
import os

import numpy as np
from PIL import Image


def main():
	"""main"""
	DATA_FILE = "data/ujipenchars2.txt"

	data = []
	labels = []

	file_data = open(DATA_FILE, 'r').read()
	file_data = file_data.split("WORD ")

	label = re.compile("[0-9A-Z-]")
	points = re.compile(".*POINTS.*")
	for i in file_data:
		if label.match(i[0]):
			strokes = []

			lines = i.split("\n")
			labels.append(i[0])

			for j in lines[1:]:
				if points.match(j):
					strokes.append([int(k) for k in j.split("#")[1].strip().split(" ")])
			data.append(strokes)

	for idx, i in enumerate(data):
		directory = os.path.join("data", labels[idx])
		if not os.path.exists(directory):
			os.makedirs(directory)
		proc_data(i, os.path.join(directory, str(idx) + ".png"))


def proc_data(pen_strokes, output_path):
	"""process pen strokes data into a 32x32 image

	The pen stroke data is expected in the following format:
	[
		[x1, y1, x2, y2, ...],  # penstroke 1
		[x1, y1, x2, y2, ...],  # penstroke 2
	]

	Args:
		pen_strokes: 2D array (see format above)
		output_path: where to output the image
	"""
	ink_data = []

	all_data = []
	for i in pen_strokes:
		all_data += i

	all_data = np.reshape(all_data, (-1, 2))

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
		data = np.reshape(data, (-1, 2))
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
	img_data = np.empty(shape=(32, 32), dtype=np.uint8)
	# init as all white
	for x in range(img_data.shape[0]):
		for y in range(img_data.shape[1]):
			img_data[x][y] = 255

	# apply inking
	for coord in ink_data:
		img_data[coord[1]][coord[0]] = 0

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
					img_data[coord[1] + i[1]][coord[0] + i[0]] = 0
			except:
				pass

	# save image
	img = Image.fromarray(img_data)
	img.save(output_path)

if __name__ == '__main__':
	main()
