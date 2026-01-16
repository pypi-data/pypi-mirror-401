#include "tflm_zsp_prepare_quantize.h"
#include "tflm_zsp_prepare_common.h"

TfLiteStatus tflm_zsp_prepare_quantize(OpDataQuantizeReference *data,
									float input_params_scale,
									float output_params_scale,
									int32_t input_params_zero_point,
									int32_t output_params_zero_point){

	double effective_scale = (double) (input_params_scale/output_params_scale);

    QuantizeMultiplier(effective_scale, &data->requantize_output_multiplier,
                       &data->requantize_output_shift);

    data->quantization_params.zero_point = output_params_zero_point;
    data->quantization_params.scale = (double)(output_params_scale);

    data->input_zero_point = input_params_zero_point;


    return  kTfLiteOk;
}
