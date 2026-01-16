#ifndef __TFLM_ZSP_PREPARE_CONCATENATION_S8_H__
#define __TFLM_ZSP_PREPARE_CONCATENATION_S8_H__
#include "tflm_zsp_prepare_common.h"

typedef struct {
    int axis;
    TfLiteFusedActivation activation;
} TfLiteConcatenationParams;

typedef struct{
    uint16_t inputs_count;
    int32_t outer_size;
    int32_t copy_size0;
    int32_t copy_size1;
    int32_t copy_size2;
    int32_t copy_size3;
    int32_t copy_size4;
    int32_t copy_size5;
    int32_t copy_size6;
    int32_t copy_size7;
    int32_t copy_size8;
    int32_t copy_size9;
}OpDataConcatenation;

/**
 * Parameters:
 *             params                : Point to the struct TfLiteConcatenationParams data.
 *            input_dims_axis_data: The axis_value dimension of all input tensor.
 *
 *    Details:
 *        axis_value = params->axis > 0?  params->axis: params->axis + output_dims_size;
 *
 * **/

TfLiteStatus tflm_zsp_prepare_concatenation_s8(TfLiteConcatenationParams* params,
                                                int32_t output_type,
                                                int32_t node_inputs_size,
                                                int32_t output_dims_size,
                                                int32_t* output_dims_data,
                                                int32_t* input_dims_axis_data,
                                                OpDataConcatenation *data);
#endif
