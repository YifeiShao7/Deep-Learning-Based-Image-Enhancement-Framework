import tensorflow as tf
import cv2
import numpy as np

INPUT_SIZE = 512
ATTENTION_SIZE = 32
MULTIPLE = 6

# reconstruct residual from patches
def reconstruct_residual_from_patches(residual, multiple):
    residual = np.reshape(residual, [ATTENTION_SIZE, ATTENTION_SIZE, multiple, multiple, 3])
    residual = np.transpose(residual, [0,2,1,3,4])
    return np.reshape(residual, [ATTENTION_SIZE * multiple, ATTENTION_SIZE * multiple, 3])

# extract image patches
def extract_image_patches(img, multiple):
    h, w, c = img.shape
    img = np.reshape(img, [h//multiple, multiple, w//multiple, multiple, c])
    img = np.transpose(img, [0,2,1,3,4])
    return img

# residual aggregation module
def residual_aggregate(residual, attention, multiple):
    residual = extract_image_patches(residual, multiple * INPUT_SIZE//ATTENTION_SIZE)
    residual = np.reshape(residual, [1, residual.shape[0] * residual.shape[1], -1])
    residual = np.matmul(attention, residual)
    residual = reconstruct_residual_from_patches(residual, multiple * INPUT_SIZE//ATTENTION_SIZE)
    return residual

def resize_ave(img, multiple):
    img = img.astype(np.float32)
    img_patches = extract_image_patches(img, multiple)
    img = np.mean(img_patches, axis=(2,3))
    return img

# pre-processing module
def pre_process(raw_img, raw_mask, multiple):

    raw_mask = raw_mask.astype(np.float32) / 255.
    raw_img = raw_img.astype(np.float32)

    # resize raw image & mask to desinated size
    large_img = cv2.resize(raw_img,  (multiple * INPUT_SIZE, multiple * INPUT_SIZE), interpolation = cv2. INTER_LINEAR)
    large_mask = cv2.resize(raw_mask, (multiple * INPUT_SIZE, multiple * INPUT_SIZE), interpolation = cv2.INTER_NEAREST)

    # down-sample large image & mask to 512x512
    small_img = resize_ave(large_img, multiple)
    small_mask = cv2.resize(raw_mask, (INPUT_SIZE, INPUT_SIZE), interpolation = cv2.INTER_NEAREST)

    # set hole region to 1. and background to 0.
    small_mask = 1. - small_mask
    return large_img, large_mask, small_img, small_mask

# post-processing module
def post_process(raw_img, large_img, large_mask, res_512, img_512, mask_512, attention, multiple):

    # compute the raw residual map
    h, w, c = raw_img.shape
    low_base = cv2.resize(res_512.astype(np.float32), (INPUT_SIZE * multiple, INPUT_SIZE * multiple), interpolation = cv2.INTER_LINEAR)
    low_large = cv2.resize(img_512.astype(np.float32), (INPUT_SIZE * multiple, INPUT_SIZE * multiple), interpolation = cv2.INTER_LINEAR)
    residual = (large_img - low_large) * large_mask

    # reconstruct residual map using residual aggregation module
    residual = residual_aggregate(residual, attention, multiple)

    # compute large inpainted result
    res_large = low_base + residual
    res_large = np.clip(res_large, 0., 255.)

    # resize large inpainted result to raw size
    res_raw = cv2.resize(res_large, (w, h), interpolation = cv2.INTER_LINEAR)

    # paste the hole region to the original raw image
    mask = cv2.resize(mask_512.astype(np.float32), (w, h), interpolation = cv2.INTER_LINEAR)
    mask = np.expand_dims(mask, axis=2)
    res_raw = res_raw * mask + raw_img * (1. - mask)

    return res_raw.astype(np.uint8)


def inpaint(raw_img,
            raw_mask,
            sess,
            inpainted_512_node,
            attention_node,
            mask_512_node,
            img_512_ph,
            mask_512_ph,
            multiple):
    # pre-processing
    img_large, mask_large, img_512, mask_512 = pre_process(raw_img, raw_mask, multiple)

    # neural network
    inpainted_512, attention, mask_512 = sess.run([inpainted_512_node, attention_node, mask_512_node],
                                                  feed_dict={img_512_ph: [img_512], mask_512_ph: [mask_512[:, :, 0:1]]})

    # post-processing
    res_raw_size = post_process(raw_img, img_large, mask_large, \
                                inpainted_512[0], img_512, mask_512[0], attention[0], multiple)

    return res_raw_size

"""
process with the inpaint model
:param src_img: original image
:param mask_img: mask the inpaint area
:return inpainted image
"""
def inpaint_process(src_img, mask_img):
    with tf.Graph().as_default():
        with open('./HiFillModel/hifill.pb', "rb") as f:
            output_graph_def = tf.compat.v1.GraphDef()
            output_graph_def.ParseFromString(f.read())
            tf.import_graph_def(output_graph_def, name="")

        with tf.compat.v1.Session() as sess:
            init = tf.compat.v1.global_variables_initializer()
            sess.run(init)
            image_ph = sess.graph.get_tensor_by_name('img:0')
            mask_ph = sess.graph.get_tensor_by_name('mask:0')
            inpainted_512_node = sess.graph.get_tensor_by_name('inpainted:0')
            attention_node = sess.graph.get_tensor_by_name('attention:0')
            mask_512_node = sess.graph.get_tensor_by_name('mask_processed:0')

            inpainted = inpaint(src_img, mask_img, sess, inpainted_512_node, attention_node, mask_512_node, image_ph, mask_ph, MULTIPLE)
            return inpainted
