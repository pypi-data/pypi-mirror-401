#ifndef __TFLM_ZSP_PREPARE_QUANTIZE_H__
#define __TFLM_ZSP_PREPARE_QUANTIZE_H__

#include <stdint.h>
#include "tflm_zsp_prepare_common.h"


typedef struct{
  int32_t zero_point;
  double scale;
} QuantizationParams;

typedef struct{
  QuantizationParams quantization_params;
  // The scaling factor from input to output (aka the 'real multiplier') can
  // be represented as a fixed point multiplier plus a left shift.
  int32_t requantize_output_multiplier;
  int requantize_output_shift;

  int32_t input_zero_point;
} OpDataQuantizeReference;



TfLiteStatus tflm_zsp_prepare_quantize(OpDataQuantizeReference *data,
									float input_params_scale,
									float output_params_scale,
									int32_t input_params_zero_point,
									int32_t output_params_zero_point);


#endif
