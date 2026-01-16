#include "tflm_zsp_prepare_mul_s8.h"

TfLiteStatus tflm_zsp_prepare_elementwise_mul_s8(TfLiteMulParams* params,
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
                                    int32_t *output_dim_data,
                                    int32_t output_dims_size,
                                    OpDataMul* data)
{
    int32_t output_size = 1;
    int32_t i = 0;
    int32_t dims_count = max(input1_dims_size, input2_dims_size);
    int32_t extended_shape1[10];
    int32_t extended_shape2[10];
    int32_t extended_shape1_size = dims_count - input1_dims_size;
    int32_t extended_shape2_size = dims_count - input2_dims_size;

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

    if (output_type == kTfLiteInt8 || output_type == kTfLiteInt16) {
        CalculateActivationRangeQuantized(params->activation, output_type,
                                        output_params_scale,output_params_zeropoint,
                                        &data->output_activation_min, &data->output_activation_max);

        double  real_multiplier = input1_params_scale * input2_params_scale / output_params_scale;

        QuantizeMultiplier(real_multiplier, &data->output_multiplier,&data->output_shift);

        data->input1_zero_point = -input1_params_zeropoint;
        data->input2_zero_point = -input2_params_zeropoint;
        data->output_zero_point = output_params_zeropoint;

        if (output_type == kTfLiteInt16) {
            if(data->input1_zero_point != 0 || (data->input2_zero_point != 0) || (data->output_zero_point != 0))
                return kTfLiteError;
        }
    }
    else if (output_type == kTfLiteInt32) {
        CalculateActivationRange_s32(params->activation,
                                    &data->output_activation_min,
                                    &data->output_activation_max);
    }


    for(i = 0;i< output_dims_size;i++){
        output_size *= output_dim_data[i];
    }

    data->output_size = output_size;

    return  kTfLiteOk;
}
