#include "tflm_zsp_prepare_tanh_s8.h"

TfLiteStatus tflm_zsp_prepare_tanh_s8(OpDataTanh *data,
                                    int32_t input_params_zero_point,
                                    int32_t* output_dims_data,
                                    int32_t output_dims_size,
                                    double input_params_scale)
{
    int32_t output_size = 1;
    int32_t i = 1;

    double multiplier = input_params_scale * (1LL << 27);

    data->input_zero_point = input_params_zero_point;

    QuantizeMultiplier(multiplier, &data->input_multiplier, &data->input_left_shift);

    int64_t tmp = (1 << 4)  - 1;
    tmp <<= (31 - 4);
    tmp >>= data->input_left_shift;
    data->input_range_radius = (int32_t)tmp;

    data->output_activation_min = -128;
    data->output_activation_max = 127;

    output_size = 1;
    for(i= 0; i< output_dims_size ; i++){
        output_size *= output_dims_data[i];
    }
    data->output_size = output_size;

    return kTfLiteOk;
}

