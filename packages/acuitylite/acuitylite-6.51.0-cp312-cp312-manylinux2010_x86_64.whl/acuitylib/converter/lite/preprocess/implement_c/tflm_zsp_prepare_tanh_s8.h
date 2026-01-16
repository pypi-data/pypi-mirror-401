#ifndef __TFLM_ZSP_PREPARE_TANH_S8_H__
#define __TFLM_ZSP_PREPARE_TANH_S8_H__
#include "tflm_zsp_prepare_common.h"

typedef struct{
    int32_t input_zero_point;
    int32_t input_range_radius;
    int32_t input_multiplier;
    int32_t input_left_shift;
    int32_t output_activation_max;
    int32_t output_activation_min;
    int32_t output_size;
}OpDataTanh;

TfLiteStatus tflm_zsp_prepare_tanh_s8(OpDataTanh *data,
                                        int32_t input_params_zero_point,
                                        int32_t* output_dims_data,
                                        int32_t output_dims_size,
                                        double input_params_scale);

#endif //__TFLM_ZSP_PREPARE_TANH_S8_H__
