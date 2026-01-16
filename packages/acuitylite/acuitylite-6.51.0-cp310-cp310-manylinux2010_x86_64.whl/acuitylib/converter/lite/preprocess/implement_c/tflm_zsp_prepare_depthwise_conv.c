#include "tflm_zsp_prepare_depthwise_conv.h"
#include "tflm_zsp_padding.h"
#include <stdlib.h>
#include <stdbool.h>

TfLiteStatus tflm_zsp_prepare_depthwise_conv(
								OpDataConv *data,
								const TfLiteDepthwiseConvParams params,
								int32_t input_type,
								int32_t output_type,
								int32_t node_builtin_activation,
								int32_t input_width,
								int32_t input_height,
								int32_t filter_width,
								int32_t filter_height,
								int32_t output_width,
								int32_t output_height,
								const float input_param_scale,
								const float filter_param_scale,
								const float output_param_scale,
								const float* filter_quant_scale_data,
								int32_t filter_quant_scale_size,
								int32_t input_param_zeropoint,
								int32_t filter_param_zeropoint,
								int32_t output_param_zeropoint,
								int32_t output_channels
								){

	data->padding = ComputePaddingHeightWidth(
								params.stride_height, params.stride_width, params.dilation_height_factor,
								params.dilation_width_factor, input_height, input_width, filter_height,
								filter_width, params.padding, &output_height, &output_width);


	if(!filter_quant_scale_size)
		return kTfLiteError;

	const bool is_per_channel = filter_quant_scale_size > 1;

	if(is_per_channel){
		if(filter_quant_scale_size != output_channels)
			return kTfLiteError;

	}

	if(input_type != kTfLiteFloat32){

		PopulateConvolutionQuantizationParams(input_type,
											input_param_scale,
											filter_param_scale,
											filter_quant_scale_size,
											(float *)filter_quant_scale_data,
											output_type,
											output_param_scale,
											output_param_zeropoint,
											node_builtin_activation,
											&data->output_multiplier,
											&data->output_shift,
											&data->output_activation_min,
											&data->output_activation_max,
											data->per_channel_output_multiplier,
											data->per_channel_output_shift,
											output_channels);
	}


	data->input_zero_point =  input_param_zeropoint;
	data->filter_zero_point = filter_param_zeropoint;
	data->output_zero_point = output_param_zeropoint;

	return kTfLiteOk;

}
