#ifndef __TFLM_ZSP_PREPARE_HARDSWISH_S8_H__
#define __TFLM_ZSP_PREPARE_HARDSWISH_S8_H__
#include "tflm_zsp_prepare_common.h"

typedef struct{
    int16_t input_zero_point;
    int16_t output_zero_point;
    int16_t reluish_multiplier;
    int32_t reluish_multiplier_exponent;
    int16_t output_multiplier;
    int32_t output_multiplier_exponent;
}OpDataHardSwish;

TfLiteStatus tflm_zsp_prepare_hardswish_s8(OpDataHardSwish* data,
                                            int32_t input_params_zero_point,
                                            int32_t output_params_zero_point,
                                            float input_params_scale,
                                            float output_params_scale);

#endif //__TFLM_ZSP_PREPARE_HARDSWISH_S8_H__
