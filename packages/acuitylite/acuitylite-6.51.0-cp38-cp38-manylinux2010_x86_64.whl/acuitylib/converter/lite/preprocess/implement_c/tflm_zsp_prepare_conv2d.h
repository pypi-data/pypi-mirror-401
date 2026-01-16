#ifndef __TFLM_ZSP_PREPARE_CONV2D_H__
#define __TFLM_ZSP_PREPARE_CONV2D_H__


#include "tflm_zsp_prepare_common.h"

typedef struct{
  TfLitePaddingValues padding;

  // Cached tensor zero point values for quantized operations.
  int32_t input_zero_point;
  int32_t filter_zero_point;
  int32_t output_zero_point;

  // The scaling factor from input to output (aka the 'real multiplier') can
  // be represented as a fixed point multiplier plus a left shift.
  int32_t output_multiplier;
  int output_shift;

  // Per channel output multiplier and shift.
  int32_t* per_channel_output_multiplier;
  int32_t* per_channel_output_shift;

  // The range of the fused activation layer. For example for kNone and
  // uint8_t these would be 0 and 255.
  int32_t output_activation_min;
  int32_t output_activation_max;

  // A buffer used to store unpacked filter values. This is used if the source
  // tensor is of n-bit precision that cannot be easily processed by kernels.
  int filter_buffer_index;
} OpDataConv;

typedef struct {
  // Parameters for CONV_2D version 1.
  int padding;
  int stride_width;
  int stride_height;
  int activation;

  // Parameters for CONV_2D version 2.
  // Note: Version 2 supports dilation values not equal to 1.
  int dilation_width_factor;
  int dilation_height_factor;

  // Parameters for CONV_2D version 7 or above.
  // Used to determine the default value for the quantized bias.
  int quantized_bias_type;
} TfLiteConvParams;

TfLiteStatus tflm_zsp_prepare_conv2d(TfLiteConvParams params, int32_t input_width, int32_t input_height, int32_t filter_width,int32_t filter_height, int32_t out_width, int32_t out_height, int32_t input_type, float input_param_scale, int32_t input_param_zeropoint_t, float filter_param_scale, int32_t filter_quant_scale_size, float* filter_quant_scale_data, int32_t filter_param_zeropoint_t, int32_t output_type, float output_param_scale, int32_t output_param_zeropoint_t, int32_t output_channels, OpDataConv* data);

#endif //__TFLM_ZSP_PREPARE_CONV2D_H__
