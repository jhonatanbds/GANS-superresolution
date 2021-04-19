from ISR.models import RDN
from ISR.models import Cut_VGG19
from ISR.models import Discriminator

lr_train_patch_size = 40
layers_to_extract = [5, 9]
scale = 4
hr_train_patch_size = lr_train_patch_size * scale

rrdn  = RDN(arch_params={'C':6, 'D':20, 'G':64, 'G0':64, 'x':scale}, patch_size=lr_train_patch_size)
# rrdn  = RRDN(arch_params={'C':4, 'D':3, 'G':64, 'G0':64, 'T':10, 'x':scale}, patch_size=lr_train_patch_size)

f_ext = Cut_VGG19(patch_size=hr_train_patch_size, layers_to_extract=layers_to_extract)
discr = Discriminator(patch_size=hr_train_patch_size, kernel_size=3)

from ISR.train import Trainer

loss_weights = {
  'generator': 0.2,
  'feature_extractor': 0.0833,
  'discriminator': 0.01
}
losses = {
  'generator': 'mae',
  'feature_extractor': 'mse',
  'discriminator': 'binary_crossentropy'
}

log_dirs = {'logs': './logs', 'weights': './weights'}

learning_rate = {'initial_value': 0.0004, 'decay_factor': 0.5, 'decay_frequency': 30}

flatness = {'min': 0.0, 'max': 0.15, 'increase': 0.01, 'increase_frequency': 5}

adam_optimizer = {'beta1': 0.9, 'beta2': 0.999, 'epsilon': None}

trainer = Trainer(
    generator=rrdn,
    discriminator=discr,
    feature_extractor=f_ext,
    lr_train_dir='/media/jhonatan/Data/h6f86gl(2)/final/X4/lr_train',
    hr_train_dir='/media/jhonatan/Data/h6f86gl(2)/final/hr_train',
    lr_valid_dir='/media/jhonatan/Data/h6f86gl(2)/final/X4/lr_val',
    hr_valid_dir='/media/jhonatan/Data/h6f86gl(2)/final/hr_val',
    loss_weights=loss_weights,
    losses=losses,
    learning_rate=learning_rate,
    flatness=flatness,
    log_dirs=log_dirs,
    adam_optimizer=adam_optimizer,
    metrics={'generator': 'PSNR_Y'},
    dataname='SSIG',
    weights_generator=None,
    weights_discriminator=None,
    n_validation=50,
)

trainer.train(
    epochs=500,
    steps_per_epoch=60,
    batch_size=8,
    monitored_metrics = {'val_generator_PSNR_Y': 'min'}
)

