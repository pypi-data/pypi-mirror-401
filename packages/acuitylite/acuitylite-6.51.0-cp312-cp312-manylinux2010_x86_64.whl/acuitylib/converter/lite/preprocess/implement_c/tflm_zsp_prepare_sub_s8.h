#ifndef __TFLM_ZSP_PREPARE_SUB_S8_H__
#define __TFLM_ZSP_PREPARE_SUB_S8_H__
#include "tflm_zsp_prepare_common.h"

typedef struct {
    TfLiteFusedActivation activation;
    int pot_scale_int16;
} TfLiteSubParams;

typedef struct {
    int32_t requires_broadcast;

    // These fields are used in both the general 8-bit -> 8bit quantized path,
    // and the special 16-bit -> 16bit quantized path
    int input1_shift;
    int input2_shift;
    int32_t output_activation_min;
    int32_t output_activation_max;

    // These fields are used only in the general 8-bit -> 8bit quantized path
    int32_t input1_multiplier;
    int32_t input2_multiplier;
    int32_t output_multiplier;
    int output_shift;
    int left_shift;
    int32_t input1_offset;
    int32_t input2_offset;
    int32_t output_offset;
    //(params_type == 0)? input1_is_constvalue, input2_is_constvalue;
    int32_t params_type;
} OpDataSub;

TfLiteStatus tflm_zsp_prepare_elementwise_sub_s8(TfLiteSubParams* params,
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
                                    OpDataSub* data);


#endif
