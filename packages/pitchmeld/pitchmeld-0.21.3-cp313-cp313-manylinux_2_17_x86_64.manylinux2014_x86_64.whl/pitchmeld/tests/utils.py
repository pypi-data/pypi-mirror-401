# Copyright (C) 2024 Gilles Degottex <contact@pitchmeld.ing> All Rights Reserved.

import logging

import os
import sys
import glob

import numpy as np
import soundfile

import pitchmeld

def assert_nan_inf(wav):
    idx = np.where(np.isnan(wav))[0]
    assert len(idx)==0

    idx = np.where(np.isinf(wav))[0]
    assert len(idx)==0

def assert_diff_sigs(ref, test, thresh_max=pitchmeld.float32.eps, thresh_rmse=pitchmeld.float32.eps):

    if ref.shape != test.shape:
        print(f"shape of the reference file is not the same as the test file: {ref.shape} vs. {test.shape}")
        return False, {'RMSE': np.nan, 'MAXE': np.nan}

    assert_nan_inf(test)

    err = ref - test

    RMSE = np.sqrt(np.mean(err**2))
    MAXE = max(abs(err))
    info = {'RMSE':pitchmeld.lin2db(RMSE), 'MAXE':pitchmeld.lin2db(MAXE)}

    ret = True

    if RMSE > thresh_rmse:
        logging.error(f"RMSE is {pitchmeld.lin2db(RMSE):.3f}dB > {pitchmeld.lin2db(thresh_rmse):.3f}dB")
        ret = False

    if MAXE > thresh_max:
        logging.error(f'Max diff {pitchmeld.lin2db(MAXE):.3f}dB > {pitchmeld.lin2db(thresh_max):.3f}dB')
        # err_idx = np.where(abs(err)>thresh_max)[0]
        # if len(err_idx)>0:
        #     for n in err_idx:
        #         logging.error(f'ref[{n}]={ref[n]} test[{n}]={test[n]} err={err[n]} ({pitchmeld.lin2db(err[n])}dB) > {thresh_max} ({pitchmeld.lin2db(thresh_max)}dB)')
        ret = False

    return ret, info


def filepaths_to_process():
    fpaths = glob.glob(f"{os.path.dirname(__file__)}/test_data/wav/*.wav")
    assert len(fpaths) > 0
    return fpaths


# def dir_refs(self):
#     return '../pitchmeld/sdk_python3/test_data/refs'

# def dir_output(self):
#     return 'test_data/sdk_python3'
