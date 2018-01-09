import numpy as np
import sys

if len(sys.argv) != 2:
    print ('Usage: %s data00x' % __file__)
    sys.exit(0)

label_file = 'label_data/raw_data/' + sys.argv[1] + '.npz'

# forward, right, backward, left
label_data = np.load(label_file)['train_labels'][1:]


# forward_left, forward, forward_right
new_label_array = np.zeros((1, 3), np.float32)

for label_array in label_data:
    temp_label_array = np.zeros((1, 3), np.float32)

    # forward left
    if label_array[0] == 1 and label_array[3] == 1:
        temp_label_array[0][0] = 1
    # forward right
    elif label_array[0] == 1 and label_array[1] == 1:
        temp_label_array[0][2] = 1
    # forward
    else:
        temp_label_array[0][1] = label_array[0]

    new_label_array = np.vstack((new_label_array, temp_label_array))

np.savez('label_data/' + sys.argv[1] + '.npz', label_data=new_label_array[1:])
