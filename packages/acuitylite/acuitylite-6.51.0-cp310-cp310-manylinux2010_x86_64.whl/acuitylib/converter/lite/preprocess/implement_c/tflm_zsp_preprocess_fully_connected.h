
#ifndef __TFLM_ZSP_PREPROCESS_FULLY_CONNECTED_H__
#define __TFLM_ZSP_PREPROCESS_FULLY_CONNECTED_H__

#include <stdint.h>
#include "tflm_zsp_preprocess_common.h"

/******************
*  row_num : 	output_dim_c
*  col_num:		filter_dim_n
*
*  pDst: size = output_dim_c * filter_dim_n;
*
*******************/
void tflm_zsp_filter_trans_int8_fullconnected(int8_t *data_src, int8_t* data_dst, int32_t row_num, int32_t col_num);

/******************
*
*  data_output: size = sizeof(int64_t) + output_dim_c * sizeof(int32_t);
*
******************/

void tflm_zsp_preprocess_fullconnected(int32_t *data_output, const int32_t *data_bias, const int8_t *data_filter ,int32_t filter_offset, int32_t input_offset, int32_t filter_dim_n, int32_t output_dim_c, int32_t output_multiplier,int32_t quantized_activation_max,int32_t quantized_activation_min, int32_t output_offset, int32_t output_shift);

#endif
