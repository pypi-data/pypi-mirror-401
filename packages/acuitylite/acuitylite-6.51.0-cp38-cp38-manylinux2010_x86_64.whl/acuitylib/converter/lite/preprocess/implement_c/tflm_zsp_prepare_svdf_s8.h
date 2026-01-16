#ifndef __TFLM_ZSP_PREPARE_SVDF_S8_H__
#define __TFLM_ZSP_PREPARE_SVDF_S8_H__
#include <stdint.h>
#include "tflm_zsp_prepare_common.h"


typedef struct{
  int32_t effective_scale_1_a;
  int32_t effective_scale_2_a;
  // b versions of each scale are kept at int since the numbers are just the
  // shift value - typically between [-32, 32].
  int effective_scale_1_b;
  int effective_scale_2_b;

  // Cached tensor zero point values for quantized operations.
  int input_zero_point;
  int output_zero_point;
  int activation_state_zero_point;
} OpDataSvdf;


TfLiteStatus tflm_zsp_prepare_svdf(OpDataSvdf *data,
									float input_params_scale,
									float weight_feature_params_scale,
									float activation_state_params_scale,
									float weights_time_params_scale,
									float output_params_scale,
									int32_t input_params_zero_point,
									int32_t output_params_zero_point,
									int32_t	activation_state_params_zero_point);


#endif
