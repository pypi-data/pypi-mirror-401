#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include "tflm_zsp_prepare_conv2d.h"
#include "tflm_zsp_padding.h"


TfLiteStatus tflm_zsp_prepare_conv2d(TfLiteConvParams params, int32_t input_width, int32_t input_height, int32_t filter_width,int32_t filter_height, int32_t out_width, int32_t out_height, int32_t input_type, float input_param_scale, int32_t input_param_zeropoint_t, float filter_param_scale, int32_t filter_quant_scale_size, float* filter_quant_scale_data, int32_t filter_param_zeropoint_t, int32_t output_type, float output_param_scale, int32_t output_param_zeropoint_t, int32_t output_channels, OpDataConv* data)
{
	data->padding = ComputePaddingHeightWidth(
      params.stride_height, params.stride_width, params.dilation_height_factor,
      params.dilation_width_factor, input_height, input_width, filter_height, filter_width,
      params.padding, &out_height, &out_width);

	if (input_type != kTfLiteFloat32) {
		PopulateConvolutionQuantizationParams(input_type, input_param_scale, filter_param_scale, filter_quant_scale_size, filter_quant_scale_data, output_type, output_param_scale, output_param_zeropoint_t, params.activation, &data->output_multiplier, &data->output_shift, &data->output_activation_min, &data->output_activation_max, data->per_channel_output_multiplier, (int32_t*) data->per_channel_output_shift, output_channels);
	}

	data->input_zero_point = input_param_zeropoint_t;
	data->filter_zero_point = filter_param_zeropoint_t;
	data->output_zero_point = output_param_zeropoint_t;


	return kTfLiteOk;
}


