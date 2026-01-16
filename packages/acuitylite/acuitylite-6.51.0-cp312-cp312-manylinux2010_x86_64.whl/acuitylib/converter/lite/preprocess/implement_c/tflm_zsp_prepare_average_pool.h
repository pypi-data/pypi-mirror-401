#ifndef __TFLM_ZSP_AVERAGE_POOL_H__
#define __TFLM_ZSP_AVERAGE_POOL_H__
#include <stdint.h>
#include "tflm_zsp_prepare_common.h"

typedef struct{
  TfLitePaddingValues padding;
  int32_t activation_min;
  int32_t activation_max;
  float activation_min_f32;
  float activation_max_f32;
}OpDataPooling;


typedef struct {
  int padding;
  int stride_width;
  int stride_height;
  int filter_width;
  int filter_height;
  int activation;
} TfLitePoolParams;


TfLiteStatus tflm_zsp_prepare_avgpool(
							OpDataPooling *op_data,
							TfLitePoolParams params,
							int32_t input_height,
							int32_t input_width,
							int32_t output_type,
							float output_param_scale,
							int32_t output_param_zeropoint
							);


#endif
