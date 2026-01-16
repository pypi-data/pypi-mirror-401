#include "tflm_zsp_prepare_pad_s8.h"

TfLiteStatus tflm_zsp_prepare_pad_s8(int32_t *paddings_data,
                                    int32_t *output_dims_data,
                                    int32_t input_type,
                                    int32_t input_dims_size,
                                    int32_t node_num_inputs,
                                    int32_t *node_inputs_constant_value_data,
                                    int32_t output_params_zero_point,
                                    OpDataPad *data)
{
    int32_t pad_count = 5 - input_dims_size;
    int32_t left_padding_copy[5] = {0};
    int32_t right_padding_copy[5] = {0};
    int32_t *output_shape = (int32_t *)&data->output_shape0;

    for(int32_t i = 0; i<pad_count; i++){
        left_padding_copy[i] = 0;
        right_padding_copy[i] = 0;
        output_shape[i] = 1;
    }

    for(int32_t i = 0;i<input_dims_size;i++){
        left_padding_copy[i + pad_count] = paddings_data[2 * i];
        right_padding_copy[i + pad_count] = paddings_data[2 * i + 1];
        output_shape[i + pad_count] = output_dims_data[i];
    }

    data->left_b_padding = left_padding_copy[0];
    data->left_p_padding = left_padding_copy[1];
    data->left_h_padding = left_padding_copy[2];
    data->left_w_padding = left_padding_copy[3];
    data->left_d_padding = left_padding_copy[4];

    data->right_b_padding = right_padding_copy[0];
    data->right_p_padding = right_padding_copy[1];
    data->right_h_padding = right_padding_copy[2];
    data->right_w_padding = right_padding_copy[3];
    data->right_d_padding = right_padding_copy[4];

    data->pad_value = output_params_zero_point;
    if(node_num_inputs == 3){
        if(node_inputs_constant_value_data != 0)
            data->pad_value = *node_inputs_constant_value_data;
    }

    return kTfLiteOk;
}

