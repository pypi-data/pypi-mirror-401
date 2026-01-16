#include "tflm_zsp_prepare_elementwise_add_s8.h"
#include "tflm_zsp_prepare_common.h"


TfLiteStatus tflm_zsp_prepare_elementwise_add_s8(TfLiteAddParams* params,
        int32_t input1_params_zeropoint,
        int32_t input2_params_zeropoint,
        int32_t output_params_zeropoint,
        int32_t input1_dims_size,
        int32_t input2_dims_size,
        int32_t* input1_dims_data,
        int32_t* input2_dims_data,
        float input1_params_scale,
        float input2_params_scale,
        float output_params_scale,
        int32_t output_type,
        OpDataAdd* data){

    int32_t dims_count = max(input1_dims_size, input2_dims_size);
    int32_t extended_shape1[10];
    int32_t extended_shape2[10];
    int32_t extended_shape1_size = dims_count - input1_dims_size;
    int32_t extended_shape2_size = dims_count - input2_dims_size;
    int32_t i = 0;

    for(i=0; i< extended_shape1_size; i++){
        extended_shape1[i] = 1;
    }
    for(i= 0; i< input1_dims_size; i++){
        extended_shape1[i + extended_shape1_size] = input1_dims_data[i];
    }

    for(i=0; i< extended_shape2_size; i++){
        extended_shape2[i] = 1;
    }
    for(i= 0; i< input2_dims_size; i++){
        extended_shape2[i + extended_shape2_size] = input2_dims_data[i];
    }

    data->params_type = 0;
    for(int32_t i= dims_count - 1; i >= 0; --i){
        if(extended_shape1[i] == extended_shape2[i]){
            continue;
        }else if(extended_shape1[i] == 1){
            data->params_type = 1;
            break;
        }else if(extended_shape2[i] == 1){
            data->params_type = 2;
            break;
        }else{
            return kTfLiteError;
        }
    }

    data->input1_offset = -input1_params_zeropoint;
    data->input2_offset = -input2_params_zeropoint;
    data->output_offset = output_params_zeropoint;

    data->left_shift =  (output_type == kTfLiteInt16) ? 15 : 20;

    const double twice_max_input_scale = (double)2.0 * max(input1_params_scale, input2_params_scale);
    const double real_input1_multiplier = (double)input1_params_scale/twice_max_input_scale;
    const double real_input2_multiplier = (double)input2_params_scale/twice_max_input_scale;
    const double real_output_multiplier = twice_max_input_scale/((1<<data->left_shift) * (double)output_params_scale);

    QuantizeMultiplierSmallerThanOneExp((double)real_input1_multiplier, &data->input1_multiplier,
            &data->input1_shift);

    QuantizeMultiplierSmallerThanOneExp((double)real_input2_multiplier, &data->input2_multiplier,
            &data->input2_shift);

    QuantizeMultiplierSmallerThanOneExp((double)real_output_multiplier, &data->output_multiplier,
            &data->output_shift);

    CalculateActivationRangeQuantized( params->activation,
                                        output_type,
                                        output_params_scale,
                                        output_params_zeropoint,
                                        &data->output_activation_min,
                                        &data->output_activation_max);

    return kTfLiteOk;
}
