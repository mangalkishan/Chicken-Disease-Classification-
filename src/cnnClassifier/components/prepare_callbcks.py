import os
import tensorflow as tf
from time import time
from cnnClassifier.entity.config_entity import PrepareCallBacksConfig


class PrepareCallBacks:
    def __init__(self, config: PrepareCallBacksConfig):
        self.config = config

    @property
    def _create_tb_callbacks(self):
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_logs_dir = os.path.join(self.config.tenserboard_root_log_dir, f"tb_logs_at{timestamp}")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=tb_logs_dir)
        return tensorboard_callback
    
    @property
    def _create_checkpoint_callbacks(self):
        checkpoint_filepath = self.config.checkpoint_model_filepath
        model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath, save_best_only=True)
        return model_checkpoint_callback
    
    def get_tb_ckpt_callbacks(self):
        return [self._create_tb_callbacks, self._create_checkpoint_callbacks]