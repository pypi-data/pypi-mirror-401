#include "tflm_zsp_prepare_hardswish_s8.h"

TfLiteStatus tflm_zsp_prepare_hardswish_s8(OpDataHardSwish* data,
                                            int32_t input_params_zero_point,
                                            int32_t output_params_zero_point,
                                            float input_params_scale,
                                            float output_params_scale)

{
    int32_t output_multiplier_fixedpoint_int32;
    int32_t reluish_multiplier_fixedpoint_int32;

    float hires_input_scale = (1.0f / 128.0f) * input_params_scale;
    float reluish_scale = 3.0f / 32768.0f;
    double output_multiplier = hires_input_scale / output_params_scale;
    double reluish_multiplier = hires_input_scale / reluish_scale;
    data->input_zero_point = input_params_zero_point;
    data->output_zero_point = output_params_zero_point;
    QuantizeMultiplier(output_multiplier, &output_multiplier_fixedpoint_int32, &data->output_multiplier_exponent);
    data->output_multiplier = (int16_t)((int64_t)output_multiplier_fixedpoint_int32 + (1LL << 15)) >> 16;
    QuantizeMultiplier(reluish_multiplier, &reluish_multiplier_fixedpoint_int32, &data->reluish_multiplier_exponent);
    data->reluish_multiplier = (int16_t)((int64_t)reluish_multiplier_fixedpoint_int32 + (1LL << 15)) >> 16;

    return kTfLiteOk;
}

