#ifndef __TFLM_ZSP_PREPARE_MUL_S8_H__
#define __TFLM_ZSP_PREPARE_MUL_S8_H__
#include "tflm_zsp_prepare_common.h"

typedef struct {
    TfLiteFusedActivation activation;
} TfLiteMulParams;

typedef struct{
    int32_t input1_zero_point;
    int32_t input2_zero_point;

    int32_t output_activation_min;
    int32_t output_activation_max;
    int32_t output_zero_point;
    int32_t output_multiplier;
    int32_t output_shift;

    int32_t output_size;
    int32_t params_type;
}OpDataMul;

TfLiteStatus tflm_zsp_prepare_elementwise_mul_s8(TfLiteMulParams* params,
                                    int32_t input1_params_zero_point,
                                    int32_t input2_params_zero_point,
                                    int32_t output_params_zero_point,
                                    int32_t input1_dims_size,
                                    int32_t input2_dims_size,
                                    int32_t* input1_dims_data,
                                    int32_t* input2_dims_data,
                                    float input1_params_scale,
                                    float input2_params_scale,
                                    float output_params_scale,
                                    int32_t output_type,
                                    int32_t *output_dim_data,
                                    int32_t output_dims_size,
                                    OpDataMul* data);


#endif
