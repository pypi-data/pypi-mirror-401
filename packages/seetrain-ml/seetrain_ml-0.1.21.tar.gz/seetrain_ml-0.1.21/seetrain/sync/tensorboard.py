#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import os
from typing import Any, Dict, List

from ..data import data as seetrain_data
from ..data.modules import Image, Text


def _extract_args(args: tuple, kwargs: Dict[str, Any], param_names: List[str]) -> tuple:
    """
    从args和kwargs中提取参数值的通用函数

    Args:
        args: 位置参数元组
        kwargs: 关键字参数字典
        param_names: 参数名称列表

    Returns:
        tuple: 按param_names顺序返回提取的参数值
    """
    values = []
    for i, name in enumerate(param_names):
        if len(args) > i:
            values.append(args[i])
        else:
            values.append(kwargs.get(name, None))
    return tuple(values)


def _create_patched_methods(SummaryWriter, logdir_extractor, types=None):
    """
    创建patched方法的工厂函数

    Args:
        SummaryWriter: SummaryWriter类
        logdir_extractor: 提取logdir的函数
        types: 要同步的数据类型列表，如 ['scalar', 'scalars', 'image', 'text']。
               None 表示同步所有类型。

    Returns:
        tuple: (patched_init, patched_add_scalar, patched_add_image, patched_close)
    """
    types_set = set(types) if types is not None else None

    original_init = SummaryWriter.__init__
    original_add_scalar = SummaryWriter.add_scalar
    original_add_scalars = SummaryWriter.add_scalars
    original_add_image = SummaryWriter.add_image
    original_add_images = getattr(SummaryWriter, "add_images", None)
    original_add_figure = getattr(SummaryWriter, "add_figure", None)
    original_add_text = SummaryWriter.add_text
    original_close = SummaryWriter.close
    
    def _norm_step(s):
        if s is None:
            return None
        try:
            return int(s)
        except Exception:
            try:
                return int(s.item())
            except Exception:
                return None
    
    def _to_uint8_hwc(arr):
        try:
            import numpy as np
            if hasattr(arr, "dtype") and arr.dtype is not None and arr.dtype.kind == 'f':
                try:
                    mn = float(arr.min()) if arr.size else 0.0
                    mx = float(arr.max()) if arr.size else 0.0
                except Exception:
                    mn, mx = 0.0, 0.0
                if mx <= 1.0 and mn >= 0.0:
                    arr = (arr * 255.0).round()
                arr = np.clip(arr, 0, 255).astype(np.uint8)
            elif hasattr(arr, "dtype") and arr.dtype != None and arr.dtype != getattr(__import__("numpy"), "uint8"):
                import numpy as np
                arr = np.clip(arr, 0, 255).astype(np.uint8)
            return arr
        except Exception:
            return arr
    
    def patched_init(self, *args, **kwargs):
        tb_logdir = logdir_extractor(args, kwargs)
        if tb_logdir is not None:
            try:
                tb_logdir = os.fspath(tb_logdir)
            except TypeError:
                tb_logdir = str(tb_logdir)

        tb_config = {
            'tensorboard_logdir': tb_logdir,
        }

        if not seetrain_data._initialized:
            seetrain_data.init(config=tb_config, dir=tb_logdir)
        else:
            seetrain_data.update_config(tb_config)
            if tb_logdir:
                os.environ["LOG_FILE"] = os.path.join(os.path.abspath(tb_logdir), "seetrain.log")

        return original_init(self, *args, **kwargs)

    @functools.wraps(original_add_scalar)
    def patched_add_scalar(self, *args, **kwargs):
        if types_set is not None and 'scalar' not in types_set:
            return original_add_scalar(self, *args, **kwargs)
        tag, scalar_value, global_step = _extract_args(
            args, kwargs, ['tag', 'scalar_value', 'global_step']
        )

        data = {tag: scalar_value}
        step = _norm_step(global_step)
        seetrain_data.log(data=data, step=step, print_to_console=False)

        return original_add_scalar(self, *args, **kwargs)

    @functools.wraps(original_add_scalars)
    def patched_add_scalars(self, *args, **kwargs):
        if types_set is not None and 'scalars' not in types_set:
            return original_add_scalars(self, *args, **kwargs)
        tag, scalar_value_dict, global_step = _extract_args(
            args, kwargs, ['tag', 'scalar_value_dict', 'global_step']
        )
        data = {}
        for dict_tag, value in scalar_value_dict.items():
            data[f"{tag}/{dict_tag}"] = value
        step = _norm_step(global_step)
        seetrain_data.log(data=data, step=step, print_to_console=False)
        return original_add_scalars(self, *args, **kwargs)

    @functools.wraps(original_add_image)
    def patched_add_image(self, *args, **kwargs):
        if types_set is not None and 'image' not in types_set:
            return original_add_image(self, *args, **kwargs)
        import numpy as np

        tag, img_tensor, global_step, _, dataformats = _extract_args(
            args, kwargs, ['tag', 'img_tensor', 'global_step', 'walltime', 'dataformats']
        )
        dataformats = dataformats or 'CHW'

        if hasattr(img_tensor, 'cpu'):
            img_tensor = img_tensor.cpu()
        if hasattr(img_tensor, 'numpy'):
            img_tensor = img_tensor.numpy()

        if dataformats == 'CHW':
            img_tensor = np.transpose(img_tensor, (1, 2, 0))
        elif dataformats == 'NCHW':
            if img_tensor.ndim == 4:
                img_tensor = img_tensor[0]
            img_tensor = np.transpose(img_tensor, (1, 2, 0))
        elif dataformats == 'HW':
            img_tensor = np.expand_dims(img_tensor, axis=-1)
        elif dataformats == 'HWC':
            pass

        img_tensor = _to_uint8_hwc(img_tensor)
        data = {tag: Image(img_tensor)}
        step = _norm_step(global_step)
        seetrain_data.log(data=data, step=step, print_to_console=False)

        return original_add_image(self, *args, **kwargs)

    if original_add_images is not None:
        @functools.wraps(original_add_images)
        def patched_add_images(self, *args, **kwargs):
            if types_set is not None and 'image' not in types_set:
                return original_add_images(self, *args, **kwargs)
            import numpy as np
            tag, img_tensor, global_step, _, dataformats = _extract_args(
                args, kwargs, ['tag', 'img_tensor', 'global_step', 'walltime', 'dataformats']
            )
            dataformats = dataformats or 'NCHW'
            if hasattr(img_tensor, 'cpu'):
                img_tensor = img_tensor.cpu()
            if hasattr(img_tensor, 'numpy'):
                img_tensor = img_tensor.numpy()
            if dataformats == 'NCHW':
                if img_tensor.ndim == 4:
                    for idx in range(img_tensor.shape[0]):
                        single = np.transpose(img_tensor[idx], (1, 2, 0)).copy()
                        single = _to_uint8_hwc(single)
                        data = {f"{tag}/{idx}": Image(single)}
                        step = _norm_step(global_step)
                        seetrain_data.log(data=data, step=step, print_to_console=False)
                else:
                    arr = np.transpose(img_tensor, (1, 2, 0)).copy()
                    arr = _to_uint8_hwc(arr)
                    data = {tag: Image(arr)}
                    step = _norm_step(global_step)
                    seetrain_data.log(data=data, step=step, print_to_console=False)
            elif dataformats == 'NHWC':
                if img_tensor.ndim == 4:
                    for idx in range(img_tensor.shape[0]):
                        arr = _to_uint8_hwc(img_tensor[idx])
                        data = {f"{tag}/{idx}": Image(arr)}
                        step = _norm_step(global_step)
                        seetrain_data.log(data=data, step=step, print_to_console=False)
                else:
                    arr = _to_uint8_hwc(img_tensor)
                    data = {tag: Image(arr)}
                    step = _norm_step(global_step)
                    seetrain_data.log(data=data, step=step, print_to_console=False)
            else:
                if img_tensor.ndim == 4:
                    arr = img_tensor[0]
                else:
                    arr = img_tensor
                if arr.ndim == 3 and arr.shape[0] in (1, 3, 4):
                    arr = np.transpose(arr, (1, 2, 0)).copy()
                arr = _to_uint8_hwc(arr)
                data = {tag: Image(arr)}
                step = _norm_step(global_step)
                seetrain_data.log(data=data, step=step, print_to_console=False)
            return original_add_images(self, *args, **kwargs)

    if original_add_figure is not None:
        @functools.wraps(original_add_figure)
        def patched_add_figure(self, *args, **kwargs):
            if types_set is not None and 'image' not in types_set:
                return original_add_figure(self, *args, **kwargs)
            try:
                import numpy as np
                from matplotlib.figure import Figure
            except Exception:
                return original_add_figure(self, *args, **kwargs)
            tag, figure, global_step = _extract_args(
                args, kwargs, ['tag', 'figure', 'global_step']
            )
            if isinstance(figure, Figure):
                try:
                    figure.canvas.draw()
                    w, h = figure.canvas.get_width_height()
                    
                    # 兼容不同版本的 matplotlib
                    if hasattr(figure.canvas, 'tostring_rgb'):
                        buf_bytes = figure.canvas.tostring_rgb()
                    else:
                        buf_bytes = figure.canvas.tobytes()
                        
                    buf = np.frombuffer(buf_bytes, dtype=np.uint8)
                    
                    # 确保 buffer 长度正确
                    if len(buf) == w * h * 3:
                        arr = buf.reshape(h, w, 3)
                        data = {tag: Image(arr)}
                        step = _norm_step(global_step)
                        seetrain_data.log(data=data, step=step, print_to_console=False)
                    elif len(buf) == w * h * 4: # RGBA
                        arr = buf.reshape(h, w, 4)
                        data = {tag: Image(arr[:, :, :3])} 
                        step = _norm_step(global_step)
                        seetrain_data.log(data=data, step=step, print_to_console=False)
                except Exception:
                    pass
            return original_add_figure(self, *args, **kwargs)

    @functools.wraps(original_add_text)
    def patched_add_text(self, *args, **kwargs):
        if types_set is not None and 'text' not in types_set:
            return original_add_text(self, *args, **kwargs)
        tag, text_string, global_step = _extract_args(
            args, kwargs, ['tag', 'text_string', 'global_step']
        )
        text_string = str(text_string)
        data = {tag: Text(text_string)}
        step = _norm_step(global_step)
        seetrain_data.log(data=data, step=step, print_to_console=False)
        return original_add_text(self, *args, **kwargs)

    def patched_close(self):
        original_close(self)
        seetrain_data.finish()

    patched_methods = {
        '__init__': patched_init,
        'add_scalar': patched_add_scalar,
        'add_scalars': patched_add_scalars,
        'add_image': patched_add_image,
        'add_text': patched_add_text,
        'close': patched_close
    }
    
    if original_add_images is not None:
        patched_methods['add_images'] = patched_add_images
        
    if original_add_figure is not None:
        patched_methods['add_figure'] = patched_add_figure

    return patched_methods


def _apply_patches(SummaryWriter, patched_methods):
    """
    应用monkey patch到SummaryWriter类
    
    Args:
        SummaryWriter: SummaryWriter类
        patched_methods: 包含patch方法的字典
    """
    if getattr(SummaryWriter, "_seetrain_patched", False):
        return
    for method_name, patched_func in patched_methods.items():
        setattr(SummaryWriter, method_name, patched_func)
    try:
        setattr(SummaryWriter, "_seetrain_patched", True)
    except Exception:
        pass



def _sync_tensorboard_generic(import_func, logdir_extractor, types=None):
    """
    通用的tensorboard同步函数

    Args:
        import_func: 导入SummaryWriter的函数
        logdir_extractor: 提取logdir的函数
        types: 要同步的数据类型列表，如 ['scalar', 'scalars', 'image', 'text']。
               None 表示同步所有类型。
    """
    try:
        SummaryWriter = import_func()
    except ImportError as e:
        raise ImportError(f"Import failed: {e}")

    if getattr(SummaryWriter, "_seetrain_patched", False):
        return
    patched_methods = _create_patched_methods(SummaryWriter, logdir_extractor, types)
    _apply_patches(SummaryWriter, patched_methods)


def sync_tensorboardX(types=None):
    """
    同步tensorboardX到seetrain

    from tensorboardX import SummaryWriter
    import numpy as np
    import seetrain

    seetrain.sync_tensorboardX()

    seetrain.sync_tensorboardX(types=['scalar', 'scalars'])

    writer = SummaryWriter('runs/example')

    for i in range(100):
        scalar_value = np.random.rand()
        writer.add_scalar('random_scalar', scalar_value, i)

    writer.close()

    Args:
        types: 要同步的数据类型列表，可选值: 'scalar', 'scalars', 'image', 'text'。
               None 表示同步所有类型。
    """
    def import_tensorboardx():
        from tensorboardX import SummaryWriter
        return SummaryWriter

    def extract_logdir_tensorboardx(args, kwargs):
        logdir, _, _, _, _, _, _, log_dir, _ = _extract_args(
            args, kwargs,
            ['logdir', 'comment', 'purge_step', 'max_queue', 'flush_secs',
             'filename_suffix', 'write_to_disk', 'log_dir', 'comet_config']
        )
        val = logdir or log_dir
        if val is None:
            return None
        try:
            return os.fspath(val)
        except TypeError:
            return str(val)

    _sync_tensorboard_generic(import_tensorboardx, extract_logdir_tensorboardx, types)


def sync_tensorboard_torch(types=None):
    """
    同步torch自带的tensorboard到seetrain

    from torch.utils.tensorboard import SummaryWriter
    import numpy as np
    import seetrain

    seetrain.sync_tensorboard_torch()

    seetrain.sync_tensorboard_torch(types=['scalar', 'scalars'])

    writer = SummaryWriter('runs/example')

    for i in range(100):
        scalar_value = np.random.rand()
        writer.add_scalar('random_scalar', scalar_value, i)

    writer.close()

    Args:
        types: 要同步的数据类型列表，可选值: 'scalar', 'scalars', 'image', 'text'。
               None 表示同步所有类型。
    """
    def import_torch_tensorboard():
        from torch.utils.tensorboard import SummaryWriter
        return SummaryWriter

    def extract_logdir_torch(args, kwargs):
        logdir, _ = _extract_args(args, kwargs, ['log_dir', 'comment'])
        if logdir is None:
            return None
        try:
            return os.fspath(logdir)
        except TypeError:
            return str(logdir)

    _sync_tensorboard_generic(import_torch_tensorboard, extract_logdir_torch, types)
