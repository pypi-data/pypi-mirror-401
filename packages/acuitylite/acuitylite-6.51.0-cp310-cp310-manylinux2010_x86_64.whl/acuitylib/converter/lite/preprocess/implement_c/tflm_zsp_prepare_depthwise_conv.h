#ifndef __TFLM_ZSP_PREPARE_DEPTHWISE_CONV_H__
#define __TFLM_ZSP_PREPARE_DEPTHWISE_CONV_H__
#include "tflm_zsp_prepare_common.h"


typedef struct{
	TfLitePaddingValues padding;

	int32_t input_zero_point;
	int32_t filter_zero_point;
	int32_t output_zero_point;

	int32_t output_multiplier;
	int output_shift;

	int32_t* per_channel_output_multiplier;
	int32_t* per_channel_output_shift;

	int32_t output_activation_min;
	int32_t output_activation_max;

	int filter_buffer_index;
}OpDataConv;



typedef struct {
  // Parameters for DepthwiseConv version 1 or above.
  TfLitePadding padding;
  int stride_width;
  int stride_height;
  // `depth_multiplier` is redundant. It's used by CPU kernels in
  // TensorFlow 2.0 or below, but ignored in versions above.

  // The information can be deduced from the shape of input and the shape of
  // weights. Since the TFLiteConverter toolchain doesn't support partially
  // specified shapes, relying on `depth_multiplier` stops us from supporting
  // graphs with dynamic shape tensors.

  // Note: Some of the delegates (e.g. NNAPI, GPU) are still relying on this
  // field.
  int depth_multiplier;
  int activation;
  // Parameters for DepthwiseConv version 2 or above.
  int dilation_width_factor;
  int dilation_height_factor;
} TfLiteDepthwiseConvParams;


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
								);




#endif
