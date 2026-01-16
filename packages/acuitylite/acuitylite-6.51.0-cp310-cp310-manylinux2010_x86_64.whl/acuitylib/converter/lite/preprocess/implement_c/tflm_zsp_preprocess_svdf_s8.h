#ifndef __TFLM_ZSP_PREPROCESS_SVDF_S8_H__
#define __TFLM_ZSP_PREPROCESS_SVDF_S8_H__

#include <stdint.h>
#include "tflm_zsp_preprocess_common.h"

//weights_feature_transpose_data: size = input_dims.h * weights_feature_dims.n
//weights_time_transpose_data: size = weights_time_dims.h * weights_feature_dims.n

void tflm_zsp_filter_trans_int8_svdf(int8_t *weights_feature_data, int8_t *weights_feature_transpose_data,
									int8_t *weights_time_data, int8_t *weights_time_transpose_data,
									int32_t weights_feature_dims_n, int32_t input_dims_h,
									int32_t weights_time_dims_h,int32_t svdf_params_rank);



//ctx_buf size = 2 * sizeof(int64_t)

void tflm_zsp_preprocess_svdf(int32_t *preprocess_buf ,
							int32_t input_multiplier,
							int32_t input_shift,
							int32_t output_multiplier,
							int32_t output_shift,
							int32_t input_type,
							int32_t output_offset);


#endif
