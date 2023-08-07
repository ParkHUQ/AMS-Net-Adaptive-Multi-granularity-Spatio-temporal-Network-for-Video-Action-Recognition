_base_ = [
    '../../_base_/models/tpn_tsn_r50.py', '../../_base_/default_runtime.py'
]

dataset_type = 'RawframeDataset'
data_root = '/ssd/dataset/video/RGB/STH-V1/20bn-something-something-v1'
data_root_val = '/ssd/dataset/video/RGB/STH-V1/20bn-something-something-v1'
ann_file_train = '/ssd/dataset/video/RGB/STH-V1/train_videofolder.txt'
ann_file_val = '/ssd/dataset/video/RGB/STH-V1/val_videofolder.txt'
ann_file_test = '/ssd/dataset/video/RGB/STH-V1/val_videofolder.txt'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_bgr=False)

train_pipeline = [
    dict(type='SampleFrames', clip_len=1, frame_interval=1, num_clips=8),
    #dict(type='FrameSelector'),
    dict(type='RawFrameDecode'),
    dict(type='RandomResizedCrop'),
    dict(type='Resize', scale=(112, 112), keep_ratio=False),
    dict(type='Flip', flip_ratio=0.5),
    dict(type='ColorJitter', color_space_aug=True),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs', 'label'])
]
val_pipeline = [
    dict(
        type='SampleFrames',
        clip_len=1,
        frame_interval=1,
        num_clips=8,
        test_mode=True),
    #dict(type='FrameSelector'),
    dict(type='RawFrameDecode'),
    dict(type='Resize', scale=(-1, 128)),
    dict(type='CenterCrop', crop_size=112),
    dict(type='ColorJitter', color_space_aug=True),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs'])
]
test_pipeline = [
    dict(
        type='SampleFrames',
        clip_len=1,
        frame_interval=1,
        num_clips=16,
        test_mode=True),
    #dict(type='FrameSelector'),
    dict(type='RawFrameDecode'),
    dict(type='Resize', scale=(-1, 128)),
    dict(type='ThreeCrop', crop_size=128),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='FormatShape', input_format='NCHW'),
    dict(type='Collect', keys=['imgs', 'label'], meta_keys=[]),
    dict(type='ToTensor', keys=['imgs'])
]
data = dict(
    videos_per_gpu=8,
    workers_per_gpu=8,
    test_dataloader=dict(videos_per_gpu=12),
    train=dict(
        type=dataset_type,
        ann_file=ann_file_train,
        data_prefix=data_root,
        filename_tmpl='{:05d}.jpg',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file=ann_file_val,
        data_prefix=data_root_val,
        filename_tmpl='{:05d}.jpg',
        pipeline=val_pipeline),
    test=dict(
        type=dataset_type,
        ann_file=ann_file_test,
        data_prefix=data_root_val,
        filename_tmpl='{:05d}.jpg',
        pipeline=val_pipeline))
evaluation = dict(
    interval=1, metrics=['top_k_accuracy', 'mean_class_accuracy'])

# optimizer
optimizer = dict(
    type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0005,
    nesterov=True)  # this lr is used for 8 gpus
optimizer_config = dict(grad_clip=dict(max_norm=20, norm_type=2))
# learning policy
lr_config = dict(policy='step', step=[75, 125])
total_epochs = 150

# runtime settings

work_dir = './work_dirs/tpn_tsm_r50_1x1x8_150e_sthv1_rgb_1'
