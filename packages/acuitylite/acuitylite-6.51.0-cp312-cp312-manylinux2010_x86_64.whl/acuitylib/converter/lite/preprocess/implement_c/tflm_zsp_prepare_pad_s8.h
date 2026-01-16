#ifndef __TFLM_ZSP_PREPARE_PAD_S8_H__
#define __TFLM_ZSP_PREPARE_PAD_S8_H__
#include "tflm_zsp_prepare_common.h"

typedef struct{
    int32_t    left_b_padding;
    int32_t    left_p_padding;
    int32_t    left_h_padding;
    int32_t left_w_padding;
    int32_t left_d_padding;

    int32_t right_b_padding;
    int32_t right_p_padding;
    int32_t right_h_padding;
    int32_t right_w_padding;
    int32_t right_d_padding;

    int32_t output_shape0;
    int32_t output_shape1;
    int32_t output_shape2;
    int32_t output_shape3;
    int32_t output_shape4;
    int32_t pad_value;
}OpDataPad;
/**
 * Parameters:
 *        node_inputs_constant_value_data: Pointer to the constant value that exists if (node_num_inputs == 3)
 *        node_num_inputs                   : node->inputs->size
 *
 * node_inputs_constant_value_data = (node_num_inputs == 3)? GetEvalInput(context, node, 2): nullptr;
 *
 * */


TfLiteStatus tflm_zsp_prepare_pad_s8(int32_t *paddings_data,
                                    int32_t *output_dims_data,
                                    int32_t input_type,
                                    int32_t input_dims_size,
                                    int32_t node_num_inputs,
                                    int32_t *node_inputs_constant_value_data,
                                    int32_t output_params_zero_point,
                                    OpDataPad *data);

#endif

