#ifndef TFLM_ZSP_PREPARE_SOFTMAX_H__
#define TFLM_ZSP_PREPARE_SOFTMAX_H__
#include "tflm_zsp_prepare_common.h"
#include <stdint.h>

typedef struct{

  // beta is not really used (not a Tensorflow parameter) and not implemented
  // for LogSoftmax.
  double beta;
  // uint8_t inference params.  Used even when beta defaults to 1.0.
  int32_t input_multiplier;
  int32_t input_left_shift;
  // Reverse scaling is only used by LogSoftmax.
  int32_t reverse_scaling_divisor;
  int32_t reverse_scaling_right_shift;
  int diff_min;
  int32_t zero_point;
  float scale;

}SoftmaxParams;

typedef struct {
  float beta;
} TfLiteSoftmaxParams;

TfLiteStatus tflm_zsp_prepare_softmax(
							SoftmaxParams *op_data,
							TfLiteSoftmaxParams params,
							int32_t input_type,
							int32_t output_type,
							const float input_params_scale,
							const float output_params_scale,
							int output_params_zeropoint);


#endif
