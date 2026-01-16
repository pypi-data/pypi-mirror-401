#ifndef __TFLM_ZSP_PREPARE_UNPACK_S8_H__
#define __TFLM_ZSP_PREPARE_UNPACK_S8_H__
#include "tflm_zsp_prepare_common.h"


typedef struct {
  int num;
  int axis;
} TfLiteUnpackParams;


typedef struct{
  int32_t num;
  int32_t copy_size;
  int32_t outer_size;
}OpDataUnpack;


TfLiteStatus tflm_zsp_prepare_unpack_s8(TfLiteUnpackParams* params,
                                                int32_t input_data_type,
                                                int32_t *input_dims_data,
                                                int32_t input_dims_size,
                                                OpDataUnpack *data);
#endif
