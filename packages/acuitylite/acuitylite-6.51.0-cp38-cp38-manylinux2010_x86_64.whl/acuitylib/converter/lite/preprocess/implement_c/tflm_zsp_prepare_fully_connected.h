#ifndef __TFLM_ZSP_PREPARE_FULLY_CONNECTED_H__
#define __TFLM_ZSP_PREPARE_FULLY_CONNECTED_H__

#include "tflm_zsp_prepare_common.h"


typedef struct {
  // The scaling factor from input to output (aka the 'real multiplier') can
  // be represented as a fixed point multiplier plus a left shift.
  int32_t output_multiplier;
  int output_shift;
  // The range of the fused activation layer. For example for kNone and
  // uint8_t these would be 0 and 255.
  int32_t output_activation_min;
  int32_t output_activation_max;
  // Cached zero point values of tensors.
  int32_t input_zero_point;
  int32_t filter_zero_point;
  int32_t output_zero_point;
} OpDataFullyConnected;



TfLiteStatus tflm_zsp_prepare_fullyconnected(
								OpDataFullyConnected *data,
								int32_t node_builtin_activation,
								int32_t is_exist_bias,
								const float input_param_scale,
								const float filter_param_scale,
								const float	bias_param_scale,
								const float output_param_scale,
								int32_t input_param_zero_point,
								int32_t filter_param_zero_point,
								int32_t output_param_zero_point
								);

#endif
