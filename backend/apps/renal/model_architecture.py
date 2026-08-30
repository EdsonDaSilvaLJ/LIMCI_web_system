def build_renal_model(input_shape=(224, 224, 3)):
    """Reconstruct the U-Net/VGG-19 architecture compatible with the folds."""
    import tensorflow as tf

    inputs = tf.keras.Input(shape=input_shape, name="input_1")
    encoder = tf.keras.applications.VGG19(
        include_top=False,
        weights=None,
        input_tensor=inputs,
    )

    skip_connections = [
        encoder.get_layer("block4_conv4").output,
        encoder.get_layer("block3_conv4").output,
        encoder.get_layer("block2_conv2").output,
        encoder.get_layer("block1_conv2").output,
    ]
    x = encoder.get_layer("block5_conv4").output

    decoder_blocks = [
        (128, "conv2d_transpose", "concatenate", "dropout", "conv2d", "conv2d_1"),
        (64, "conv2d_transpose_1", "concatenate_1", "dropout_1", "conv2d_2", "conv2d_3"),
        (32, "conv2d_transpose_2", "concatenate_2", "dropout_2", "conv2d_4", "conv2d_5"),
        (16, "conv2d_transpose_3", "concatenate_3", "dropout_3", "conv2d_6", "conv2d_7"),
    ]

    for skip, block in zip(skip_connections, decoder_blocks):
        filters, transpose_name, concatenate_name, dropout_name, conv_1, conv_2 = block
        x = tf.keras.layers.Conv2DTranspose(
            filters,
            kernel_size=(2, 2),
            strides=(2, 2),
            padding="same",
            name=transpose_name,
        )(x)
        x = tf.keras.layers.Concatenate(name=concatenate_name)([x, skip])
        x = tf.keras.layers.Dropout(0.3, name=dropout_name)(x)
        x = tf.keras.layers.Conv2D(
            filters,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
            name=conv_1,
        )(x)
        x = tf.keras.layers.Conv2D(
            filters,
            kernel_size=(3, 3),
            activation="relu",
            padding="same",
            name=conv_2,
        )(x)

    outputs = tf.keras.layers.Conv2D(
        1,
        kernel_size=(1, 1),
        activation="sigmoid",
        name="conv2d_8",
    )(x)
    return tf.keras.Model(inputs=inputs, outputs=outputs, name="vgg19_unet")
